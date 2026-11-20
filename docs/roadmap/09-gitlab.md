# 9. GitLab

[Roadmap](README.md) · **Status:** Planned

Let applications follow project issues and merge requests and coordinate selected GitLab work-item updates.
Planned package root: `integrations/gitlab/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with GitLab.com projects, issues, merge-request reads, notes, selected issue/note writes, and project webhook intake.

Qualify one GitLab OAuth connection profile with explicit project access. Bind the service origin and account; self-managed instance support needs its own version/destination qualification.

Self-managed deployments, pipeline execution, merge commands, repository administration, and Git transport are later profiles.

Provider basis: [GitLab REST API](https://docs.gitlab.com/api/rest/), including its linked authentication and webhook references.

## Delivery sequence

1. Map project/work-item identities and bounded resource lists through the selected REST API profile.
2. Implement issue/note commands, provider-specific webhook authentication, and durable refresh/checkpoint handling.
3. Provide a project work-tracking example without requiring the GitHub integration.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise project membership loss, duplicate webhook deliveries, renamed/transferred projects, throttling, and lost note replies.
- Show the selected dependency graph excludes GitHub and that replay does not resend external writes.

