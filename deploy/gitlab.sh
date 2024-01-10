#!/bin/bash


CURRENT=$(git rev-parse --abbrev-ref HEAD) && git checkout main && git push gitlab && git checkout ${CURRENT}
