#!/usr/bin/env python3
# from os.path import exists
# from os import environ
from .common import GitActions
import argparse
from .config import Settings
from os import getenv


class Command(object):
    def __init__(self):
        self.settings = Settings()()
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--no-remote",
            action="store_false",
            help="Dont use the remote based commands",
        )
        self.parser.add_argument(
            "--title-separator",
            dest="title_separator",
            help="the character that separates the title from the body",
            default=getenv(
                "TITLE_SEPARATOR", self.settings["config"]["title_separator"]
            ),
        )
        self.parser.add_argument(
            "--body-separator",
            dest="body_separator",
            help="the character to replaces whitespace in the body of the msg",
            default=getenv("BODY_SEPARATOR", self.settings["config"]["body_separator"]),
        )
        subparsers = self.parser.add_subparsers(
            dest="action",
            title="Action SubCommands",
            description="This are the action subcommands",
            required=True
            # help="If you need extra help let me know",
        )
        # fix = subparsers.add_parser("fix", help="Create a fix branch")
        fix = subparsers.add_parser("fix", help="Create a fix branch")
        fix.add_argument("fix_branch_name", nargs="*", help="name of the Fix branch")
        # feature = subparsers.add_parser("feature", help="Create a feature branch")
        feature = subparsers.add_parser("feature", help="Create a feature branch")
        feature.add_argument(
            "feature_branch_name", nargs="*", help="name of the feature"
        )
        self.args = self.parser.parse_args()
        self.ga = GitActions(self.args)
        return

    def __call__(self):
        if self.args.action:
            func = getattr(self, self.args.action)
            return func()
        self.parser.print_help()

    def fix(self):
        if len(self.args.fix_branch_name) == 0:
            return "the branch needs a name"
        name = f"{self.args.body_separator}".join(self.args.fix_branch_name)
        name = f"fix{self.args.title_separator}{name}"
        print(self.ga.git(["checkout", "-b", name]))
        if self.args.no_remote:
            self.ga.git(["push", "--set-upstream", "origin", name])

    def feature(self):
        if len(self.args.feature_branch_name) == 0:
            return "the branch needs a name"
        name = f"{self.args.body_separator}".join(self.args.feature_branch_name)
        name = f"feature{self.args.title_separator}{name}"
        print(self.ga.git(["checkout", "-b", name]))
        if self.args.no_remote:
            self.ga.git(["push", "--set-upstream", "origin", name])


def main():
    return Command()()


if __name__ == "__main__":
    print(main())
