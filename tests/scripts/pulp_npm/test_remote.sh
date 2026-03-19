#!/bin/bash

set -eu

# shellcheck source=tests/scripts/config.source
. "$(dirname "$(dirname "$(realpath "$0")")")/config.source"

ENTITIES_NAME="test_npm_remote"

cleanup() {
  pulp npm remote destroy --name "${ENTITIES_NAME}" || true
}
trap cleanup EXIT

# Fail to create some remotes:
expect_fail pulp npm remote create --name "foo"

# Create and a remote:
expect_succ pulp npm remote create --name "foo" --url "foo"
