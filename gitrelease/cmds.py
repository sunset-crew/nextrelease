from .aftermerge import AfterMerge
from .nextrelease import NextRelease
from .changelog import ChangeLogActions
from .versionupdater import ReleaseVersionUpdater
import sys
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--no-remote", action="store_false", help="Dont use the remote based commands"
)


def git_aftermerge():
    # subparser = parser.add_subparsers(dest="action")
    parser.add_argument("increment", help="this requires ['patch','minor','major']")
    args = parser.parse_args()
    am = AfterMerge(args)
    am.main()
    sys.exit(0)
    # print("after merge")


def git_nextrelease():
    parser.add_argument(
        "--release", default="v0.1.0", help="You need the v, Default=v0.1.0"
    )
    args = parser.parse_args()
    nr = NextRelease(args)
    nr.main()
    # print("next release")


def git_versionupdater():
    subparser = parser.add_subparsers(dest="action")
    subparser.add_parser("install", help="Install Version Updater")
    subparser.add_parser("uninstall", help="Uninstall Version Updater")
    run = subparser.add_parser("run", help="Run an Update, type")
    run.add_argument("increment", help="patch, minor, major")
    args = parser.parse_args()
    poetverup = ReleaseVersionUpdater(args)
    actions = {
        "install": poetverup.install,
        "uninstall": poetverup.uninstall,
        "run": poetverup.run_update,
    }
    actions[args.action]()

    # print("version updater")


def git_changelog():
    """ Changelog management """
    header = ""
    if len(sys.argv) < 2:
        print("you need at least a change type")
        print("[a]dded|adds,[r]emoved|removes,[c]hanged|changes,[i]nstall")
        sys.exit(1)
    if sys.argv[1].lower() in ["a", "added", "adds", "installs", "loads"]:
        header = "Added"
    if sys.argv[1].lower() in [
        "c",
        "changed",
        "changes",
        "decouples",
        "edits",
        "fixes",
        "updates",
        "sets",
        "repairs",
        "replaces",
        "configures",
        "refactors",
    ]:
        header = "Changed"
    if sys.argv[1].lower() in ["r", "removed", "removes", "cleans"]:
        header = "Removed"

    if sys.argv[1].lower() in ["i", "install"]:
        if os.path.exists("CHANGELOG.md"):
            print("already exists")
            sys.exit(1)
        newfile = """# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[Also based on](https://github.com/conventional-changelog/standard-version/blob/master/CHANGELOG.md) so decending.

## [0.1.0] - 2020-12-22
### Added
- bot - adds changelog

"""
        with open("CHANGELOG.md", "w") as f:
            f.write(newfile)
        print("changelog installed")
        sys.exit(0)
    if sys.argv[1].lower() in ["r", "remove"]:
        if os.path.exists("CHANGELOG.md"):
            os.remove("CHANGELOG.md")
            sys.exit(0)
        sys.exit(1)

    if sys.argv[1].lower() in ["e", "check"]:
        if os.path.exists("CHANGELOG.md"):
            cla = ChangeLogActions("CHANGELOG.md")
            print(cla.get_current_release_branch())
        return

    if len(sys.argv) == 2:
        entry = input("msg: ")
    else:
        entry = " ".join(sys.argv[1:]).lower()
    if os.path.exists("CHANGELOG.md"):
        cla = ChangeLogActions("CHANGELOG.md")
        new_file = cla.new_change_log(header, entry)
        with open("CHANGELOG.md", "w") as f:
            f.write(new_file)
        cla.run_cmd(["git", "add", "."])
        commit_cmd = ["git", "commit", "-a", """-m{0} """.format(entry)]
        print(" ".join(commit_cmd))
        cla.run_cmd(commit_cmd)
        return
    print("No changelog here, run install")
