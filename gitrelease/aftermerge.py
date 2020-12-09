#!/usr/bin/python3
#
#  Git AfterMerge
#

import subprocess
import os 
from pkg_resources import parse_version
import sys
import configparser
from os.path import exists
from os import environ
import subprocess
import uuid


if len(sys.argv) != 2:
  print("you need a command")
  sys.exit(1)

DEBUG=False

class DirtyMasterBranch(Exception):
  pass

class BadIncrement(Exception):
    pass

class ChangesNotInstalled(Exception):
    pass

class PoetryNotInPath(Exception):
    pass

class PoetryVersionUpdater(object):
    def __init__(self,increment):
        if increment not in ["patch","minor","major"]:
            raise BadIncrement("incorrect increment string\npatch,minor,major only ")
        if "poetry" not in environ.get("PATH"):
            raise PoetryNotInPath("Poetry bin is not, you might need to install it")
        code = f"""poetry version {increment}"""
        self.msg = run_code(code)
        self.config = {}
        self.config["config"] = configparser.ConfigParser()                                     
        self.config["config"].read('pyproject.toml')
        self.config["version"] = config["config"].get('tool.poetry', 'version')
        self.config["project"] = config["config"].get('tool.poetry', 'name')
        self.file_changes = {}
        if exists("./version_updater.json"):
            with open("./version_updater.json",r) as j:
                self.file_changes = json.load(j)
        else:
            raise ChangesNotInstalled("version_updater.json not present. Please Install one")
        return

    def install(self):
        self.file_changes = gen_std_file_changes()
        with open("./version_updater.json",w) as j:
            json.dump(j,self.file_changes)
          
    def run_code(self,code,everything=False,script=False):
        if script:
          tmpfilename = "/tmp/"+str(uuid.uuid4())[:8]+".sh"
          code = code + "\nrm -f "+tmpfilename
          with open(tmpfilename, "w") as f:
              f.write(code)
          MyOut = subprocess.Popen(["bash",tmpfilename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
          MyOut = subprocess.Popen(code, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = MyOut.communicate()
        if MyOut.returncode != 0:
            print("cmd {0} return code {1}".format(" ".join(cmd),MyOut.returncode))
        if stderr is not None:
            print("stderr")
            print(stderr)
        if everything:
            return { "out": stdout, "err": stdout,"obj": MyOut }
        else:
            return stdout.decode()

    def gen_std_file_changes():
        return [
            {"name": "Makefile", "searchStr": "VERSION :=", "formatStr": "VERSION := {0}\n"},
            {
                "name": "tests/test_{0}.py".format(config["project"]),
                "searchStr": "    assert __version__",
                "formatStr": """    assert __version__ == "{0}"\n""",
            },
            {
                "name": "{0}/__init__.py".format(config["project"]),
                "searchStr": "__version__ =",
                "formatStr": """__version__ = "{0}"\n""",
            },
        ]

    def main(self):
        for fc in self.file_changes:
            if not exists(fc["name"]):
                print(fc["name"],"does not exist")
                continue
            with open(fc["name"], "r") as f:
                lines = f.readlines()
            try:
                with open(fc["name"], "w") as f:
                    for line in lines:
                        if line[: len(fc["searchStr"])] == fc["searchStr"]:
                            f.write(fc["formatStr"].format(self.config["version"]))
                        else:
                            f.write(line)
                print("updated {0}".format(fc["name"]))
            except Exception:
                # if the change fails, restore old file
                with open(fc["name"], "w") as f:
                    for line in lines:
                        f.write(line)
        print(run_code(["git","add",".","--all"""]))
        print(run_code(["git","commit","-a",f"""-m"{self.msg}" """]))



class AfterMerge(object):
    def __init__(self):
        self.tags = [ x for x in self.run_cmd(["git", "tag"]).split("\n") if x ]
        self.branchs = [ x.strip("'") for x in self.run_cmd(["git", "for-each-ref", "--format='%(refname:short)'", "refs/heads/*"]).split("\n") if x ]
        self.current_name = self.run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()
        self.last_merge_release = "not_set"

    def get_user_info(self):
        userhome = os.path.expanduser("~")
        return {"user": os.path.split(userhome)[-1], "userhome": userhome}

    def run_cmd(self, cmd):
        if DEBUG:
            print(" ".join(cmd))
        MyOut = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = MyOut.communicate()
        if MyOut.returncode != 0:
            print("cmd {0} return code {1}".format(" ".join(cmd),MyOut.returncode))
        if stderr is not None:
            print("stderr")
            print(stderr)
        return stdout.decode()

    def get_last_merged_release(self):
      self.run_cmd(["git","checkout","master"])
      self.run_cmd(["git","pull"])
      branch = ""
      o = self.run_cmd(["git", "log"]).strip()
      lines = [ x.strip() for x in o.split("\n") if x.strip() ]
      looping = True
      while looping:
        line = lines.pop(0)  
        if line[:12] == "Merge branch":
          branch = line.split(' ')[2].strip("'")
          print(branch)
          looping = False
      try:
        return branch.split('_')[1]
      except IndexError:
        raise

    def grab_and_commit_last_release_tag(self):
      try:
        self.last_merge_release = self.get_last_merged_release()
      except IndexError:
        raise DirtyMasterBranch("dirty master branch")
      print(self.last_merge_release)
      if self.last_merge_release == "not_set":
        print("something wrong with repo")
        sys.exit(1)
      if self.last_merge_release not in self.tags:
        if os.path.exists("./pre_tag.sh"):
            print(self.run_cmd(["bash","pre_tag.sh",sys.argv[1],self.last_merge_release]))
        self.run_cmd(["git","tag","-a",self.last_merge_release,"-m'new release {0}'".format(self.last_merge_release)])
        self.run_cmd(["git","push","--tags"])
        if os.path.exists("./post_tag.sh"):
            print(self.run_cmd(["bash","post_tag.sh",sys.argv[1],self.last_merge_release]))
      else:
        print("tag already exists, check the merge")
        sys.exit(1)

    def determine_next_version(self):
      pv = parse_version(self.last_merge_release)
      p = [ int(x) for x in pv.base_version.split(".") ]
      if sys.argv[1] in ["major","mj"]:
      # major
        p[0] = p[0] + 1
        p[1] = 0
        p[2] = 0
      # minor
      elif sys.argv[1] in ["minor","mn"]:
        p[1] = p[1] + 1
        p[2] = 0
      # patch
      else:
        p[2] = p[2] + 1
      self.version = "{0}.{1}.{2}".format(p[0],p[1],p[2])
      self.release = "v{0}".format(self.version)
      self.branch = "release_{0}".format(self.release)

    def main(self):
      self.grab_and_commit_last_release_tag()
      self.determine_next_version()
      output = self.run_cmd(["git","checkout","master"])
      output += self.run_cmd(["git","pull"])
      output += self.run_cmd(["git","fetch","-p"])
      output += self.run_cmd(["git","branch","-D", "release_{0}".format(self.last_merge_release)])
      output += self.run_cmd(["git","checkout","-b", self.branch])
      pvu = PoetryVersionUpdater()
      pvu.main()
      if os.path.exists("./new_release.sh"):
          print(self.run_cmd(["bash","new_release.sh",sys.argv[1],self.last_merge_release]))
      output += self.run_cmd(["git","push","--set-upstream", "origin", self.branch])
      print(output)
