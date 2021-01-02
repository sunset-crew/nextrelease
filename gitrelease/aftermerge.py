#!/usr/bin/python3
#
#  Git AfterMerge
#

import os
from pkg_resources import parse_version
import sys
from .common import GitActions
from .versionupdater import PoetryVersionUpdater

ga = GitActions()

DEBUG = False


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
            pvu.run_update()
        print(ga.git(["push", "--set-upstream", "origin", self.branch]), end="")
