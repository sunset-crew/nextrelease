from .aftermerge import AfterMerge
from .nextrelease import NextRelease

def git_aftermerge():
    am = AfterMerge()
    am.main()
    sys.exit(0)
    print("after merge")

def git_nextrelease():
    if len(sys.argv) != 2:
      release = sys.argv[1]
    else:
      release = "v0.1.0"
    nr = NextRelease(release)
    nr.main()

    print("next release")

