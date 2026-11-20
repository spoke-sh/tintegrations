# 15. Microsoft Teams

[Roadmap](README.md) · **Status:** Planned

Let applications observe selected team conversations and publish attributable workflow messages.
Planned package root: `integrations/microsoft-teams/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with teams, channels, selected chats/messages/replies, and the read/post operations supported by the chosen permission profile. Add change notifications and reconciliation only for explicitly qualified resource subscriptions.

Qualify a Microsoft identity OAuth profile and the permission mode for each Graph operation. Do not infer send rights from read access or from a different delegated/application permission mode.

Calls, meetings/media capture, tenant administration, message import/migration, and a full bot/UI framework are deferred.

Provider basis: [Microsoft Teams APIs in Graph](https://learn.microsoft.com/en-us/graph/teams-concept-overview).

## Delivery sequence

1. Freeze a resource/permission matrix and implement bounded team/channel/conversation reads.
2. Implement permitted message commands and notification validation/subscription lifecycle with resumable refresh.
3. Provide a selected-channel workflow example using an independent Teams package.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise membership removal, unsupported permission modes, subscription expiry, duplicate notifications, and uncertain message posts.
- Show Teams-only consumers require no Outlook mail/calendar modules and that expired authority stops new effects.

