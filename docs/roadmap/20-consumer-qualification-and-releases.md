# 20. Consumer qualification and releases

[Roadmap](README.md) · **Status:** Planned

Publish a reproducible integration collection that applications can consume in
small subsets, with explicit compatibility and recovery evidence.

## Prerequisites and scope

The [foundation](01-integration-foundation.md) and the service milestones in the
[initial catalog](README.md#milestone-sequence-and-initial-catalog) supply their
own completion evidence. This milestone verifies the combined 18-integration
catalog at one source revision; it does not postpone each integration's tests.
An earlier release may include only completed profiles and must name that subset.

Use the proposed [implementation validation matrix](integration-implementation-plan.md#validation-and-state-evolution)
and [provider state/dataflow models](integration-state-models.md) to qualify
native transitions, selected dependency closure, and recovery across the catalog.

Initially version the collection by one exact Git revision per consumer, with
explicit protocol dependency and toolchain pins. Independent package selection
does not require independent release trains or a package registry.

## Delivery sequence

1. Add independently rooted consumers for every integration, selected pairs, and
   repeated account/tenant instances. Verify public import boundaries, optional
   module selection, dependency closure, and offline rebuilds from frozen inputs.
2. Run the recovery and failure matrix at the selected pins. Keep mock/fixture
   tests, native runtime tests, and live provider verification separately visible.
   Account for required test-account capabilities without using live customer data.
3. Exercise a source upgrade with explicit state/checkpoint migration and the
   declared compatibility policy. Pin changes and integration behavior changes
   need attributable results; a source update must not silently reset identity.
4. Publish the supported resource/authentication/API matrix, consumer examples,
   provenance, changelog, and upgrade guidance for the actual released subset.

## Completion evidence

- Every initial integration passes its own milestone and shared completion gates
  at the catalog's selected revisions, with evidence linked from its milestone.
- Clean consumers build without sibling checkouts; single-integration consumers
  load only their selected public modules and transitive dependencies.
- Combined consumers preserve independent authority, credential/state ownership,
  rate budgets, and recovery; one provider's outage does not erase another's progress.
- Offline build/replay checks make no provider calls. Unknown write outcomes stay
  visible through restart and migration instead of triggering blind retries.
- Published commands and examples run against the released artifacts; unsupported
  profiles and untested platforms remain explicit.
