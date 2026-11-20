set shell := ["bash", "-euo", "pipefail", "-c"]

# List repository tasks.
default:
    @just --list

# Compile one implemented integration through its public entry point.
build integration:
    transit build -f {{ quote("integrations/" + integration + "/build.transit") }}

# Check formatting, evidence tooling, and the isolated bootstrap (not service qualification).
check:
    nix flake check --no-update-lock-file --print-build-logs

# Run native admission conformance; unresolved runtime failures remain failures.
contracts:
    transit test -f tests/contracts/build.transit --target tests

# Format repository tooling; the pinned CLIs have no Transit source formatter.
fmt:
    nixfmt flake.nix
    just --fmt

# Record native compiler acceptance; any failed probe fails this command.
probes:
    python3 tooling/probe.py

# Run one integration's Transit contract tests.
test integration:
    transit test -f {{ quote("integrations/" + integration + "/build.transit") }} --target tests
