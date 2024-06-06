import os
import sys
from .common import GitActions
import argparse

DEBUG = False


class FakePR(object):
    def __init__(self, args):
        self.ga = GitActions(args)
        self.current = self.get_current_release_branch()
        self.args = args
        self.main_branch = "main" if self.ga.check_git_branch("main") else "master"

    def get_current_release_branch(self):
        if not os.path.exists(".git"):
            print("this isn't a repo, no control of versioning")
            sys.exit(1)
        current_release = self.ga.git(["rev-parse", "--abbrev-ref", "HEAD"]).strip()
        if current_release[:7] == "release":
            return current_release
        branches = self.ga.git(["branch", "--all"]).split("\n")
        for branch in branches:
            if "release" in branch:
                return branch.strip()
        raise Exception("No Remotes Found")

    def __call__(self):
        print(self.current)
        merge_msg = f"Merge pull request from {self.current} into {self.main_branch}"
        self.ga.git(["checkout", self.main_branch])
        self.ga.git(
            [
                "merge",
                "--no-ff",
                self.current,
                "-m{0}".format(merge_msg),
            ]
        )
        # self.ga.git(["branch", "-D", "{0}".format(self.current)])
        # $ git checkout main
        # # you need to force the merge commit --no-ff
        # $ git merge --no-ff release_vx.x.x
        # $ git branch -D release_vx.x.x


class FakePRController(FakePR):
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--no-remote",
            action="store_false",
            help="Dont use the remote based commands",
        )
        super().__init__(parser.parse_args())
