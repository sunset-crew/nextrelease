#!/usr/bin/python3
#
#  Git AfterMerge
#

import os
import sys
from .common import GitActions
from .versionupdater import ReleaseVersionUpdater

DEBUG = False


class AfterMerge(object):
    def __init__(self, args):
        self.ga = GitActions(args)
        self.ga.gather_git_info()
        self.args = args

    def main(self):
        last_merged_release = self.ga.find_last_merged_release()
        print(last_merged_release)
        self.ga.tag_last_release_and_push(last_merged_release)
        self.version, self.release, self.branch = self.ga.determine_next_version(
            sys.argv[1], last_merged_release
        )
        self.ga.create_new_branch(self.branch)
        self.ga.git(["branch", "-D", "release_{0}".format(last_merged_release)])
        if os.path.exists(self.ga.version_update_file):
            pvu = ReleaseVersionUpdater(self.args)
            pvu.run_update()
        if self.args.no_remote:
            print(
                self.ga.git(
                    [
                        "push",
                        "-o merge_request.create",
                        "-o merge_request.target=master",
                        "-o merge_request.remove_source_branch",
                        "-o merge_request.title=" + self.branch,
                        "--set-upstream",
                        "origin",
                        self.branch,
                    ]
                ),
                end="",
            )
