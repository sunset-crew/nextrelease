#!/bin/bash

git remote add github git@github.com:sunset-crew/nextrelease.git
CURRENT=$(git rev-parse --abbrev-ref HEAD) && git checkout main && git push github && git push --tags github && git checkout ${CURRENT}
git remote remove github
