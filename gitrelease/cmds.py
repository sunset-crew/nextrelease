from .aftermerge import AfterMerge
from .nextrelease import NextRelease
from .common import VersionUpdaterActions
import sys


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
