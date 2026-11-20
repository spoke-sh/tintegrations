# 12. Google Calendar

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Google Calendar state/dataflow model](integration-state-models.md#google-calendar).

Let applications reconcile selected calendars and create or update events with explicit notification policy.
Planned package root: `integrations/google-calendar/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with calendar discovery, event reads, bounded recurrence expansion, free/busy reads, selected event creation/updates/cancellation, and incremental synchronization.

Compose qualified oauth-google behavior with Calendar-specific scopes and per-calendar bindings. Sharing an OAuth provider does not require the Drive or Gmail integrations.

Calendar administration, broad ACL management, resource provisioning, and a general scheduling optimizer are later work.

Provider basis: [Calendar API overview](https://developers.google.com/workspace/calendar/api/guides/overview).

## Delivery sequence

1. Map all-day/timed events, zones, attendees, recurring series, and exceptions without losing provider identities.
2. Implement selected event commands with explicit attendee-notification behavior and conflict handling.
3. Add incremental reconciliation and a scheduling example with recovery after invalid continuation state.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise daylight-saving boundaries, recurring exceptions, cancelled events, access loss, stale updates, and interrupted sync.
- Verify retry handling does not silently create a second meeting or imply that cancelling local work retracts invitations.

