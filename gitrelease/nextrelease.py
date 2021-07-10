#!/usr/bin/python3
#
#  Git NextRelease
#
from os.path import exists
from os import environ
from .common import GitActions
import argparse


class PoetryNotInPath(Exception):
    pass


class AlreadyExistsError(Exception):
    pass


class PoetryInstallVersionUpdater(object):
    def __init__(self, project):
        if "poetry" not in environ.get("PATH"):
            raise PoetryNotInPath("Poetry bin is not, you might need to install it")
        if exists("./version_updater.json"):
            raise AlreadyExistsError("version_updater.json exists already")
        self.project = project
        self.file_changes = []


class NextRelease(object):
    def __init__(self, args):
        self.args = args
        self.ga = GitActions(self.args)
        self.ga.gather_git_info()
        # self.release = "v{0}.{1}.{2}".format(major,minor,patch)
        self.branch = "release_{0}".format(self.args.release)

    def __call__(self):
        self.ga.create_new_branch(self.branch)
        if self.args.no_remote:
            self.ga.git(["push", "--set-upstream", "origin", self.branch])


class NextReleaseController(NextRelease):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--no-remote",
            action="store_false",
            help="Dont use the remote based commands",
        )
        parser.add_argument(
            "--release", default="v0.1.0", help="You need the v, Default=v0.1.0"
        )
        super().__init__(parser.parse_args())
