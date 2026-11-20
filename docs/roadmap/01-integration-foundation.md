# 1. Integration workspace and shared contracts

[Roadmap](README.md) · **Status:** In Progress

Let applications select independent service integrations from one pinned
repository revision, compose their public Transit modules, and inspect durable
operation and synchronization outcomes.

## Prerequisites and scope

Follow the [integration conventions](../../integrations/README.md). Transit owns
execution, state, secrets, transports, and effects; transitc owns source/build
semantics; `tpackages` owns reusable protocol implementations. This milestone
defines the integration composition contract and records upstream gaps rather
than implementing a replacement compiler, resolver, or runtime here.

The [flake](../../flake.nix) and [lock](../../flake.lock) define the executable
baseline. The pinned compiler lacks the workspace and lazy-export syntax used
by `tpackages`. The standalone transitc pin supplies CLI scaffolding; current
builds/tests use `transit build` and `transit test`. Reassess these facts when
upgrading pins; upstream source plans are not evidence of executable support.

## Delivered scope

- Pinned development shell, formatter, direnv setup, Just commands, and CI.
- Independent `integrations/<name>/` package conventions.
- [Bootstrap fixture](../../tests/bootstrap/build.transit) for module composition,
  instance isolation, fresh test state, and duplicate-key refusal.

The bootstrap passed on x86_64 Linux when the repository was initialized; all
four declared platform definitions evaluated. This establishes the bootstrap
subset, not external effects, service APIs, or selective workspace resolution.

## Delivery sequence

The proposed [implementation plan](integration-implementation-plan.md) and
[provider models](integration-state-models.md) make the resource ownership,
dataflow transitions, native capability gates, and review units concrete. They
are design artifacts; executable acceptance remains open.

1. Define public client/resource modules, explicit account/tenant bindings,
   selected read/write capabilities, and optional webhook/synchronization modules.
   Imports alone must not activate endpoints or background work.
2. Define typed operation outcomes, stable remote identifiers, pagination and
   checkpoint semantics, bounded requests, cancellation, and retry/reconciliation
   policy. Preserve unknown remote outcomes after lost replies; do not promise
   remote rollback or universal exactly-once delivery.
3. Compose protocol dependencies through public `tpackages` entries at explicit
   revisions. Verify provider-specific protocol profiles before reuse; providers'
   native webhook signatures do not automatically implement Standard Webhooks.
4. Record minimal compiler/runtime probes and actionable upstream requirements
   for protected credentials, durable effects, checkpoint recovery, selected
   exports, and independent consumer resolution. Source authoring can proceed
   while these gates remain open; record blocked execution explicitly.
5. Add the root workspace manifest and per-integration CI checks as executable
   integrations arrive. Prove an external consumer selects just its requested
   integration and transitive dependencies without sibling checkout paths.

## Completion evidence

- Build and test an independently rooted consumer at exact repository and
  toolchain revisions; verify its dependency/output closure excludes unrelated
  integrations and unselected optional modules.
- Run two instances with separate account/tenant bindings and demonstrate state,
  credential, and checkpoint isolation.
- Demonstrate bounded reads, denied writes, duplicate work, lost responses, and
  restart recovery through the selected integration's actual public entry.
- Keep default checks deterministic and credential-free. Record live provider
  verification separately, with the exact API/authentication profile and limits.
- Document the executable contract and remaining unsupported profiles beside
  the integration. Bootstrap-only success cannot close this milestone.
