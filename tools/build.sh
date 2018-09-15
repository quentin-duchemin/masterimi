#!/bin/bash
set -o nounset
set -o errexit
set -o xtrace
set -o pipefail

echo "CHecking if we are on master branch"
test "$(git rev-parse --abbrev-ref HEAD)" = "master"

echo "Checking if local changes on tracked files"
test -z "$(git status --porcelain --untracked-files=no)"

echo "Checking if all local commits are pushed to origin"
test "$(git rev-parse @{u})" = "$(git rev-parse HEAD)"

docker-compose -f docker-compose.yml -f build.override.yml build
docker-compose -f docker-compose.yml -f build.override.yml push
