from .aftermerge import AfterMerge
from .nextrelease import NextRelease
import sys


def git_aftermerge():
    if len(sys.argv) != 2:
        print("this requires ['patch','minor','major']")
        sys.exit(1)
    am = AfterMerge()
    am.main()
    sys.exit(0)
    print("after merge")


def git_nextrelease():
    if len(sys.argv) == 2:
        release = sys.argv[1]
    else:
        release = "v0.1.0"
    nr = NextRelease(release)
    nr.main()
    print("next release")
