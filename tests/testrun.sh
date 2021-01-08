#!/bin/bash

#APPNAME=$1

APPNAME='testrepo'

pyproject_file(){
    cat <<EOT > pyproject.toml
[tool.poetry]
name = "${APPNAME}"
version = "0.1.0"
description = "This is a test Repo"
authors = ["Joe <joe@testing.local>"]

[tool.poetry.dependencies]
python = "^3.7"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
EOT
}

#cd tests
[ -d "${APPNAME}" ] && rm -rf ${APPNAME}
mkdir ${APPNAME}
# cp testrepo.tar.gz
cd ${APPNAME}
pyproject_file
# tar xzvf testrepo.tar.gz 
git init
git add . 
git commit -a -m"initial commit"
git nextrelease --no-remote
git versionupdater install
git changelog install
git changelog adds versioninstaller and changelog
echo "new_file=1" > newfile.sh
git changelog adds newfile.sh
git checkout master
git merge release_v0.1.0 --commit
echo "new_file=2" > newfile.sh
git add . 
git commit -a -m"Merge branch 'release_v0.1.0' into 'master'"
git aftermerge patch --no-remote
cd .. 
[ -d "${APPNAME}" ] && rm -rf ${APPNAME}
