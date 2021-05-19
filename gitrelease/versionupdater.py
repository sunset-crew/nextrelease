#!/usr/bin/python3
#
#  Git VersionUpdater
#

import json
from os.path import exists
from os import environ
from .common import GitActions, VersionUpdaterActions

DEBUG = False


class GitDirNotFound(Exception):
    pass


class DirtyMasterBranch(Exception):
    pass


class BadIncrement(Exception):
    pass


class ChangesNotInstalled(Exception):
    pass


class NoProjectDataFile(Exception):
    pass


class PoetryNotInPath(Exception):
    pass


class ReleaseVersionUpdater(VersionUpdaterActions):
    def __init__(self, args):
        self.args = args
        self.ga = GitActions(args)
        super().__init__(args)
        if not exists(".git"):
            raise GitDirNotFound("You need to be in the root of the git repo")

    def update_version(self):
        current_tag = self.ga.get_current_tag().strip("\n")
        next_tag_info = self.ga.determine_next_version(self.args.increment, current_tag)
        lines = []
        with open(".version", "r") as f:
            lines = f.read()
        print(lines)
        new = [
            "VERSION=" + next_tag_info[0] if "VERSION" in line else line
            for line in lines.split("\n")
        ]
        with open(".version", "w") as f:
            f.write("\n".join(new))
        self.msg = f"Bumping {current_tag} to {next_tag_info[1]}"
        print(self.msg, end="")

    def update_poetry(self):
        if "poetry" not in environ.get("PATH"):
            raise PoetryNotInPath("Poetry bin is not, you might need to install it")
        self.msg = self.ga.run_code(["poetry", "version", self.args.increment])
        print(self.msg, end="")

    def gather_info(self):
        self.config = self.ga.get_project_info()
        self.file_changes = {}
        if exists(self.ga.version_update_file):
            with open(self.ga.version_update_file, "r") as j:
                self.file_changes = json.load(j)
        else:
            raise ChangesNotInstalled(
                f"{self.version_update_file} not present. Please Install one"
            )

    def update_files(self):
        for fc in self.file_changes:
            if not exists(fc["name"]):
                print(fc["name"], "does not exist")
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
        print(self.ga.git(["add", ".", "--all" ""]), end="")
        print(self.ga.git(["commit", "-a", f"""-m{self.msg} """]), end="")

    def run_update(self):
        if exists(".version"):
            self.update_version()
        elif exists("pyproject.toml"):
            self.update_poetry()
        else:
            raise NoProjectDataFile(
                "maybe add a .version file with an appname and version"
            )
        self.gather_info()
        self.update_files()
