# 2. Stripe

[Roadmap](README.md) · **Status:** Planned

Let applications connect customer billing records to Transit workflows and observe checkout and subscription outcomes.
Planned package root: `integrations/stripe/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with customer reads/creation/updates, product and price reads, Checkout Session creation/retrieval, subscription and invoice reads, and selected checkout/billing events. Keep resource access, event intake, and synchronization separately selectable.

Use an explicitly bound Stripe account and protected API-key reference. Keep test and live account state separate. Pin the API version and event payload profile before implementing fixtures; OAuth/Connect is a later profile.

Connect, payouts, refunds, direct card handling, tax calculation, and a general billing-policy engine are outside this first profile.

Provider basis: [Checkout Sessions](https://docs.stripe.com/api/checkout/sessions), [subscriptions](https://docs.stripe.com/api/subscriptions), [webhooks](https://docs.stripe.com/webhooks), and [idempotent requests](https://docs.stripe.com/api/idempotent_requests).

## Delivery sequence

1. Implement typed resource mappings and paginated reads, then customer and Checkout Session commands with recorded operation identity.
2. Implement native Stripe signature verification and durable event intake. Reconcile selected billing events against remote resources before publishing application-facing state.
3. Add a checkout-to-billing-state example with resumable reconciliation. Application entitlement and fulfillment policy remain with the consumer.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise duplicate/out-of-order events, invalid signatures, transient failures, lost write replies, and retry behavior within the selected endpoint's idempotency contract.
- Show account isolation and restart recovery without creating an extra customer/session or regressing newer observed state.

