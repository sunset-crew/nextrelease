from .aftermerge import AfterMerge
from .nextrelease import NextRelease
from .changelog import ChangeLogActions
from .common import VersionUpdaterActions
import sys
import os


def git_aftermerge():
    if len(sys.argv) != 2:
        print("this requires ['patch','minor','major']")
        sys.exit(1)
    am = AfterMerge()
    am.main()
    sys.exit(0)
    # print("after merge")


def git_nextrelease():
    if len(sys.argv) == 2:
        release = sys.argv[1]
    else:
        release = "v0.1.0"
    nr = NextRelease(release)
    nr.main()
    # print("next release")


def git_versionupdater():
    if len(sys.argv) == 2:
        cmd = sys.argv[1]
    else:
        print("install,uninstall")
        return
    verupact = VersionUpdaterActions()
    actions = {
        "install": verupact.install,
        "uninstall": verupact.uninstall,
    }
    actions[cmd]()
    # print("version updater")


def git_changelog():
    """ Changelog management """
    header = ""
    if len(sys.argv) < 2:
        print("you need at least a change type")
        print("[a]dded|adds,[r]emoved|removes,[c]hanged|changes,[i]nstall")
        sys.exit(1)
    if sys.argv[1].lower() in ["a", "added", "adds"]:
        header = "Added"
    if sys.argv[1].lower() in ["c", "changed", "changes"]:
        header = "Changed"
    if sys.argv[1].lower() in ["r", "removed", "removes"]:
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
    if sys.argv[1].lower() in ["i", "install"]:
        if os.path.exists("CHANGELOG.md"):
            os.remove("CHANGELOG.md")
            sys.exit(0)
        sys.exit(1)
    if len(sys.argv) == 2:
        entry = input("msg: ")
    else:
        entry = " ".join(sys.argv[1:]).lower()
    if os.path.exists("CHANGELOG.md"):
        cla = ChangeLogActions("CHANGELOG.md")
        new_file = cla.new_change_log(header, entry)
        with open("CHANGELOG.md", "w") as f:
            f.write(new_file)
        return
    print("No changelog here, run install")
