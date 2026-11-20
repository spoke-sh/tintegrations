# Roadmap

This roadmap tracks integration scope, delivery order, prerequisites, acceptance
criteria, and status. It follows the numbered milestone and status conventions in
[Transit's roadmap](https://github.com/spoke-sh/transit/blob/ff2bd9690765f33045f3156908ef538f7748b333/docs/roadmap/README.md#maintaining-the-sequence),
adapted to this repository. Order expresses implementation priority and explicit
prerequisites, not delivery dates or dependencies between unrelated services.

The initial catalog contains **18 integrations**. Stripe, GitHub, Salesforce, and
HubSpot form the first delivery phase; engineering, collaboration, knowledge,
productivity, support, and commerce integrations follow. All service integrations
are **Planned**. The repository currently contains development tooling and an
executable bootstrap fixture, with no service implementations.

Each integration is an independent root under `integrations/<name>/`. Consumers
select public modules at one pinned repository revision, plus explicit transitive
dependencies. A shared provider or delivery phase must not force installation of
unrelated integrations. In particular, Google services and Microsoft services
remain separately selectable; Outlook also separates mail and calendar modules.

## Delivery phases

| Phase | Milestones | Intended outcome |
| --- | --- | --- |
| I: Foundation and first integrations | 1–5 | Establish the consumer/effect contracts with Stripe, GitHub, Salesforce, and HubSpot. |
| II: Team workflows | 6–9 | Add Slack, Linear, Jira Cloud, and GitLab work/conversation workflows. |
| III: Knowledge and productivity | 10–16 | Add Notion, Google Drive, Google Calendar, Gmail, Outlook, Teams, and Airtable. |
| IV: Support and commerce | 17–19 | Add Zendesk, Intercom, and Shopify service workflows. |
| V: Consumer qualification | 20 | Verify the combined catalog's independent consumption, compatibility, recovery, and release evidence. |

Every integration must pass its own completion gates as it lands; the final
milestone combines that evidence at a single revision. Source authoring may
overlap once its contracts are clear, while executable support remains gated by
the relevant upstream capabilities. A later provider need not wait for an
unrelated provider's API work when its own prerequisites are satisfied.

## Milestone sequence and initial catalog

Roots below are planned paths, not existing implementations. Each service file
defines its initial operations, authentication profile, exclusions, and evidence.

| Order | Milestone | Integration root | Status | Initial outcome |
| --- | --- | --- | --- | --- |
| 1 | [Integration foundation](01-integration-foundation.md) | — | In Progress | Independent package selection, account bindings, durable outcomes, and upstream compatibility. |
| 2 | [Stripe](02-stripe.md) | `integrations/stripe/` | Planned | Customers, checkout, billing observations, and event reconciliation. |
| 3 | [GitHub](03-github.md) | `integrations/github/` | Planned | Repositories, issues, pull-request observations, comments, and change intake. |
| 4 | [Salesforce](04-salesforce.md) | `integrations/salesforce/` | Planned | Selected sales objects, field metadata, record operations, and reconciliation. |
| 5 | [HubSpot](05-hubspot.md) | `integrations/hubspot/` | Planned | Contacts, companies, deals, properties, associations, and change intake. |
| 6 | [Slack](06-slack.md) | `integrations/slack/` | Planned | Selected conversation reads, workflow messages, and event reconciliation. |
| 7 | [Linear](07-linear.md) | `integrations/linear/` | Planned | Teams, projects, issues, comments, and selected workflow mutations. |
| 8 | [Jira Cloud](08-jira.md) | `integrations/jira/` | Planned | Project-specific issue fields, comments, transitions, and reconciliation. |
| 9 | [GitLab](09-gitlab.md) | `integrations/gitlab/` | Planned | Projects, issues, merge-request observations, notes, and change intake. |
| 10 | [Notion](10-notion.md) | `integrations/notion/` | Planned | Selected pages, blocks, structured data, and bounded content updates. |
| 11 | [Google Drive](11-google-drive.md) | `integrations/google-drive/` | Planned | Files/folders, bounded content transfer, and change tracking. |
| 12 | [Google Calendar](12-google-calendar.md) | `integrations/google-calendar/` | Planned | Calendars, events, availability, and incremental synchronization. |
| 13 | [Gmail](13-gmail.md) | `integrations/gmail/` | Planned | Messages, threads, labels, drafts, explicit sends, and history reconciliation. |
| 14 | [Microsoft Outlook](14-microsoft-outlook.md) | `integrations/microsoft-outlook/` | Planned | Independently selected mail/calendar operations and change reconciliation. |
| 15 | [Microsoft Teams](15-microsoft-teams.md) | `integrations/microsoft-teams/` | Planned | Selected team/channel conversations, messages, and notifications. |
| 16 | [Airtable](16-airtable.md) | `integrations/airtable/` | Planned | Base/table metadata, typed record operations, and reconciliation. |
| 17 | [Zendesk](17-zendesk.md) | `integrations/zendesk/` | Planned | Tickets, customers, assignment, comments, and support-case synchronization. |
| 18 | [Intercom](18-intercom.md) | `integrations/intercom/` | Planned | Contacts, companies, conversations, replies/notes, and change intake. |
| 19 | [Shopify](19-shopify.md) | `integrations/shopify/` | Planned | Catalog/customer/order observations, selected metadata updates, and change intake. |
| 20 | [Consumer qualification and releases](20-consumer-qualification-and-releases.md) | — | Planned | Reproducible independent consumption, recovery evidence, and compatibility records. |

This catalog is the initial implementation scope, not a claim of complete
provider coverage. Add another integration through a scoped milestone with an
identified consumer use case; extend an existing service through explicit module
profiles rather than making every API mandatory.

## Ownership and prerequisites

| Owner | Responsibility |
| --- | --- |
| Transit / transitc | Runtime execution, protected credentials, transport/effects, durable state, compilation, and package resolution. |
| `tpackages` | Reusable protocol implementations and provider-specific protocol adapters. |
| `tintegrations` | Service resources, typed operations, provider-specific pagination/errors, synchronization, and domain workflows. |
| Consumer application | Business policy, field ownership/conflict decisions, account/tenant bindings, and selected authority/activation. |

The [foundation milestone](01-integration-foundation.md) tracks current compiler
constraints. Existing `tpackages` source is a candidate dependency, not proof of
executable protocol support. Reuse public entries only after qualifying the needed
profile, and record missing upstream work explicitly. Do not create synthetic
passing checks for unsupported source or move integration behavior into a second
runtime to hide those gaps.

Provider references in individual milestones were consulted for planning on
2026-11-19. They identify relevant API families; they do not freeze a supported
version. Before implementation, select the exact API/schema revision, account
type, authentication mode, permissions, event types, and test environment. Record
those choices alongside fixtures and supported behavior. Provider-specific
signatures, retries, and permission rules require their own qualification.

## Shared completion gates

Every service milestone must establish all of the following for its selected
profile, in addition to its provider-specific cases:

1. **Independent consumption.** An external consumer imports only public entries
   from pinned sources. Its build graph excludes unrelated integrations and
   unselected resource families, tests, webhooks, and background synchronization.
   Demonstrate two independent account/tenant instances.
2. **Useful end-to-end behavior.** Exercise a real public read, selected write,
   and declared synchronization workflow with typed results, durable progress,
   explicit authority, and bounded work. State concrete unsupported operations.
3. **Failure and recovery.** Test expired/revoked credentials, access changes,
   provider errors/throttling, duplicate/out-of-order input, partial results,
   interrupted pagination, lost write replies, and restart where applicable.
   State the provider's reconciliation limits; replay must not redispatch writes.
4. **Traceable evidence.** Record source/toolchain/API revisions, commands,
   fixtures, and results. Keep deterministic checks credential-free and verify
   the selected profile against a separate provider test account/environment
   where available. Report component tests and provider verification separately;
   a mocked success cannot substitute for the latter.
5. **Usable delivery.** Supply an executable consumer example, integration
   README, supported resource/authentication matrix, dependency list, and
   migration/compatibility notes. Add build/test coverage to repository CI.

## Maintaining the sequence

Keep one numbered, descriptively named Markdown file per milestone and exactly
one row for it in the ordered catalog. Use `Planned`, `In Progress`, and
`Completed` consistently in the index and milestone header. Keep phase membership
contiguous and exhaustive; phases group delivery outcomes, not runtime dependencies.

When inserting, splitting, or reordering work, update filenames, headings, index
rows, phase ranges, prerequisites, and inbound links together. Retain delivered
scope and prior evidence. Do not close a milestone merely because source was
authored, a parser accepted it, or a narrower component check passed.

When all completion criteria pass, update the milestone and index together,
retain the completed file and evidence, and document current usage beside the
integration. Reopen an unmet criterion as `In Progress`, preserving previous
results and naming remaining work. Contributor details are in
[AGENTS.md](AGENTS.md).
