# 16. Airtable

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Airtable state/dataflow model](integration-state-models.md#airtable).

Let applications map selected Airtable records to typed Transit data and synchronize explicit field changes.
Planned package root: `integrations/airtable/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with base/table/field metadata, bounded record lists, selected record create/update/upsert operations, and change reconciliation for configured tables.

Choose and qualify an OAuth app profile with explicit base scopes. Credential references and base/table bindings remain distinct from consumer business identity.

Base/schema administration, scripting/automations, unrestricted formula execution, and complete spreadsheet semantics are deferred.

Provider basis: [Airtable Web API](https://airtable.com/developers/web/api/introduction).

## Delivery sequence

1. Map provider field/record IDs, supported cell types, linked records, and computed/read-only fields.
2. Implement bounded reads and selected record writes with per-record outcomes and explicit source-of-truth policy.
3. Add checkpointed reconciliation and a table workflow example that survives field renames.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise changed field types, renamed fields, linked-record dependencies, missing values, partial batch failures, and access loss.
- Prove retries preserve uncertain create outcomes and the consumer does not treat computed fields as writable.

