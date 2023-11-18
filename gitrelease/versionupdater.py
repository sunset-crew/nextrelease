#!/usr/bin/python3
#
#  Git VersionUpdater
#

import json
from os.path import exists
from os import environ
from .common import GitActions, VersionUpdaterActions
import argparse
from shutil import which

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
        self.ga = GitActions(args)
        super().__init__(args)
        self.current_tag = self.ga.get_current_tag().strip("\n")
        if self.args.action != "install":
            self.next_tag_info = self.ga.determine_next_version(
                self.args.increment, self.current_tag
            )
        if not exists(".git"):
            raise GitDirNotFound("You need to be in the root of the git repo")

    def update_version(self):
        # ~ current_tag = self.ga.get_current_tag().strip("\n")
        # ~ next_tag_info = self.ga.determine_next_version(self.args.increment, self.current_tag)
        lines = []
        with open(".version", "r") as f:
            lines = f.read()
        print(lines)
        new = [
            "VERSION=" + self.next_tag_info[0] if "VERSION" in line else line
            for line in lines.split("\n")
        ]
        with open(".version", "w") as f:
            f.write("\n".join(new))
        self.msg = f"Bumping {self.current_tag} to {self.next_tag_info[1]}\n"
        print(self.msg, end="")

    def update_cargo(self):
        self.msg = f"Bumping {self.current_tag} to {self.next_tag_info[1]}\n"
        print(self.msg, end="")

    def update_poetry(self):
        if "poetry" not in environ.get("PATH") and not which("poetry"):
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

    def run(self):
        if exists(".version"):
            self.update_version()
        elif exists("pyproject.toml"):
            self.update_poetry()
        elif exists("Cargo.toml"):
            self.update_cargo()
        else:
            raise NoProjectDataFile(
                "maybe add a .version file with an appname and version"
            )
        # print(self.msg)
        self.gather_info()
        self.update_files()


class ReleaseVersionUpdaterController(ReleaseVersionUpdater):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--no-remote",
            action="store_false",
            help="Dont use the remote based commands",
        )
        subparser = parser.add_subparsers(dest="action")
        subparser.add_parser("install", help="Install Version Updater")
        subparser.add_parser("uninstall", help="Uninstall Version Updater")
        run = subparser.add_parser("run", help="Run an Update, type")
        run.add_argument("increment", help="patch, minor, major", default="patch")
        super().__init__(parser.parse_args())

    def __call__(self):
        allowed_funcs = [
            "install",
            "uninstall",
            "run",
        ]
        if self.args.action in allowed_funcs:
            getattr(self, self.args.action)()
