#!/usr/bin/python3
#
#  Git NextRelease
#

import subprocess
import sys
from os import exists

class PoetryInstallVersionUpdater(object):
    def __init__(self,project):
        if "poetry" not in environ.get("PATH"):
            raise PoetryNotInPath("Poetry bin is not, you might need to install it")
        if exists("./version_updater.json"):
            raise AlreadyExistsError("version_updater.json exists already")
        self.project = project

    def install(self):
        self.file_changes = gen_std_file_changes()
        with open("./version_updater.json",w) as j:
            json.dump(j,self.file_changes)

    def gen_std_file_changes():
        return [
            {"name": "Makefile", "searchStr": "VERSION :=", "formatStr": "VERSION := {0}\n"},
            {
                "name": "tests/test_{0}.py".format(self.project),
                "searchStr": "    assert __version__",
                "formatStr": """    assert __version__ == "{0}"\n""",
            },
            {
                "name": "{0}/__init__.py".format(self.project),
                "searchStr": "__version__ =",
                "formatStr": """__version__ = "{0}"\n""",
            },
        ]

class NextRelease():

    def __init__(self, release):
        # self.release = "v{0}.{1}.{2}".format(major,minor,patch)
        self.branch = "release_{0}".format(release)

    def run_code(self,code,everything=False,script=False,verbose=False):
        if script:
          tmpfilename = "/tmp/"+str(uuid.uuid4())[:8]+".sh"
          if verbose:
              print("making ",tmpfilename)
          code = code + "\nrm -vf "+tmpfilename
          with open(tmpfilename, "w") as f:
              f.write(code)
          MyOut = subprocess.Popen(["bash",tmpfilename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
          MyOut = subprocess.Popen(code, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = MyOut.communicate()
        if verbose:
            if MyOut.returncode != 0:
                print("cmd {0} return code {1}".format(" ".join(cmd),MyOut.returncode))
            if stderr is not None:
                print("stderr")
                print(stderr)
        if everything:
            return { "out": stdout, "err": stdout,"obj": MyOut }
        else:
            return stdout.decode()

    def main(self):
        runit = """#!/bin/bash
git checkout master
git pull
git fetch -p 
git checkout -b {0}
git push --set-upstream origin {0}
""".format(self.branch)
        print(run_code(runit,everything=False,script=True))
