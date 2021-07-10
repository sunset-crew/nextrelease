from .aftermerge import AfterMergeController
from .nextrelease import NextReleaseController
from .changelog import ChangeLogController
from .versionupdater import ReleaseVersionUpdaterController


def git_aftermerge():
    cmd = AfterMergeController()
    cmd()


def git_nextrelease():
    cmd = NextReleaseController()
    cmd()


def git_versionupdater():
    cmd = ReleaseVersionUpdaterController()
    cmd()


git_changelog = ChangeLogController()
