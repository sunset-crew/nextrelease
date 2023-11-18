#!/usr/bin/python3
#
#  Git AfterMerge
#

import os
import sys
from .common import GitActions
from .versionupdater import ReleaseVersionUpdater
import argparse

DEBUG = False


class AfterMerge(object):
    def __init__(self, args):
        self.ga = GitActions(args)
        self.ga.gather_git_info()
        self.args = args
        self.main_branch = "main" if self.ga.check_git_branch("main") else "master"

    def __call__(self):
        last_merged_release = self.ga.find_last_merged_release()
        print(last_merged_release)
        self.ga.tag_last_release_and_push(last_merged_release)
        self.version, self.release, self.branch = self.ga.determine_next_version(
            sys.argv[1], last_merged_release
        )
        self.ga.create_new_branch(self.branch)
        self.ga.git(["branch", "-D", "release_{0}".format(last_merged_release)])
        if os.path.exists(self.ga.version_update_file):
            self.args.action = "run"
            pvu = ReleaseVersionUpdater(self.args)
            pvu.run()
        if self.args.no_remote:
            print(
                self.ga.git(
                    [
                        "push",
                        "-o merge_request.create",
                        "-o merge_request.target=" + self.main_branch,
                        "-o merge_request.remove_source_branch",
                        "-o merge_request.title=" + self.branch,
                        "--set-upstream",
                        "origin",
                        self.branch,
                    ]
                ),
                end="",
            )


class AfterMergeController(AfterMerge):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--no-remote",
            action="store_false",
            help="Dont use the remote based commands",
        )
        parser.add_argument("increment", choices=["patch", "minor", "major"])
        super().__init__(parser.parse_args())
