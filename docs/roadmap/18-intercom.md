# 18. Intercom

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Intercom state/dataflow model](integration-state-models.md#intercom).

Let applications maintain customer conversation context and perform selected support workflow actions.
Planned package root: `integrations/intercom/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with contacts, companies, conversations, tags, assignment/status changes, replies, and internal notes. Include selected reads/writes and webhook-assisted reconciliation.

Qualify an Intercom OAuth application profile with explicit workspace and regional API destination bindings. Record the API version and required permissions for each operation.

Campaigns, broad Messenger customization, Fin/agent execution, help-center publishing, and workspace administration are deferred.

Provider basis: [Intercom REST API](https://developers.intercom.com/docs/references/rest-api/api.intercom.io).

## Delivery sequence

1. Map customer/conversation identity, participants, parts, assignment, and note/reply visibility.
2. Implement bounded reads and selected actions with durable attempt identity and explicit partial/error outcomes.
3. Add authenticated change intake and an example connecting a selected conversation to application customer state.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise changed contacts, conversation reassignment, duplicate events, regional destination mismatch, and lost reply responses.
- Show internal notes remain distinct from customer-visible messages and resumed processing does not duplicate external replies.

