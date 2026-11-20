set shell := ["bash", "-euo", "pipefail", "-c"]

# List repository tasks.
default:
    @just --list

# Compile one implemented integration through its public entry point.
build integration:
    transit build -f {{ quote("integrations/" + integration + "/build.transit") }}

# Check formatting and build/test the isolated bootstrap with the pinned tools.
check:
    nix flake check --no-update-lock-file --print-build-logs

# Format repository tooling; the pinned CLIs have no Transit source formatter.
fmt:
    nixfmt flake.nix
    just --fmt

# Run one integration's Transit contract tests.
test integration:
    transit test -f {{ quote("integrations/" + integration + "/build.transit") }} --target tests
