# Integration state and dataflow models

Status: **Proposed for review — 2026-11-19.**

Read the [implementation plan](integration-implementation-plan.md) first for
shared identity, authority, atomicity, effect/replay, retention, and migration
contracts. Each model below implements an existing [catalog milestone](README.md)
without expanding its exclusions. All resource and flow names are proposed
logical names, not claims that new Transit syntax is executable.

Each full profile inherits the common connection identity, operation ledger,
versioned policy, sync positions, and authorized reads. Tables below identify
provider-specific roles rather than requiring a monolithic instance with every
optional feature. Relationship Tables and Document attributes have distinct
canonical fields; raw provider captures are evidence, not a second writable copy.
Select only resources needed by the chosen public modules.

KV refresh coalescing requires a guarded generation: an accepted hint advances
the wanted generation and durably admits work. Completing an older refresh may
clear the claim only if no newer hint arrived; otherwise it schedules the next
bounded continuation in the same decision. Do not drop wakeups by deleting a
claim unconditionally. Delivery identity must follow the provider's authenticated
uniqueness contract; equal payload hashes alone do not prove equal deliveries.
Distinguish logical events from delivery attempts and compare contract-defined
immutable content, allowing documented changes to redelivery metadata.

Without a provider version/order guarantee, serialization prevents conflicting
local acceptance but cannot prove globally freshest remote state. Emit observed
basis/time and honest coverage; qualify how each profile handles older responses.
Notifications and list/search cursors are not generic change-data-capture tokens.

## Model index

| Integration | Model | Milestone |
| --- | --- | --- |
| Stripe | [Primitive model](#stripe) | [Scope and completion](02-stripe.md) |
| GitHub | [Primitive model](#github) | [Scope and completion](03-github.md) |
| Salesforce | [Primitive model](#salesforce) | [Scope and completion](04-salesforce.md) |
| HubSpot | [Primitive model](#hubspot) | [Scope and completion](05-hubspot.md) |
| Slack | [Primitive model](#slack) | [Scope and completion](06-slack.md) |
| Linear | [Primitive model](#linear) | [Scope and completion](07-linear.md) |
| Jira Cloud | [Primitive model](#jira-cloud) | [Scope and completion](08-jira.md) |
| GitLab | [Primitive model](#gitlab) | [Scope and completion](09-gitlab.md) |
| Notion | [Primitive model](#notion) | [Scope and completion](10-notion.md) |
| Google Drive | [Primitive model](#google-drive) | [Scope and completion](11-google-drive.md) |
| Google Calendar | [Primitive model](#google-calendar) | [Scope and completion](12-google-calendar.md) |
| Gmail | [Primitive model](#gmail) | [Scope and completion](13-gmail.md) |
| Microsoft Outlook | [Primitive model](#microsoft-outlook) | [Scope and completion](14-microsoft-outlook.md) |
| Microsoft Teams | [Primitive model](#microsoft-teams) | [Scope and completion](15-microsoft-teams.md) |
| Airtable | [Primitive model](#airtable) | [Scope and completion](16-airtable.md) |
| Zendesk | [Primitive model](#zendesk) | [Scope and completion](17-zendesk.md) |
| Intercom | [Primitive model](#intercom) | [Scope and completion](18-intercom.md) |
| Shopify | [Primitive model](#shopify) | [Scope and completion](19-shopify.md) |

## Stripe

[Milestone](02-stripe.md) · Planned root: `integrations/stripe/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Customer/product/price/session/subscription/invoice identities and relationships; original customer/session command identities; billing refresh runs and query indexes. |
| `DOCUMENT` | Versioned customer and billing attributes, selected event interpretation/API-version policy, and application-supplied resource mappings. Keep application entitlement decisions outside this state. |
| `KV` | Verified event receipts scoped to the bound account/endpoint and event profile; per-resource refresh generations. Native secret storage owns signing/API keys. |
| `QUEUE` | Customer/Checkout Session writes, billing-resource refreshes, list pages, and explicitly authorized uncertain-operation reconciliation. |
| `STREAM` | Customer and billing observations, Checkout Session operation outcomes, and reconciliation progress. Session completion and observed payment/subscription state remain distinct events. |
| `DATAFLOW` | AdmitCustomer/Checkout, DispatchStripe, AcceptStripeResponse, VerifyEvent, RefreshBilling, ReconcileAttempt, and bounded maintenance. |

**First workflow and atomic acceptance.** Create a customer, create a Checkout Session using the resulting customer
reference, then ingest a selected billing event. Admission commits operation
plus Queue work; response acceptance commits identity, attribute Document
revision, and result Stream. Verified event intake claims KV and enqueues
refresh atomically; the billing consumer reacts to committed observations
rather than an unverified payload.

**Required failure proof.** Drop a create response, redeliver the event, reorder old/new billing hints,
rotate a signing key, and restart before event settlement. Preserve the
original operation/idempotency contract and current account binding. Unknown
writes never become a fresh checkout automatically.

## GitHub

[Milestone](03-github.md) · Planned root: `integrations/github/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Repository/work-item/comment identities, repository membership relations, issue-versus-pull-request kind, command ledger, and per-repository sync progress. |
| `DOCUMENT` | Issue/PR/comment attributes and bounded bodies; versioned repository selection and permitted-operation policy. Numeric issue number is scoped to its repository, not a universal identity. |
| `KV` | Verified webhook delivery receipts and per-work-item refresh generations; short-lived webhook validation context where required. |
| `QUEUE` | Repository/work-item pages, issue/comment mutations, object refreshes, and reconciliation/status reads. |
| `STREAM` | Repository/work-item observations, command outcomes, and repository sync progress, retaining remote identity and source revision basis. |
| `DATAFLOW` | ConnectOAuth, ListRepositoryWork, AdmitIssue/Comment, DispatchGitHub, AcceptObservation, VerifyWebhook, RefreshWorkItem, and ConsumeCredentialCompletion. |

**First workflow and atomic acceptance.** Compose oauth-github through its public port, observe an issue, admit a
selected update, and consume a verified webhook-driven refresh. The update
result records provider evidence; the refresh commits its Document and indexed
identity with the output/checkpoint. Consumers do not call an OAuth or
integration finish method.

**Required failure proof.** Lose a comment-create reply, replay a delivery, transfer a repository/issue,
and revoke access during refresh. Preserve comments with unknown outcomes
instead of reposting; distinguish inaccessible resources from deletion. No
merge or Actions execution enters the selected graph.

## Salesforce

[Milestone](04-salesforce.md) · Planned root: `integrations/salesforce/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Organization/object/record identities, selected account-contact/opportunity relationships, external-ID constraints for chosen writes, operation ledger, and bounded query/reconciliation runs. |
| `DOCUMENT` | Selected typed record attributes, versioned Describe/field mappings, and allowed object/field policy. Separate a provider's schema revision/basis from local Document revisions. |
| `KV` | Point refresh generations and short-lived validation/context claims. No fictional CDC receipt store is required for the initial polling profile. |
| `QUEUE` | Describe refreshes, query pages, record writes/upserts, targeted reads, and bounded reconciliation sweeps. |
| `STREAM` | Record observations, schema/mapping-change notices, per-record write outcomes, and sync coverage/progress. |
| `DATAFLOW` | RefreshSchema, QueryPage, MapRecord, AdmitRecordWrite, DispatchSalesforce, AcceptRecord, and ReconcileSelection from native timer/Queue inputs. |

**First workflow and atomic acceptance.** Load a bounded schema profile, read one Contact with its Account relation, and
update a selected field. Admission binds the schema/policy revision; response
acceptance checks that basis and commits canonical attributes, relationship
changes, and output together. A native timer schedules the next bounded
reconciliation.

**Required failure proof.** Change a custom field type or write permission after admission, interrupt a
multi-page query, and lose an upsert reply. Refuse incompatible writes and keep
partial coverage visible; a completed ordinary search is not proof that missing
records were deleted.

## HubSpot

[Milestone](05-hubspot.md) · Planned root: `integrations/hubspot/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Contact/company/deal identities, association edges with provider association type, pipeline/stage identities, per-record operations, and reconciliation progress. |
| `DOCUMENT` | Typed selected CRM properties, property-schema/pipeline snapshots, and versioned mapping and subscription policy. |
| `KV` | Verified notification receipts using the selected app/event uniqueness contract, and point refresh generations for affected records/associations. |
| `QUEUE` | Object/property pages, selected record/association writes, webhook-triggered refreshes, and bounded reconciliation. |
| `STREAM` | CRM observations, relationship changes, individual write outcomes, schema-policy notices, and sync progress. |
| `DATAFLOW` | RefreshProperties, ReadObjects, AdmitRecord/AssociationChange, DispatchHubSpot, AcceptBatchMembers, VerifyNotification, and RefreshCRM. |

**First workflow and atomic acceptance.** Create or select a Contact, link it to a Company through an explicit
association command, and observe a Deal stage. Each accepted response commits
attributes and relation indexes with output. A provider batch has a parent
operation and separate member outcomes; partial success never becomes one
atomic remote CRM transaction.

**Required failure proof.** Return a mixed-success batch, repeat a webhook batch, change a property/stage,
and lose a contact-create reply. Apply only evidenced successful members,
retain unknown members, and verify connection-scoped associations.

## Slack

[Milestone](06-slack.md) · Planned root: `integrations/slack/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Workspace/user/conversation/message identities, thread relationships, selected channel membership, message operation ledger, and history-window progress. |
| `DOCUMENT` | Bounded message/block attributes, edited/deleted observations, and versioned conversation, visibility, and notification policy. |
| `KV` | Verified Events API receipts, point conversation refresh generations, and provider-budget context keyed to the actual workspace/app/method scope. |
| `QUEUE` | Bounded conversation/history/thread fetches, message writes, event refreshes, and delayed reads under the selected rate policy. |
| `STREAM` | Conversation/message observations, message operation outcomes, access changes, and history coverage. |
| `DATAFLOW` | VerifySlackEvent, RefreshConversation/Thread, AdmitMessage, DispatchSlack, AcceptMessageObservation, and BudgetWakeup. |

**First workflow and atomic acceptance.** Read a selected thread, post one workflow message, and consume its echoed
event. Keep message timestamp identifiers as provider strings. The native
attempt result establishes the sent message identity; event acceptance may
update its Document but cannot repeat the outbound command.

**Required failure proof.** Lose the post reply, replay its event, receive an edit before an older
observation, remove channel access, and exhaust history budgets. Keep an
uncertain send inspectable and do not silently turn it into a second message.

## Linear

[Milestone](07-linear.md) · Planned root: `integrations/linear/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Workspace/team/project/issue/comment identities and relationships, operation ledger, and per-query connection progress. |
| `DOCUMENT` | Typed issue/project attributes, workflow/label schema snapshots, pinned GraphQL interpretation, and versioned field-ownership policy. |
| `KV` | Verified webhook receipts, point issue refresh generations, and selected query-cost/rate context. |
| `QUEUE` | Static selected GraphQL query pages, typed issue/comment mutations, object refreshes, and explicit reconciliation reads. |
| `STREAM` | Issue/project observations, workflow-state changes, per-mutation outcomes, and query/sync progress. |
| `DATAFLOW` | ReadLinearPage, ValidateGraphQLResult, AdmitIssueMutation, DispatchLinear, AcceptIssue, VerifyWebhook, and ReconcileIssue. |

**First workflow and atomic acceptance.** Observe an issue and its team's permitted states, submit one state change, and
consume the resulting refresh. The parser preserves GraphQL data/errors by
selected field or operation; response acceptance only publishes the portion
whose validity and coverage are established.

**Required failure proof.** Return HTTP success with GraphQL errors/partial data, change the workflow,
reorder refreshes, and lose a mutation reply. No arbitrary GraphQL request
interpreter or HTTP-200-equals-success shortcut is accepted.

## Jira Cloud

[Milestone](08-jira.md) · Planned root: `integrations/jira/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Site/project/issue identities, issue-type/field/transition relationships, comment identities, command ledger, and selected search/reconciliation runs. |
| `DOCUMENT` | Typed selected issue fields, project-specific field/transition snapshots, permitted-operation policy, and bounded comment content. |
| `KV` | Verified change-notification receipts where the selected profile supplies identity, plus per-issue refresh generations and validation context. |
| `QUEUE` | Metadata/search pages, issue/comment/transition writes, targeted issue refreshes, and bounded reconciliation. |
| `STREAM` | Issue observations, transition outcomes, schema changes, and per-selection synchronization coverage. |
| `DATAFLOW` | RefreshProjectMetadata, ReadIssuePage, ValidateTransition, DispatchJira, AcceptIssue, VerifyChange, and ReconcileProject. |

**First workflow and atomic acceptance.** Read one issue with current project metadata, request a permitted transition,
and refresh the result. Bind the write to its metadata/policy basis; accept
relation/index changes and the attribute Document revision in one native
decision.

**Required failure proof.** Remove a required custom field, change available transitions after admission,
move the issue, and interrupt search pagination. Missing search membership is
not remote deletion; transition errors remain typed provider outcomes.

## GitLab

[Milestone](09-gitlab.md) · Planned root: `integrations/gitlab/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Origin/project/issue/merge-request/note identities, relationships, operation ledger, and per-project progress. Project-local numbers are separate from stable remote keys. |
| `DOCUMENT` | Issue/MR/note attributes, selected project configuration, and versioned OAuth/webhook policy. |
| `KV` | Authenticated delivery receipts under GitLab's selected event contract and point project/work-item refresh generations. |
| `QUEUE` | Project/work-item pages, issue/note writes, webhook-triggered refreshes, and reconciliation reads. |
| `STREAM` | Project/work-item observations, note/issue outcomes, and project synchronization progress. |
| `DATAFLOW` | ReadGitLabProject, AdmitIssue/Note, DispatchGitLab, AcceptWorkItem, VerifyProjectHook, and RefreshProjectWork. |

**First workflow and atomic acceptance.** Observe a project issue, add a selected note, and reconcile a verified hook.
Store hook acknowledgement only with admitted durable work; commit the
refreshed Document, canonical identity, and emitted observation together.

**Required failure proof.** Lose a note reply, rename/transfer a project, replay a hook, and revoke
membership. Keep origin/account isolation and ensure the selected graph has no
dependency on GitHub.

## Notion

[Milestone](10-notion.md) · Planned root: `integrations/notion/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Workspace/page/block/data-source identities, parent-child relations, bounded traversal frontier/progress, and page/append operation ledger. |
| `DOCUMENT` | Typed page properties, supported block content, data-source schemas, and versioned selection/mapping policy. Unsupported block/property variants remain explicit. |
| `KV` | Point page/block refresh generations and bounded traversal validation context. Do not duplicate the relational frontier or operation ledger here. |
| `QUEUE` | Page/query/block-child pages, selected property updates and block appends, and bounded refresh/reconciliation work. |
| `STREAM` | Page/block observations, schema changes, traversal coverage, and write/append outcomes. |
| `DATAFLOW` | ReadPage, TraverseChildren, QueryDataSource, AdmitProperty/Append, DispatchNotion, AcceptPageRevision, and ReconcileSelection. |

**First workflow and atomic acceptance.** Read a page and one bounded subtree, update one supported property, and refresh
it. Commit the block/page Document revision and its parent-child index with
traversal progress. Partial traversal is visible and cannot be described as a
full document snapshot.

**Required failure proof.** Change a property schema, revoke a shared page, exceed a depth/content bound,
and lose an append response. Preserve unknown append status; repeated traversal
cannot authorize a repeat append.

## Google Drive

[Milestone](11-google-drive.md) · Planned root: `integrations/google-drive/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Drive/file identities and parent relations, explicit access/removal state, transfer operations, and per-drive change/snapshot positions and generations. |
| `DOCUMENT` | Typed file metadata and bounded content/export manifests; versioned drive/folder selection and format policy. Bytes live in protected native blob storage. |
| `KV` | Verified watch validation/delivery context when selected, point file refresh generations, and bounded transfer verification context. |
| `QUEUE` | File/list/change pages, object/content refreshes, selected upload/update work, and optional watch renewal. |
| `STREAM` | File/content observations, access/removal notices, transfer outcomes, and change-feed/snapshot progress. |
| `DATAFLOW` | BeginDriveSnapshot, ReadDriveChanges, TransferContent, AcceptFile, AdmitFileWrite, ReconcileFile, and optional RenewWatch. |

**First workflow and atomic acceptance.** For a chosen coverage profile, capture a changes start token, enumerate
selected metadata, then drain changes from that basis; verify this bootstrap
against the provider contract. Within a change run, accept each page with its
next-page position; publish the new completed start token only on the final
page. Content publication additionally requires a complete verified native
transfer.

**Required failure proof.** Crash at page acceptance, change files during enumeration, receive a
removal/access change, and interrupt an upload. A watch hint contains no
assumed file contents; keep metadata/content revisions distinct and validate
transfer completion before emitting content availability.

The [Drive changes
guide](https://developers.google.com/workspace/drive/api/guides/manage-changes)
distinguishes `nextPageToken` from final `newStartPageToken` and describes
notifications as wakeups for reading changes. The bootstrap sequence above is a
proposed integration design to qualify, not a provider snapshot guarantee.

## Google Calendar

[Milestone](12-google-calendar.md) · Planned root: `integrations/google-calendar/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Calendar/event identities, recurring-series/exception relationships, event commands, and per-calendar selection, page position, sync token, and resync generation. |
| `DOCUMENT` | Typed event/attendee/time-zone attributes, recurrence definitions, and versioned calendar scope and notification policy. |
| `KV` | Watch validation context when selected, verified notification receipts where defined, and point calendar/event refresh generations. |
| `QUEUE` | Event pages, selected create/update/cancel work, bounded recurrence queries, resync pages, and optional watch renewal. |
| `STREAM` | Event/availability observations, event-operation outcomes, access changes, and synchronization progress. |
| `DATAFLOW` | ReadCalendarPage, ApplyCalendarChanges, AdmitEventChange, DispatchCalendar, AcceptEvent, ResetCalendarSync, and optional RenewWatch. |

**First workflow and atomic acceptance.** Perform a complete selected event synchronization, then an incremental pass and
one explicit event update. The final-page sync token commits only after its
data. A provider-required full resync starts a new fenced generation; old
operation/effect history and currently valid historical evidence are not wiped.

**Required failure proof.** Invalidate the sync token, change permissions/filters, cross daylight-saving
boundaries, modify recurring exceptions, and lose a create reply. Prefer
bounded provider occurrence expansion in the initial profile; a new general
recurrence engine is not supplied implicitly by icalendar.

The [Calendar sync
guide](https://developers.google.com/workspace/calendar/api/guides/sync)
specifies final-page sync tokens, query restrictions, and full
resynchronization after a `410`. The integration will distinguish invalid
current coverage from retained historical observations.

## Gmail

[Milestone](13-gmail.md) · Planned root: `integrations/gmail/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Mailbox/message/thread/label identities and memberships, draft/send operations, and per-mailbox history/snapshot progress. |
| `DOCUMENT` | Typed selected message headers/metadata, bounded MIME/content manifests, draft intent, and versioned mailbox scope/send policy; content and attachments use protected native references. |
| `KV` | Optional push validation/notification receipts and point mailbox/message refresh generations. The accepted history position remains canonical in its Table. |
| `QUEUE` | Message/history pages, bounded attachment reads, draft/label/send work, history-reset reconciliation, and optional watch renewal. |
| `STREAM` | Message/label/thread observations, draft/send outcomes, mailbox coverage, and history-reset notices. |
| `DATAFLOW` | ReadMailbox, ReadHistory, AcceptMessageChange, AdmitDraft/Send, DispatchGmail, ReconcileSend, and ResetMailboxSync. |

**First workflow and atomic acceptance.** Build a bounded mailbox projection, apply a history page, create a draft, and
admit a send as separate durable operations. Accepting history advances
membership/Documents and the history position with output. Provider send
acceptance and recipient delivery are different facts.

**Required failure proof.** Return an unavailable history range, replay a notification, lose a send reply,
and exceed an attachment bound. Resync only the declared mailbox coverage and
never resend messages while rebuilding it.

The [Gmail synchronization
guide](https://developers.google.com/workspace/gmail/api/guides/sync) describes
partial synchronization from history and a full-sync fallback for an
out-of-range history ID (`404`). Push is an optional wakeup path, not a
replacement for accepted history progress.

## Microsoft Outlook

[Milestone](14-microsoft-outlook.md) · Planned root: `integrations/microsoft-outlook/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Tenant/mailbox/folder/message and calendar/event identities in separate modules; command ledgers; collection-specific page/delta positions and resync generations. |
| `DOCUMENT` | Typed message/event attributes, bounded content/attachment manifests, recurrence data, and separately versioned mail/calendar policy. |
| `KV` | Notification validation/subscription context when selected, verified receipt keys, and per-collection refresh generations. |
| `QUEUE` | Selected mail/calendar delta pages, message/content reads, draft/send or event writes, resync, and optional subscription renewal. |
| `STREAM` | Separate mail and calendar observations/outcomes/progress. Selecting mail alone creates no calendar state or activation. |
| `DATAFLOW` | ReadMailDelta, ReadCalendarDelta for qualified resource profiles, AcceptGraphPage, AdmitMail/Event, DispatchGraph, ResetDelta, and optional RenewSubscription. |

**First workflow and atomic acceptance.** Implement a mail-only delta consumer and draft/send workflow first, then a
separate bounded calendar profile. Preserve each returned continuation URL as
opaque protected context bound to its collection/filter and validated
destination. `nextLink` continues a run; `deltaLink` becomes the completed
basis only after acceptance.

**Required failure proof.** Return an empty page with a next link, invalidate delta state, alter a calendar
range, revoke delegated access, and lose a send reply. A renewal or resync must
not activate the other module or the Teams integration.

The [Microsoft Graph delta
guide](https://learn.microsoft.com/en-us/graph/delta-query-overview)
distinguishes page and delta links and separates pull-based delta from push
notifications. Qualify delta availability and parameter restrictions for each
selected mail/calendar resource; do not generalize that support to Teams.

## Microsoft Teams

[Milestone](15-microsoft-teams.md) · Planned root: `integrations/microsoft-teams/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Tenant/team/channel/chat/message identities, membership relations, message operations, subscription lifecycle indexes, and bounded conversation progress. |
| `DOCUMENT` | Typed selected message/reply attributes, versioned resource/permission matrix, subscription intent, and conversation selection policy. |
| `KV` | Notification validation context and receipts under the chosen subscription contract; per-conversation refresh generations. |
| `QUEUE` | Conversation/message pages, permitted message writes, change refreshes, subscription registration/renewal, and reconciliation. |
| `STREAM` | Conversation observations, message outcomes, access/subscription status changes, and coverage/progress. |
| `DATAFLOW` | ReadTeamsConversation, ValidateNotification, RefreshConversation, AdmitTeamsMessage, DispatchTeams, AcceptTeamsObservation, and MaintainSubscription. |

**First workflow and atomic acceptance.** Qualify one channel read/post permission profile, observe messages, post a
workflow message, and process a validated notification as a bounded refresh
hint. Subscription renewal is a native timer/Queue flow with desired policy in
a Document and indexed lifecycle progress in a Table.

**Required failure proof.** Change membership, reject the permission mode, expire a subscription, duplicate
a notification, and lose the message-post response. No universal Teams delta
feed or app-only send authority is inferred from another Graph endpoint.

## Airtable

[Milestone](16-airtable.md) · Planned root: `integrations/airtable/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Base/table/field/record identities, linked-record relations, selected uniqueness/upsert bindings, operation members, and per-table scan progress. |
| `DOCUMENT` | Typed supported cell values, versioned field schemas/mappings, and base/table scope policy. Computed and writable fields have distinct types/capabilities. |
| `KV` | Point record/schema refresh generations; verified webhook receipts only if a matching optional change profile is selected. |
| `QUEUE` | Schema and record pages, selected record/batch writes, relation refreshes, and bounded reconciliation. |
| `STREAM` | Record and schema observations, member-level write outcomes, and per-table coverage. |
| `DATAFLOW` | ReadBaseSchema, ReadRecordPage, ValidateCellWrite, DispatchAirtable, AcceptRecordMembers, and ReconcileTable. |

**First workflow and atomic acceptance.** Read a table's schema and records, update one writable field, and reconcile
linked-record references. Guard schema interpretation at admission/acceptance;
commit canonical cell Documents and relation indexes with per-record output and
page progress.

**Required failure proof.** Rename a field, change its type, return partial batch success, remove base
access, and lose a create reply. Stable field IDs survive renaming;
formula/computed fields are not made writable by a generic record decoder.

## Zendesk

[Milestone](17-zendesk.md) · Planned root: `integrations/zendesk/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Account/ticket/user/organization/comment identities, assignment relations, operation members, and qualified incremental-export or bounded reconciliation progress. |
| `DOCUMENT` | Typed ticket/custom-field attributes and comment content, versioned field/status policy, and explicit public-reply/internal-note intent. |
| `KV` | Authenticated notification receipts where selected and point ticket refresh generations. |
| `QUEUE` | Ticket/customer pages, selected ticket/assignment/comment writes, change refreshes, and reconciliation. |
| `STREAM` | Ticket observations, assignment/status changes, distinct reply/note outcomes, and synchronization coverage. |
| `DATAFLOW` | ReadTicketChanges, AdmitTicket/Reply/Note, DispatchZendesk, AcceptTicket, VerifyChange, and ReconcileTicket. |

**First workflow and atomic acceptance.** Read a ticket, add an internal note as a separately typed command, and refresh
its state. Native response acceptance commits the note visibility, ticket
Document/index changes, and output. Qualify a provider cursor/export profile
before promising deletion or complete incremental coverage.

**Required failure proof.** Create an update conflict, change custom fields, duplicate change delivery,
lose a public reply response, and expire an idempotency window. Internal notes
cannot appear on the public-reply Stream or be recovered as customer-visible
sends.

## Intercom

[Milestone](18-intercom.md) · Planned root: `integrations/intercom/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Workspace/contact/company/conversation/part identities, participant/assignment/tag relationships, operation ledger, and selected conversation progress. |
| `DOCUMENT` | Typed contact and conversation attributes, bounded note/reply content, mapping policy, and pinned regional/API profile. |
| `KV` | Verified webhook receipts scoped to workspace/topic contract and point conversation/contact refresh generations. |
| `QUEUE` | Contact/conversation pages, selected assignment/status/reply/note writes, webhook refreshes, and reconciliation. |
| `STREAM` | Customer/conversation observations, distinct reply/note/assignment outcomes, and sync progress. |
| `DATAFLOW` | ReadConversation, AdmitConversationAction, DispatchIntercom, AcceptConversationPart, VerifyWebhook, and RefreshConversation. |

**First workflow and atomic acceptance.** Associate a selected conversation with an application customer reference, add
an internal note, and observe an assignment change. The relationship is
integration state; the application's account-linking policy authorizes it. A
refresh transaction accepts the new Document and relationships with output.

**Required failure proof.** Change contact identity/assignment, use the wrong regional destination, replay
a webhook, and lose a reply result. Retain unknown external replies and keep
internal note bodies outside customer-facing result selection.

## Shopify

[Milestone](19-shopify.md) · Planned root: `integrations/shopify/`

| Primitive | Proposed resources and responsibility |
| --- | --- |
| `TABLE` | Shop/product/variant/customer/order identities, selected catalog/order relationships, operation members, and bounded query/reconciliation progress. |
| `DOCUMENT` | Typed selected commerce attributes, schema/API-version interpretation, supported metadata, and versioned shop/resource policy. |
| `KV` | Verified webhook delivery/event receipts according to the chosen profile, point resource refresh generations, and shop/app query-budget context. |
| `QUEUE` | Selected GraphQL pages, product metadata/order-note/tag mutations, resource refreshes, and bounded reconciliation. |
| `STREAM` | Commerce observations, member-level mutation outcomes, query-budget/sync status, and access/removal notices. |
| `DATAFLOW` | ReadCommercePage, ValidateGraphQLResult, AdmitMetadataChange, DispatchShopify, AcceptCommerceResource, VerifyWebhook, and ReconcileShop. |

**First workflow and atomic acceptance.** Observe an order, update selected metadata, and reconcile its verified event.
Preserve GraphQL user/field errors and query-cost evidence; accept only
established successful results, then commit resource Documents/indexes and
output together.

**Required failure proof.** Return partial GraphQL results, throttle a page, reorder/duplicate webhooks,
revoke shop access, and lose a mutation response. Order observations cannot
trigger fulfillment, refunds, or other excluded writes merely because a
consumer replays history.
