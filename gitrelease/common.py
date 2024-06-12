import subprocess
import uuid
import os
import re
import json
import sys
import configparser
from io import StringIO
from pkg_resources import parse_version


class MissingProjectConfig(Exception):
    pass


class MissingMergeCommit(Exception):
    pass


class MissingCommitLog(Exception):
    pass


class DefaultValues(object):
    version_update_file = "version_updater.json"
    project = "default"


class CommonFunctions(DefaultValues):
    def run_code(self, code, everything=False, script=False, verbose=False):
        if script:
            tmpfilename = "/tmp/" + str(uuid.uuid4())[:8] + ".sh"
            if verbose:
                print("making ", tmpfilename)
            code = code + "\nrm -vf " + tmpfilename
            with open(tmpfilename, "w") as f:
                f.write(code)
            MyOut = subprocess.Popen(
                ["bash", tmpfilename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        else:
            if verbose:
                print(code)
            MyOut = subprocess.Popen(
                code, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
            )
        stdout, stderr = MyOut.communicate()
        if verbose:
            if MyOut.returncode != 0:
                print(
                    "cmd {0} return code {1}".format(" ".join(code), MyOut.returncode)
                )
            if stderr is not None:
                print("stderr")
                print(stderr)
        if everything:
            return {"out": stdout, "err": stdout, "obj": MyOut}
        else:
            return stdout.decode()

    def git(self, cmd, **kargs):
        return self.run_code(["git"] + cmd, **kargs)

    def check_for_pdm(self):
        with open("pyproject.toml") as f:
            for line in f:
                if line.strip() == "[project]":
                    return True
        return False

    def get_user_info(self):
        userhome = os.path.expanduser("~")
        return {"user": os.path.split(userhome)[-1], "userhome": userhome}

    def dotenv_data(self):
        if os.path.isfile(".version"):
            command = 'env -i bash -c "source .version && env"'
            for line in subprocess.getoutput(command).split("\n"):
                key, value = line.split("=")
                print(key, value)
                os.environ[key] = value

    def get_pdm_info(self):
        out = ""
        start = False
        cnt = 0
        limit = 3
        with open("pyproject.toml") as f:
            for line in f:
                if cnt > limit:
                    break
                if line.strip() == "[project]":
                    start = True
                if start:
                    out += line
                    cnt += 1
        buf = StringIO(out)
        config = configparser.ConfigParser()
        config.read_file(buf)
        version = config["project"]["version"]
        name = config["project"]["name"]
        return version, name

    def get_project_info(self):
        config = {}
        if os.path.exists(".version"):
            parser = configparser.ConfigParser()
            with open(".version") as stream:
                parser.read_string("[top]\n" + stream.read())
            config["version"] = parser["top"]["version"]
            config["project"] = parser["top"]["appname"].replace('"', "")
            return config

        if os.path.exists("pyproject.toml"):
            config["config"] = configparser.ConfigParser()
            if self.check_for_pdm():
                config["version"], config["project"] = self.get_pdm_info()
                return config
            print(self.check_for_pdm())
            config["config"].read("pyproject.toml")
            config["version"] = (
                config["config"].get("tool.poetry", "version").replace('"', "")
            )
            config["project"] = (
                config["config"].get("tool.poetry", "name").replace('"', "")
            )
            return config

        if os.path.exists("package.json"):
            config["config"] = open("package.json")
            data = json.load(config["config"])
            config["version"] = data["version"]
            config["project"] = data["name"]
            config["config"].close()
            return config

        if os.path.exists("Cargo.toml"):
            print("Cargo")
            config["config"] = configparser.ConfigParser()
            config["config"].read("Cargo.toml")
            config["version"] = (
                config["config"].get("package", "version").replace('"', "")
            )
            config["project"] = config["config"].get("package", "name").replace('"', "")
            return config
        raise MissingProjectConfig("maybe setup an .version")


class VersionUpdaterActions(CommonFunctions):
    def __init__(self, args):
        self.config = self.get_project_info()
        self.args = args

    def uninstall(self):
        if os.path.exists(self.version_update_file):
            os.remove(self.version_update_file)
            print("version_updater.json removed")
            return
        print("version_updater.json not found")

    def install(self):
        if os.path.exists(".git"):
            self.basic_makefile()
            newfile = self.gen_std_file_changes()
            with open(self.version_update_file, "w") as j:
                json.dump(newfile, j)
            print("installed")
            return
        if os.path.exists(".gitignore"):
            ignorelist = []
            with open(".gitignore", "r") as f:
                ignorelist = f.readlines()
            if self.version_update_file not in ignorelist:
                ignorelist.append(self.version_update_file + "\n")
            try:
                with open(".gitignore", "w") as f:
                    f.write("".join(ignorelist))
            except Exception:
                print("no access to .gitignore")
        print("not the root of the repository")

    def basic_makefile(self):
        contents = """VERSION := {0}

clean:
{1}-rm -rf dist
{1}-rm -rf env

patch:
{1}git aftermerge patch || exit 1

minor:
{1}git aftermerge minor || exit 1

major:
{1}git aftermerge major || exit 1

""".format(
            self.config["version"], "	"
        )
        if os.path.exists("Makefile"):
            return "Already exists"

        with open("Makefile", "w") as f:
            f.write(contents)
        return "created Makefile"

    def gen_std_file_changes(self):
        out = []
        if os.path.exists("Makefile"):
            out.append(
                {
                    "name": "Makefile",
                    "searchStr": "VERSION :=",
                    "formatStr": "VERSION := {0}\n",
                }
            )
        if os.path.exists("Cargo.toml"):
            out.append(
                {
                    "name": "Cargo.toml",
                    "searchStr": "version =",
                    "formatStr": """version = "{0}"\n""",
                }
            )

        if os.path.exists("tests/test_{0}.py".format(self.config["project"])):
            out.append(
                {
                    "name": "tests/test_{0}.py".format(self.config["project"]),
                    "searchStr": "    assert __version__ ==",
                    "formatStr": '    assert __version__ == "{0}"\n',
                }
            )

        if os.path.exists(".version"):
            out.append(
                {
                    "name": ".version",
                    "searchStr": "VERSION=",
                    "formatStr": "VERSION={0}\n",
                }
            )

        if os.path.exists("{0}/__init__.py".format(self.config["project"])):
            out.append(
                {
                    "name": "{0}/__init__.py".format(self.config["project"]),
                    "searchStr": "__version__ =",
                    "formatStr": '__version__ = "{0}"\n',
                }
            )

        # ~ if os.path.exists("package.json"):
        # ~ out.append(
        # ~ {
        # ~ "name": "package.json",
        # ~ "searchStr": '"version"',
        # ~ "formatStr": '               "version": "{0}",\n',
        # ~ }
        # ~ )

        return out


class GitActions(CommonFunctions):
    def __init__(self, args):
        self.args = args

    def check_git_branch(self, branch):
        obj = self.run_code(["git", "rev-parse", "--verify", branch], everything=True)
        if obj["obj"].returncode == 0:
            return True
        return False

    def gather_git_info(self):
        if self.check_git_branch("master"):
            self.git(
                ["checkout", "master"]
            )  # use everything to determine if this checkout worked.
        elif self.check_git_branch("main"):
            self.git(
                ["checkout", "main"]
            )  # use everything to determine if this checkout worked.
        if self.args.no_remote:
            self.git(["pull"])
        self.tags = [x for x in self.git(["tag"]).split("\n") if x]
        self.branches = [
            x.strip("'")
            for x in self.git(
                ["for-each-ref", "--format='%(refname:short)'", "refs/heads/*"]
            ).split("\n")
            if x
        ]
        self.current_name = self.git(["rev-parse", "--abbrev-ref", "HEAD"]).strip()

    def find_last_merged_release(self):
        branch = ""
        o = self.git(["log"]).strip()
        lines = [x.strip() for x in o.split("\n") if x.strip()]
        if not lines:
            raise MissingCommitLog("nothing in the git log")
        looping = True
        while looping:
            try:
                line = lines.pop(0)
            except IndexError:
                raise MissingMergeCommit("enable 'Allow merge commits'")
            if line[:10] in ["Merge pull"]:
                try:
                    # github
                    branch = line.split("/")[1]
                except IndexError:
                    # gitea
                    word_list = re.findall(r"release_v\d.\d.\d", line)
                    branch = word_list[0]
                looping = False
            if line[:12] in ["Merge branch"]:
                # gitlab
                branch = line.split(" ")[2].strip("'")
                looping = False
        print(branch)
        try:
            return branch.split("_")[1]
        except IndexError:
            raise

    def tag_last_release_and_push(self, last_merged_release):
        # print(last_merged_release)
        if last_merged_release == "not_set":
            print("something wrong with repo")
            sys.exit(1)
        if last_merged_release not in self.tags:
            # pretag decommission
            if os.path.exists("./pre_tag.sh"):
                print(
                    self.run_code(
                        ["bash", "pre_tag.sh", "aftermerge", last_merged_release]
                    )
                )
            self.git(
                [
                    "tag",
                    "-a",
                    last_merged_release,
                    "-m'new release {0}'".format(last_merged_release),
                ]
            )
            if self.args.no_remote:
                self.git(["push", "--tags"])
            if os.path.exists("./post_tag.sh"):
                print(
                    self.run_code(
                        ["bash", "post_tag.sh", "aftermerge", last_merged_release]
                    ),
                    end="",
                )
        else:
            print("tag already exists, check the merge")
            sys.exit(1)

    def create_new_branch(self, branch):
        trunk_branch = os.getenv("TRUNK_BRANCH", "development")
        if self.check_git_branch(trunk_branch):
            print(self.git(["checkout", trunk_branch]), end="")
        elif self.check_git_branch("master"):
            print(self.git(["checkout", "master"]), end="")
        elif self.check_git_branch("main"):
            print(self.git(["checkout", "main"]), end="")
        else:
            print("Main/Master/Development Branches all missing")
            print("Either set TRUNK_BRANCH env or create the branches")
            sys.exit(1)
        if self.args.no_remote:
            print(self.git(["pull"]), end="")
            print(self.git(["fetch", "-p"]), end="")
        print(self.git(["checkout", "-b", branch]), end="")

    def get_current_tag(self):
        return self.git(["describe", "--abbrev=0"])

    def determine_next_version(self, increment, last_merge_release):
        pv = parse_version(last_merge_release)
        p = [int(x) for x in pv.base_version.split(".")]
        if increment in ["major", "mj"]:
            # major
            p[0] = p[0] + 1
            p[1] = 0
            p[2] = 0
        # minor
        elif increment in ["minor", "mn"]:
            p[1] = p[1] + 1
            p[2] = 0
        # patch
        else:
            p[2] = p[2] + 1

        version = "{0}.{1}.{2}".format(p[0], p[1], p[2])
        release = "v{0}".format(version)
        branch = "release_{0}".format(release)
        return (version, release, branch)
