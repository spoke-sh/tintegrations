# 13. Gmail

[Roadmap](README.md) · **Status:** Planned

Let applications process selected mailbox observations and issue traceable draft/send commands.
Planned package root: `integrations/gmail/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with messages, threads, labels, drafts, bounded message/attachment reads, selected label updates, draft creation, sending, and incremental history reconciliation.

Use qualified oauth-google behavior with explicitly selected mailbox scopes. Keep reading, modifying, and sending as separate selected capabilities and bind each mailbox independently.

Domain-wide administration/delegation, mailbox migration, forwarding rules, bulk campaigns, and unrestricted send-as identities are deferred.

Provider basis: [Gmail API overview](https://developers.google.com/workspace/gmail/api/guides).

## Delivery sequence

1. Map message/thread identity and bounded MIME/attachment handling using Transit facilities, with explicit content-size limits.
2. Implement draft/label/send commands and observable pending, accepted, failed, or unknown outcomes.
3. Add history-based reconciliation and a mailbox workflow example; push delivery infrastructure is a separate optional module/profile.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise expired history state, mailbox access loss, duplicate observations, oversized attachments, and lost send replies.
- Prove replay does not resend mail and provider acceptance is not reported as recipient delivery.

