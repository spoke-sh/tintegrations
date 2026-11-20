# 19. Shopify

[Roadmap](README.md) · **Status:** Planned

Let applications synchronize selected commerce records and perform bounded merchant workflow updates.
Planned package root: `integrations/shopify/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with products/variants, customers, orders, inventory/fulfillment status reads, selected product metadata and order-note/tag updates, and corresponding webhook-assisted reconciliation.

Qualify one Shopify app/token lifecycle with explicit shop and access scopes. Pin a stable GraphQL Admin API version and the required customer-data permissions before implementing fixtures.

Charging/refunds, fulfillment execution, checkout customization, theme management, broad inventory mutation, and a storefront framework are deferred.

Provider basis: [GraphQL Admin API](https://shopify.dev/docs/api/admin-graphql/latest). The implementation must pin an explicit supported version rather than the moving `latest` reference.

## Delivery sequence

1. Implement typed selected GraphQL queries, cursor pagination, and explicit query-cost/throttle handling.
2. Add selected mutations and signed webhook intake, preserving per-operation errors and shop identity.
3. Provide a commerce-status synchronization example with durable progress and explicit handling of removals/access loss.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise partial GraphQL errors, throttling, duplicate/out-of-order notifications, revoked shop access, and uncertain writes.
- Demonstrate shop isolation, checkpoint recovery, and separation between observed order status and application fulfillment decisions.

