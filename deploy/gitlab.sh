#!/bin/bash


CURRENT=$(git rev-parse --abbrev-ref HEAD) && git checkout main && git push gitlab && git push --tags gitlab && git checkout ${CURRENT}
