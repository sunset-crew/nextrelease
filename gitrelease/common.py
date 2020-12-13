import subprocess
import uuid
import os
import json
import sys


class DefaultValues(object):
    version_update_file = "version_updater.json"
    project = "default"


class CommonFunctions(DefaultValues):
    def run_code(self, code, everything=False, script=False, verbose=False):
        if script:
            tmpfilename = "/tmp/" + str(uuid.uuid4())[:8] + ".sh"
            if verbose:
                print("making ", tmpfilename)
            code = code + "\nrm -vf " + tmpfilename
            with open(tmpfilename, "w") as f:
                f.write(code)
            MyOut = subprocess.Popen(
                ["bash", tmpfilename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        else:
            print(code)
            MyOut = subprocess.Popen(
                code, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        stdout, stderr = MyOut.communicate()
        if verbose:
            if MyOut.returncode != 0:
                print(
                    "cmd {0} return code {1}".format(" ".join(code), MyOut.returncode)
                )
            if stderr is not None:
                print("stderr")
                print(stderr)
        if everything:
            return {"out": stdout, "err": stdout, "obj": MyOut}
        else:
            return stdout.decode()

    def git(self, cmd, **kargs):
        return self.run_code(["git"] + cmd, **kargs)

    def get_user_info(self):
        userhome = os.path.expanduser("~")
        return {"user": os.path.split(userhome)[-1], "userhome": userhome}

    def install(self):
        self.file_changes = self.gen_std_file_changes()
        with open(self.version_update_file, "w") as j:
            json.dump(j, self.file_changes)

    def set_project(self, project):
        self.project = project

    def gen_std_file_changes(self):
        return [
            {
                "name": "Makefile",
                "searchStr": "VERSION :=",
                "formatStr": "VERSION := {0}\n",
            },
            {
                "name": "tests/test_{0}.py".format(self.project),
                "searchStr": "    assert __version__",
                "formatStr": "    assert __version__ == {0}\n",
            },
            {
                "name": "{0}/__init__.py".format(self.project),
                "searchStr": "__version__ =",
                "formatStr": "__version__ = {0}\n",
            },
        ]


class GitActions(CommonFunctions):
    def gather_git_info(self):
        self.git(
            ["checkout", "master"]
        )  # use everything to determine if this checkout worked.
        self.git(["pull"])
        self.tags = [x for x in self.git(["tag"]).split("\n") if x]
        self.branches = [
            x.strip("'")
            for x in self.git(
                ["for-each-ref", "--format='%(refname:short)'", "refs/heads/*"]
            ).split("\n")
            if x
        ]
        self.current_name = self.git(["rev-parse", "--abbrev-ref", "HEAD"]).strip()

    def find_last_merged_release(self):
        branch = ""
        o = self.git(["log"]).strip()
        lines = [x.strip() for x in o.split("\n") if x.strip()]
        print(lines)
        looping = True
        while looping:
            line = lines.pop(0)
            if line[:12] == "Merge branch":
                branch = line.split(" ")[2].strip("'")
                print(branch)
                looping = False
        try:
            return branch.split("_")[1]
        except IndexError:
            raise

    def tag_last_release_and_push(self, last_merged_release):
        print(last_merged_release)
        if last_merged_release == "not_set":
            print("something wrong with repo")
            sys.exit(1)
        if last_merged_release not in self.tags:
            # pretag decommission
            if os.path.exists("./pre_tag.sh"):
                print(
                    self.run_code(
                        ["bash", "pre_tag.sh", sys.argv[1], last_merged_release]
                    )
                )
            self.git(
                [
                    "tag",
                    "-a",
                    last_merged_release,
                    "-m'new release {0}'".format(last_merged_release),
                ]
            )
            self.git(["push", "--tags"])
            if os.path.exists("./post_tag.sh"):
                print(
                    self.run_code(
                        ["bash", "post_tag.sh", sys.argv[1], last_merged_release]
                    )
                )
        else:
            print("tag already exists, check the merge")
            sys.exit(1)

    def create_new_branch(self, branch):
        print(self.git(["checkout", "master"]))
        print(self.git(["pull"]))
        print(self.git(["fetch", "-p"]))
        print(self.git(["checkout", "-b", branch]))
