# 14. Microsoft Outlook

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Microsoft Outlook state/dataflow model](integration-state-models.md#microsoft-outlook).

Let applications compose selected mail and calendar workflows through independently selectable Outlook modules.
Planned package root: `integrations/microsoft-outlook/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with mailbox folders/messages/drafts and calendars/events, bounded reads, selected draft/send and event commands, and change reconciliation. Mail and calendar modules must remain independently selectable.

Qualify a Microsoft identity OAuth profile through shared protocol machinery. Start with explicitly delegated mailbox/calendar access; record supported tenant/account types and each Graph operation's permission requirements.

Tenant administration, broad application-only mailbox access, archive mailbox support, and a complete Microsoft 365 integration are outside the first profile.

Provider basis: [Outlook mail](https://learn.microsoft.com/en-us/graph/outlook-mail-concept-overview) and [Outlook calendar](https://learn.microsoft.com/en-us/graph/outlook-calendar-concept-overview) API overviews.

## Delivery sequence

1. Map mail/calendar resources through a selected stable Microsoft Graph profile and preserve remote identity/conflict metadata.
2. Implement bounded reads and selected commands with separate mail-send and calendar-write capabilities.
3. Add resumable change reconciliation and independent mail-only and calendar-only consumer examples.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise tenant mismatch, scope revocation, changed resources, invalid continuation state, recurring-event exceptions, and uncertain sends.
- Show mail-only consumers require neither calendar activation nor the Microsoft Teams integration.

