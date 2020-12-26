#!/usr/bin/python3
#
#  Git AfterMerge
#

import os
import json
from pkg_resources import parse_version
import sys
from os.path import exists
from os import environ
from .common import GitActions

ga = GitActions()

DEBUG = False


class DirtyMasterBranch(Exception):
    pass


class BadIncrement(Exception):
    pass


class ChangesNotInstalled(Exception):
    pass


class PoetryNotInPath(Exception):
    pass


class PoetryVersionUpdater(object):
    def __init__(self):
        if "poetry" not in environ.get("PATH"):
            raise PoetryNotInPath("Poetry bin is not, you might need to install it")

    def update_poetry(self, increment):
        if increment not in ["patch", "minor", "major"]:
            raise BadIncrement("incorrect increment string\npatch,minor,major only ")
        self.msg = ga.run_code(["poetry", "version", increment])
        print(self.msg)

    def gather_info(self):
        self.config = ga.get_project_info()
        self.file_changes = {}

        if exists(ga.version_update_file):
            with open(ga.version_update_file, "r") as j:
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
        print(ga.git(["add", ".", "--all" ""]))
        print(ga.git(["commit", "-a", f"""-m"{self.msg}" """]))

    def main(self):
        self.gather_info()
        self.update_files()


class AfterMerge(object):
    def __init__(self):
        ga.gather_git_info()

    def determine_next_version(self, last_merge_release):
        pv = parse_version(last_merge_release)
        p = [int(x) for x in pv.base_version.split(".")]
        if sys.argv[1] in ["major", "mj"]:
            # major
            p[0] = p[0] + 1
            p[1] = 0
            p[2] = 0
        # minor
        elif sys.argv[1] in ["minor", "mn"]:
            p[1] = p[1] + 1
            p[2] = 0
        # patch
        else:
            p[2] = p[2] + 1

        self.version = "{0}.{1}.{2}".format(p[0], p[1], p[2])
        self.release = "v{0}".format(self.version)
        self.branch = "release_{0}".format(self.release)

    def main(self):
        last_merged_release = ga.find_last_merged_release()
        print(last_merged_release)
        ga.tag_last_release_and_push(last_merged_release)
        self.determine_next_version(last_merged_release)
        ga.create_new_branch(self.branch)
        ga.git(["branch", "-D", "release_{0}".format(last_merged_release)])
        if os.path.exists(ga.version_update_file):
            pvu = PoetryVersionUpdater()
            pvu.update_poetry(sys.argv[1])
            pvu.main()
        print(ga.git(["push", "--set-upstream", "origin", self.branch]))
