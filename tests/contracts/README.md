# Native admission contract fixture

This suite exercises Transit's supported public TABLE/QUEUE/STREAM/DATAFLOW
profile through the pinned native test host. It is a test fixture, not a public
integration or an alternative implementation of the planned Document/KV model.

`admission.transit` commits an operation identity, one work item, and an accepted
outcome in one atomic block. Same-content redelivery observes the existing row;
conflicting reuse refuses. A test-only guard after all three writes exercises
rollback, and a second Queue dataflow observes the admitted work without making
network requests. Constructors declare resources; test setup explicitly grants
and activates them. The default build target leaves its dataflow inactive.

Account IDs, payload commitments, and the admission decision are test inputs.
They do not establish cryptographic commitments, actor authorization, private
storage, credentials, or provider account verification. The fixture does not
test Document/KV transactions, HTTP effects, crash/restart, required Stream
checkpoints, or provider behavior; those remain separate execution gates.

Delivery counters distinguish native input submissions while keeping the same
logical operation and commitment during redelivery. The work observer activates
only after admission assertions; the fixture does not qualify concurrent
downstream consumption. The current suite fails with a native `TestDeadline`;
its assertions have not established the intended invariants.

Run `nix develop --no-update-lock-file -c just contracts`. Every assertion must
pass as written; a runtime failure is never an accepted compiler diagnostic.
See [execution requirements](../../docs/compiler-requirements.md) for the
capability probes and recorded toolchain boundary.
