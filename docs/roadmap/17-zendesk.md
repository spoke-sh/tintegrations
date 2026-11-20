# 17. Zendesk

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Zendesk state/dataflow model](integration-state-models.md#zendesk).

Let applications track support cases and submit explicit ticket updates with inspectable outcomes.
Planned package root: `integrations/zendesk/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with tickets, users, organizations, comments, selected ticket create/update/assignment commands, and change reconciliation. Treat public replies and internal notes as distinct operations.

Qualify a Zendesk OAuth profile, service subdomain, and allowed ticket scope. Compose shared OAuth machinery and retain the actor and account context for each command.

Guide, Talk, workforce management, broad account administration, and automatic support-policy decisions are deferred.

Provider basis: [Zendesk Ticketing API](https://developer.zendesk.com/api-reference/ticketing/introduction/).

## Delivery sequence

1. Map ticket status/assignment, custom fields, requesters, and comment visibility.
2. Implement bounded reads and selected ticket/comment commands with provider-specific validation and retry rules.
3. Add incremental reconciliation and a support-case example with durable operation state.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise concurrent updates, invalid field/status changes, private-note disclosure, access loss, and duplicate change delivery.
- Demonstrate that an uncertain public reply is not blindly posted again and that ticket creation respects the selected idempotency contract.

