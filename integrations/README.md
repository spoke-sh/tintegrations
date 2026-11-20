# Integration conventions

Each `integrations/<name>/` directory is an independent Transit package root for
one service. Use lowercase kebab-case names, such as `stripe`, `github`,
`salesforce`, and `hubspot`. The [roadmap catalog](../docs/roadmap/README.md#milestone-sequence-and-initial-catalog)
owns the initial integration list and delivery status. No service integrations
are implemented yet.

## Package structure

```text
integrations/<name>/
  README.md
  build.transit
  src/
  tests/
  examples/
```

`build.transit` is the public entry point. It should expose the supported modules,
a `default` build target, and a `tests` test target. Keep examples and tests rooted
through this entry so their imports stay within the package. Implementation files
under `src/` are private to the integration.

Document supported API versions, resources and operations, authentication,
required scopes, configuration, public modules, dependencies, and compatibility
with the pinned Transit tools. Include a minimal consumer example and distinguish
implemented behavior from planned behavior and compiler/runtime blockers.

## Dependency boundaries

Service APIs, resource mappings, provider-specific pagination and rate limits,
webhook handling, synchronization, and domain workflows belong here. Reusable
protocol machinery belongs in `tpackages`; execution, durable state, secrets, and
transport capabilities belong in Transit. Application business policy belongs
with the consumer.

Consumers pin a repository revision and select specific integration roots and
public modules. Do not require a root entry that imports every integration.
Optional resource families, webhook endpoints, and background synchronization
should be selected explicitly rather than activated merely by importing a client.

Depend on public `tpackages` entries at an explicit revision. Do not embed sibling
checkout paths such as `../../tpackages`, import another package's private `src/`,
or make unrelated integrations depend on one another for convenience. Any future
workspace dependency resolver must preserve the selected revision and transitive
dependency closure outside this checkout.

## Adding an integration

1. Start from its [roadmap milestone](../docs/roadmap/README.md), create the package
   root, and document the initial service/API scope.
2. Implement its public entry, Transit modules, deterministic contract tests, and
   a minimal consumer composition.
3. Run `just build <name>` and `just test <name>` in the development shell. Add the
   integration's checks to the flake/CI when its implementation is executable.
4. Verify a consumer can select it without loading unrelated integrations, and
   record any compiler/runtime gaps explicitly.

Keep provider network calls and credentials out of the default checks. Tests
should cover the supported contract, including provider errors, pagination,
retries/idempotency, and webhook replay where relevant. Live qualification can be
separate and opt-in. The repository bootstrap checks only the toolchain; it does
not qualify any service behavior.
