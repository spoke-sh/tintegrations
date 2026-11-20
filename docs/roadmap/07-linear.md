# 7. Linear

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Linear state/dataflow model](integration-state-models.md#linear).

Let applications synchronize engineering work and submit explicit issue transitions to Linear.
Planned package root: `integrations/linear/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with teams, projects, issues, workflow states, labels, and comments. Include selected issue creation/updates, comments, and webhook-driven refresh.

Use a selected Linear OAuth profile over qualified shared OAuth machinery. Bind the workspace and actor mode; do not treat a personal API-key profile as interchangeable with app authorization.

Agent-specific APIs, broad project administration, file uploads, and generic arbitrary GraphQL execution are deferred.

Provider basis: [GraphQL API](https://linear.app/developers/graphql), including its linked OAuth, pagination, rate-limit, and webhook contracts.

## Delivery sequence

1. Pin a GraphQL schema basis and implement bounded queries for the selected resources and connections.
2. Implement selected mutations and webhook intake with typed partial/error outcomes and durable reconciliation.
3. Provide a work-item synchronization example with explicit remote/local field ownership.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise GraphQL partial results, schema drift, invalid state transitions, rate/complexity limits, and duplicate notifications.
- Show that retries preserve mutation uncertainty and do not erase newer issue state.

