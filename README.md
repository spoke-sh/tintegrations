# tintegrations

Officially maintained integrations for [Transit](https://github.com/spoke-sh/transit).
This monorepo owns service-specific clients, resource mappings, synchronization,
and workflows for products such as Stripe, GitHub, Salesforce, and HubSpot.

[`tpackages`](https://github.com/spoke-sh/tpackages) provides reusable protocol
implementations and provider adapters. Integrations compose those packages where
appropriate: for example, `oauth-github` handles GitHub authorization, while a
GitHub integration works with repositories, issues, and pull requests.

## Layout and consumption

All maintained integrations belong directly under `integrations/<name>/`, using
lowercase kebab-case names:

```text
docs/
  roadmap/           numbered delivery milestones and integration catalog
integrations/
  README.md          shared integration conventions
  <name>/
    README.md        supported operations, configuration, usage, and status
    build.transit    public entry point and build/test targets
    src/             implementation modules
    tests/           integration contract tests and fixtures
    examples/        minimal consumer compositions
tests/
  bootstrap/         executable toolchain smoke fixture
```

The [roadmap](docs/roadmap/README.md) defines the initial catalog of 18 integrations,
their delivery order, scope, and completion criteria. It begins with Stripe,
GitHub, Salesforce, and HubSpot, then extends to engineering, collaboration,
knowledge, productivity, support, and commerce services.
This bootstrap contains development tooling and conventions; no service
implementations are included yet. See [integration conventions](integrations/README.md)
before adding the first one. The [documentation index](docs/README.md) links the
owning guides and plans.

The consumer model follows `tpackages`: pin one repository revision, select the
integration subdirectories needed by the application, and import their public
entries. Only selected integrations and their transitive dependencies should enter
the application. Sharing a workspace does not make every integration a dependency.
Dependencies on `tpackages` must also select explicit packages at a pinned revision.

The pinned compiler does not yet support the workspace and lazy-export syntax
used by `tpackages`. There is no root workspace manifest until integrations are
added and the required compiler support is established. Build/test commands
operate on individual integration entries; selective downstream consumption is a
design requirement to verify when implementations arrive.

## Development

With Nix and flakes enabled:

```sh
nix develop
just
just check
just fmt
```

The shell provides the upstream `transit` and `transitc` executables, Git, Just,
and nixfmt. `.envrc` enables optional direnv support. No sibling checkout is
required.

| Command | Behavior |
| --- | --- |
| `just` | List available tasks. |
| `just check` | Run Nix/Just formatting checks and the bootstrap build/tests in the Nix sandbox, keeping the lock unchanged. |
| `just build <name>` | Build `integrations/<name>/build.transit`. Requires an implemented integration. |
| `just test <name>` | Run the selected integration's `tests` target. |
| `just fmt` | Format `flake.nix` and `justfile`. |

`nix flake check --no-update-lock-file --print-build-logs` runs the same checks
directly. The bootstrap verifies module composition, independent instances,
isolated test state, and duplicate-key refusal. It needs no provider credentials
or running server. Nix may fetch or build dependencies on first use.

The pinned standalone `transitc` is a CLI scaffold; compilation and tests use
`transit build` and `transit test`, matching `tpackages`. Passing the bootstrap
does not establish support for future service integrations.

## Upstream pins

`flake.nix` pins Transit and transitc to the same revisions used by the initial
`tpackages` environment. `flake.lock` records their content hashes and transitive
inputs; nixpkgs follows Transit's pin. The flake declares x86_64 and aarch64 Linux
and Darwin, matching both upstreams. Checks establish support on the platform
where they run.

To upgrade, change the relevant full commit hash in `flake.nix`, run
`nix flake lock`, review both files, and re-run `nix develop --command just check`
plus the build/tests for each implemented integration.
