# 10. Notion

[Roadmap](README.md) · **Status:** Planned

Proposed implementation: [shared plan](integration-implementation-plan.md) and
[Notion state/dataflow model](integration-state-models.md#notion).

Let applications work with selected shared knowledge resources and maintain attributable local projections.
Planned package root: `integrations/notion/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with authorized pages, block trees, database/data-source schemas and queries, selected page-property updates, and bounded block appends. Define the selected API version's resource model explicitly.

Select a Notion connection/authentication profile and version header. Limit access to resources shared with that connection; shared OAuth logic does not grant workspace-wide access.

Complete editor fidelity, arbitrary rich-media uploads, workspace administration, and a universal document renderer are deferred.

Provider basis: [Notion API introduction](https://developers.notion.com/reference/intro) and its linked versioning, authentication, and pagination references.

## Delivery sequence

1. Map the supported property/block types and bound recursive traversal, pagination, and result sizes.
2. Implement selected page/property/block commands and explicit polling/reconciliation with durable progress.
3. Provide a structured-page synchronization example that retains unsupported-content markers rather than dropping unknown blocks.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise revoked page sharing, schema/property changes, deep block trees, unsupported block types, and interrupted pagination.
- Preserve uncertain append outcomes after lost replies; do not blindly append the same content again.

