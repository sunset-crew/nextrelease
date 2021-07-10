from datetime import datetime
import sys
import os
import subprocess


class WordPlay:
    def __init__(self):
        pass

    def add_s(self):
        pass

    def add_ed(self):
        pass

    def add_d(self):
        pass


class ChangeLogActions(object):
    def __init__(self, filelocation):
        if not os.path.exists(".git"):
            print("this isn't a repo, no control of versioning")
            sys.exit(1)

        self.current_branch = self.get_current_release_branch()
        self.filelocation = filelocation
        self.userhome = os.path.expanduser("~")
        self.username = os.path.split(self.userhome)[-1]
        self.f = []
        self.i = 0
        self.last_line = ""
        self.newhead = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Also based on](https://github.com/conventional-changelog/standard-version/blob/master/CHANGELOG.md) so decending.

"""
        self.obj = {}
        self.curr = "Added"
        with open(self.filelocation, "r") as locfile:
            self.f = locfile.read().splitlines()
        date = datetime.now()
        self.today_string = date.strftime("%Y-%m-%d")

    def run_cmd(self, cmd, everything=None):
        MyOut = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = MyOut.communicate()
        if MyOut.returncode != 0:
            print("cmd {0} return code {1}".format(" ".join(cmd), MyOut.returncode))
        if everything:
            return {
                "out": stdout.decode(),
                "err": stderr.decode(),
                "code": MyOut.returncode,
            }
        else:
            return stdout.decode()

    def get_current_release_branch(self):
        if not os.path.exists(".git"):
            print("this isn't a repo, no control of versioning")
            sys.exit(1)
        current_release = self.run_cmd(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        ).strip()
        if current_release[:7] == "release":
            return current_release
        branches = self.run_cmd(["git", "branch", "--all"]).split("\n")
        for branch in branches:
            if "remotes" in branch and "release" in branch:
                return branch.split("/")[-1].strip()
        raise Exception("No Remotes Found")

    def find_last_version_entry(self):
        for line in self.f:
            if len(line) > 2:
                if line[:2] == "##":
                    self.last_line = line
                    break
            self.i = self.i + 1

    def parse_last_version_entry(self):
        raw_version = self.last_line.split("-")[0]
        # string_date = self.last_line.split("-")[1:]
        start = raw_version.find("[") + 1
        stop = raw_version.find("]")
        self.version = self.current_branch[9:]
        self.new = True
        if raw_version[start:stop] == self.current_branch[9:]:
            self.new = False
        if self.version.strip() == "":
            raise Exception("Version unknown")
        print(self.version)

    def parse_version_information(self):
        obj = {
            "Added": {"active": False, "data": []},
            "Removed": {"active": False, "data": []},
            "Changed": {"active": False, "data": []},
        }
        if not self.new:
            count = self.i + 1
            for line in self.f[count:]:
                self.i = self.i + 1
                if len(line) > 3 and line[:3] == "## ":
                    break

                if (
                    self.curr != ""
                    and line[2:] != ""
                    and obj[self.curr]["active"]
                    and line[:3] != "###"
                ):
                    obj[self.curr]["data"] += [line[2:]]
                    continue

                if len(line) > 3 and line[:3] == "###":
                    # print(line[3:].strip())
                    obj[self.curr]["active"] = False
                    self.curr = line[3:].strip()
                    obj[self.curr]["active"] = True
                # next_lines.append(line)
        return obj

    def build_updated_section(self, obj):
        self.updated_section = f"## [{self.version}] - {self.today_string}\n"
        for k, v in obj.items():
            if len(v["data"]) > 0:
                self.updated_section += "### " + k + "\n"
                for data in v["data"]:
                    self.updated_section += "- " + data + "\n"
                self.updated_section += "\n"

    def new_change_log(self, heading, entry):
        self.find_last_version_entry()
        self.parse_last_version_entry()
        obj = self.parse_version_information()
        # obj = self.add_data_to_object(obj,"Added","adds the proper thing now")
        obj[heading]["data"].append(entry)
        self.build_updated_section(obj)
        count = self.i
        the_rest_of_the_doc = "\n".join(self.f[count:])
        # print(self.newhead+self.updated_section+the_rest_of_the_doc)
        return self.newhead + self.updated_section + the_rest_of_the_doc


class ChangeLogController:
    def __call__(self):
        """ Changelog management """
        header = ""
        if len(sys.argv) < 2:
            print("you need at least a change type")
            print("[a]dded|adds,[r]emoved|removes,[c]hanged|changes,[i]nstall")
            sys.exit(1)

        if sys.argv[1].lower() in ["a", "added", "adds", "installs", "loads"]:
            header = "Added"
        if sys.argv[1].lower() in [
            "c",
            "changed",
            "changes",
            "decouples",
            "edits",
            "fixes",
            "updates",
            "sets",
            "repairs",
            "replaces",
            "configures",
            "refactors",
            "prevents",
            "allows",
        ]:
            header = "Changed"
        if sys.argv[1].lower() in ["r", "removed", "removes", "cleans"]:
            header = "Removed"

        if sys.argv[1].lower() in ["i", "install"]:
            if os.path.exists("CHANGELOG.md"):
                print("already exists")
                sys.exit(1)
            newfile = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Also based on](https://github.com/conventional-changelog/standard-version/blob/master/CHANGELOG.md) so decending.

## [0.1.0] - 2020-12-22
### Added
- bot - adds changelog
"""
            with open("CHANGELOG.md", "w") as f:
                f.write(newfile)
            print("changelog installed")
            sys.exit(0)
        if sys.argv[1].lower() in ["r", "remove"]:
            if os.path.exists("CHANGELOG.md"):
                os.remove("CHANGELOG.md")
                sys.exit(0)
            sys.exit(1)

        if sys.argv[1].lower() in ["e", "check"]:
            if os.path.exists("CHANGELOG.md"):
                cla = ChangeLogActions("CHANGELOG.md")
                print(cla.get_current_release_branch())
            return

        if len(sys.argv) == 2:
            entry = input("msg: ")
        else:
            entry = " ".join(sys.argv[1:]).lower()
        if os.path.exists("CHANGELOG.md"):
            cla = ChangeLogActions("CHANGELOG.md")
            new_file = cla.new_change_log(header, entry)
            with open("CHANGELOG.md", "w") as f:
                f.write(new_file)
            cla.run_cmd(["git", "add", "."])
            commit_cmd = ["git", "commit", "-a", """-m{0} """.format(entry)]
            print(" ".join(commit_cmd))
            cla.run_cmd(commit_cmd)
            return
        print("No changelog here, run install")
