#!/usr/bin/python3
#
#  Git NextRelease
#
from os.path import exists
from os import environ
from .common import GitActions

ga = GitActions()


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


class NextRelease:
    def __init__(self, release):
        # self.release = "v{0}.{1}.{2}".format(major,minor,patch)
        self.branch = "release_{0}".format(release)

    def main(self):
        ga.create_new_branch(self.branch)
