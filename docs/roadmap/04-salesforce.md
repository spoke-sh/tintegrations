# 4. Salesforce

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Salesforce state/dataflow model](integration-state-models.md#salesforce).

Let applications synchronize selected sales records and submit traceable CRM updates without flattening organization-specific schemas.
Planned package root: `integrations/salesforce/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with Accounts, Contacts, Leads, and Opportunities: metadata/field discovery, bounded queries, record reads, and selected create/update/upsert commands. Use resumable polling/reconciliation for the initial synchronization profile.

Use an explicitly selected Salesforce OAuth application/grant profile, composing qualified tpackages OAuth machinery where applicable. Bind the organization, instance destination, API version, and allowed objects/fields to each connection.

Bulk APIs, Change Data Capture/Pub/Sub, metadata deployment, arbitrary custom-object coverage, and automatic conflict resolution are later profiles.

Provider basis: [REST API overview](https://developer.salesforce.com/docs/platform/api-rest/guide/intro-what-is-rest-api.html) and [REST resources](https://developer.salesforce.com/docs/platform/api-rest/guide/intro-rest-resources.html).

## Delivery sequence

1. Freeze the initial object/field contract and map provider identifiers, relationships, validation errors, and omitted/inaccessible fields.
2. Implement paginated query/read operations and record commands with caller-specified field ownership and conflict policy.
3. Implement bounded reconciliation with durable progress and an example that connects an application customer to a selected CRM record.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise field/object permission denial, schema changes, validation failures, expired continuation state, and partial reconciliation.
- Demonstrate organization isolation and lost-response recovery without treating an upsert key as proof that every business effect executes once.

