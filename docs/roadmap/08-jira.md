# 8. Jira Cloud

[Roadmap](README.md) · **Status:** Planned

Let applications track and update Jira work using each project's actual fields and workflow transitions.
Planned package root: `integrations/jira/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with projects, issues, issue types/field metadata, comments, and available transitions. Include bounded search, selected issue creation/updates/transitions, and selected change intake.

Select and qualify a Jira Cloud OAuth profile with explicit site and project scopes. Reuse qualified OAuth machinery without making Jira-specific schema/workflow behavior a shared protocol concern.

Jira Data Center, Service Management, project/workflow administration, and arbitrary plugin field coverage require separate profiles.

Provider basis: [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/).

## Delivery sequence

1. Map project-specific fields and transition requirements, distinguishing missing values from inaccessible data.
2. Implement bounded reads/search and selected writes with typed validation/conflict outcomes.
3. Add webhook-assisted reconciliation and an example that mirrors an issue and requests an allowed transition.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise changed custom fields, invalid transitions, lost permissions, search pagination changes, and uncertain writes.
- Demonstrate site isolation and that a webhook cannot authorize a transition the connection cannot perform.

