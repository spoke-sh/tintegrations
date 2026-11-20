# 6. Slack

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Slack state/dataflow model](integration-state-models.md#slack).

Let applications observe selected conversations and deliver durable, attributable workflow messages.
Planned package root: `integrations/slack/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with workspace/user/channel metadata, authorized conversation and thread reads, message posting/updating, and selected Events API subscriptions. Restrict ingestion to configured conversations.

Select a Slack app OAuth/bot profile, its scopes, and its installation/distribution mode. Reuse qualified OAuth protocol machinery; keep bot identity and workspace bindings explicit.

Enterprise administration, calls, broad workspace export, interactive UI frameworks, and Slack Connect coverage are later profiles.

Provider basis: [Web API](https://docs.slack.dev/apis/web-api/), including its linked Conversations, Events, authentication, and rate-limit guides.

## Delivery sequence

1. Map conversations, thread/message identities, and bounded history pagination without converting provider timestamps to floating-point identifiers.
2. Implement message commands and authenticated event intake with deduplication, retry budgets, and reconciliation.
3. Provide a channel workflow example with observable send state and resumable selected-conversation ingestion.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise channel removal, revoked scopes, history throttling, duplicate events, edits/deletes, and uncertain sends.
- Verify a retry cannot silently post a second message and that a disconnected workspace stops new work.

