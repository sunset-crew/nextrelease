#!/usr/bin/python3
#
#  Git VersionUpdater
#

import json
from os.path import exists
from os import environ
from .common import GitActions, VersionUpdaterActions

DEBUG = False


class DirtyMasterBranch(Exception):
    pass


class BadIncrement(Exception):
    pass


class ChangesNotInstalled(Exception):
    pass


class PoetryNotInPath(Exception):
    pass


class PoetryVersionUpdater(VersionUpdaterActions):
    def __init__(self, args):
        self.args = args
        self.ga = GitActions(args)
        super().__init__(args)
        if "poetry" not in environ.get("PATH"):
            raise PoetryNotInPath("Poetry bin is not, you might need to install it")
        if not exists(".git"):
            raise DirtyMasterBranch("You need to be in the root of the git repo")

    def update_poetry(self):
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
        self.update_poetry()
        self.gather_info()
        self.update_files()
