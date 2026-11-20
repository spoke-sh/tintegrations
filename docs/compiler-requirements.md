# Integration execution requirements

The first implementation gate is **blocked on the pinned compiler surface**.
The repository can compile public Queue-driven Table/Stream programs, but cannot
yet compile the Document/KV state, command admission, private resources, and HTTP
effects needed for the first Stripe workflow. This affects every integration's
full profile. No service integration is implemented or qualified by this work.

The [implementation plan](roadmap/integration-implementation-plan.md#native-capability-and-compiler-gates)
requires a first working Stripe workflow before spreading implementations across
the catalog. Keep that gate open. Source-only wrappers or a second host runtime
would not establish the required behavior. An upstream implementation or a
separately qualified toolchain update is needed to continue that workflow.

## Reproduce the evidence

The probes were run on x86_64 Linux on 2026-11-19 (America/Los_Angeles), with:

- Transit `c1f2680d9353175e58ad503e750e7b4da76a84c5`.
- transitc `61536eaa510e2ba8826c08b4f41072ed66f41ed5`.
- Diagnostic definition `06091bff7096eeaceb3fc0d62bc0aa0d1bc184b20c3b275df74e8c93bf8b13e5`.

```sh
nix develop --no-update-lock-file -c just contracts
nix develop --no-update-lock-file -c just probes
```

`contracts` executes native tests. `probes` runs each source through native
`transit build --check --format json --color off` and writes
`.transit/reports/compiler-probes.json`. **It exits nonzero when any probe fails.**
There are no expected-failure exceptions. The report distinguishes compilation
from runtime tests and provider verification, neither of which a build proves.
Missing tools, timeouts, and process crashes also fail the command.

The [recorded probe report](evidence/compiler-probes-2026-11-19.json) includes
exact commands, declared pins, executable path, source hashes, exit codes, and
unmodified native output. It records one compiled probe and ten failed builds.
Use the Nix shell to bind the executable to the declared pins; running the Python
script with another `transit` on PATH does not qualify that toolchain.

## Native admission contract

The [contract suite](../tests/contracts/build.transit) exercises the existing
TABLE, QUEUE, STREAM, and Queue-input DATAFLOW profile. Its intended invariants
are one durable work item per accepted operation, conflict refusal, atomic
rollback, and independent instance state. The [fixture notes](../tests/contracts/README.md)
define its limits. Runtime results are recorded separately from compiler probes;
a later runtime assertion failure must remain a failure, never a compiler gap.

The final [native admission report](evidence/admission-2026-11-19.json) records
`TestDeadline` at the first admission workflow assertion; the remaining five
cases did not run. This suite is **not qualified**. Earlier diagnostic runs
sometimes completed the first case but did not complete the suite. The final
fixture separates construction, authorization, and activation and uses distinct
delivery inputs when reusing a logical operation ID.

As a control, the unchanged
[upstream Queue fixture](https://github.com/spoke-sh/transit/tree/c1f2680d9353175e58ad503e750e7b4da76a84c5/tests/fixtures/application-queue-programs)
was copied from the pinned Transit revision into `.transit/upstream-queue/` and
run with `transit test -f .transit/upstream-queue/build.transit --target tests
--format json --color off` in this repository's Nix shell. Its
[native report](evidence/upstream-queue-2026-11-19.json) also records
`TestDeadline` at `commits and refusals`; the second case did not run.
Both reports retain native source digests and locations. The cause has not been
isolated between the pinned runtime, test host, and local environment; this is
not evidence that all Queue programs fail or that an upstream defect is proven.

`just check` continues to check formatting, the evidence recorder, and the
existing bootstrap. It does not include or stand in for the failing
`just contracts` and `just probes` qualification gates. Both commands retain
their nonzero exit status and must pass, followed by deeper capability tests,
before provider implementation is qualified. No runtime failure is allowlisted.

## Required upstream work

Locations below refer to each probe's `root/build.transit`. A refusal at a
declaration does not establish whether any later expression or operation works.
The IDs correspond to the source requirements in the
[reviewed tpackages ledger](https://github.com/spoke-sh/tpackages/blob/2e80f2ce3b7828844efc2c35fb7abcd43ad42a17/docs/compiler-requirements.md).

| Gate | Probe | First result | Required next evidence |
| --- | --- | --- | --- |
| Native Queue program | [queue-program](../tests/compiler/queue-program/build.transit) | Build check passed; no activation or runtime test in this probe. | Execute the separate admission contract suite and retain its limits. |
| Command admission — TP-16 | [command](../tests/compiler/command/build.transit) | `InvalidSourceTemplate`, parse, 2:37. | Typed command binding, original request identity, and durable admission. |
| Versioned state — TP-10 | [document](../tests/compiler/document/build.transit) | `RuntimePrivateOrUnsupportedDeclaration`, compile, 2:17. | Document write/read revisions and guarded acceptance. Direct SQL support is a separate surface. |
| Receipt claims — TP-11 | [kv](../tests/compiler/kv/build.transit) | `RuntimePrivateOrUnsupportedDeclaration`, compile, 2:17. | Conditional point claims, contention, and retained receipt identity. |
| Mixed transaction — TP-12 | [mixed-state](../tests/compiler/mixed-state/build.transit) | Document declaration refuses, compile, 3:17. | One decision across all selected resources and native input settlement; rollback and restart tests. |
| Recorded HTTP — TP-06 | [effects](../tests/compiler/effects/build.transit) | `RuntimePrivateOrUnsupportedDeclaration`, compile, 2:10. | Bound credentials, captured attempts/responses, uncertainty, observe-only replay, and transactional acceptance. |
| Private state — TP-04 | [private](../tests/compiler/private/build.transit) | `RuntimePrivateOrUnsupportedDeclaration`, compile, 2:10. | Enforced encapsulation, current authority, stable account bindings, and cross-instance denial. |
| Required consumers — TP-13 | [stream-input](../tests/compiler/stream-input/build.transit) | `InvalidSourceTemplate`, parse, 4:39. | Stream input, native checkpoints committed with effects on local state, retention and replay. |
| Maintenance — TP-15 | [timer](../tests/compiler/timer/build.transit) | `InvalidSourceTemplate`, parse, 3:39. | Native timed activation, bounded cleanup/renewal, and current authority checks. |
| Lazy exports — TP-02 | [exports](../tests/compiler/exports/build.transit) | `InvalidSourceSyntax`, parse, 1:24. | Select one public module without loading unrelated resources, examples, or tests. |
| Workspace — TP-01 | [workspace](../tests/compiler/workspace/build.transit) | `UnsupportedBuildStatement`, compile, 1:1. | Independently fetched roots, pinned public protocol dependencies, and offline selected closure. |

The proposed syntax follows the reviewed tpackages target-language contract;
these files are minimal requirements, not an assertion that the current grammar
accepts them. Do not replace private state with public service Tables, versioned
Documents with JSON Tables, or native queues/checkpoints with application leases
to bypass these gates. Keep runtime/compiler changes in their owning repositories.

## Resume implementation

1. Qualify an upstream pair against these exact probes and re-run the admission
   suite. Record new results without changing a failure into a passing exception.
2. After declarations compile, add tests for revision/claim contention and mixed
   transaction recovery. Compiler acceptance alone does not close those gates.
3. Implement Stripe's customer/Checkout/event-to-billing workflow, including
   protected effects and a required consumer. Exercise lost replies, duplicate
   events, stale refreshes, and account revocation through its actual public entry.
4. Qualify GitHub's OAuth composition and dependency selection. Continue the
   remaining provider profiles in the [delivery sequence](roadmap/integration-implementation-plan.md#delivery-units).

This evidence does not close the foundation milestone, alter any provider's
status, or claim that the 18-integration implementation is complete.
