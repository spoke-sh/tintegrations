# 3. GitHub

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[GitHub state/dataflow model](integration-state-models.md#github).

Let applications track repository work and coordinate issue workflows using durable GitHub observations and commands.
Planned package root: `integrations/github/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with repository, issue, pull-request, and issue-comment reads; issue creation/updates and issue comments; and selected issue/pull-request webhook events. Pull-request merging and repository administration are excluded.

Start with user OAuth through the candidate tpackages oauth-github public entry, subject to its compiler/protocol qualification. Bind each connection to its authorized repository scope. GitHub App installation authentication is a separate later profile.

Git transport, Actions execution, branch protection, organization administration, and GitHub Enterprise Server qualification are later work.

Provider basis: [Repository API](https://docs.github.com/en/rest/repos/repos), [issues](https://docs.github.com/en/rest/issues/issues), [pull requests](https://docs.github.com/en/rest/pulls/pulls), and [webhook practices](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks).

## Delivery sequence

1. Implement typed repository/work-item identities and paginated reads, preserving the distinction between issues and pull requests.
2. Add issue/comment commands and authenticated webhook intake with delivery deduplication, resource refresh, and resumable checkpoints.
3. Provide a repository work-tracking example that consumes changes and performs an explicitly selected issue update.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise repository access loss, transferred/deleted resources, duplicate deliveries, pagination changes, throttling, and uncertain comment creation.
- Show that webhook redelivery does not duplicate committed work and that another connection cannot read or mutate the first connection's repositories.

