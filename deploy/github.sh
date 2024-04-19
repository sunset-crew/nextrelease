#!/bin/bash


CURRENT=$(git rev-parse --abbrev-ref HEAD) && git checkout main && git push github && git push --tags github && git checkout ${CURRENT}
