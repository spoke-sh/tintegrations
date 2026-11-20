# 5. HubSpot

[Roadmap](README.md) · **Status:** Planned

Let applications maintain selected customer and deal records, their relationships, and inspectable synchronization progress.
Planned package root: `integrations/hubspot/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with Contacts, Companies, Deals, properties, pipelines, and associations. Include bounded reads/search, selected create/update commands, and webhook-assisted reconciliation for supported subscriptions.

Choose and qualify one public-app OAuth profile using shared tpackages OAuth machinery. Pin the selected API generation and app/webhook contract; do not assume all object events or account tiers expose identical capabilities.

Marketing campaigns, CMS, email automation, arbitrary custom objects, and broad workflow-authoring APIs are outside the initial profile.

Provider basis: [CRM model](https://developers.hubspot.com/docs/api-reference/legacy/crm/understanding-the-crm), [object APIs](https://developers.hubspot.com/docs/api-reference/legacy/crm/using-object-apis), and [webhooks](https://developers.hubspot.com/docs/api-reference/legacy/webhooks/guide). Recheck the provider's migration guidance when selecting the implementation profile.

## Delivery sequence

1. Map the selected object properties, record IDs, association types, and pipeline/stage identities with explicit missing-field behavior.
2. Implement bounded reads and record/association commands, preserving per-record errors and operation identity.
3. Add durable change intake and reconciliation, plus an example that tracks a customer through a selected deal stage.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise missing/custom properties, invalid associations, stage constraints, batch partial failures, and lost create replies.
- Demonstrate subscription deduplication, account isolation, and resumed reconciliation without claiming a consistent snapshot from search results.

