# 11. Google Drive

[Roadmap](README.md) · **Status:** Planned

Let applications track selected files and folders and exchange bounded content with durable progress.
Planned package root: `integrations/google-drive/`.

## Prerequisites and scope

Depends on the relevant [foundation contracts](01-integration-foundation.md),
not on earlier service integrations. This is a proposed initial profile.

Start with file/folder metadata, selected content download/export and upload/update operations, and incremental change reconciliation. Record the supported My Drive/shared-drive profile explicitly.

Compose the candidate tpackages oauth-google public entry after qualification. Bind the Google account, selected drive/file scopes, and destination; this integration must not require Gmail or Calendar.

Native Docs/Sheets/Slides editing, full desktop-drive emulation, unrestricted sharing administration, and unlimited media transfer are deferred.

Provider basis: [Drive API overview](https://developers.google.com/workspace/drive/api/guides/about-sdk).

## Delivery sequence

1. Implement stable file identities, metadata/permission-aware reads, and bounded content transfer with explicit format limits.
2. Implement selected writes and incremental change checkpoints with recovery when continuation state is unusable.
3. Provide a selected-folder synchronization example with visible removals/access loss and resumable progress.

## Completion evidence

Pass the [shared completion gates](README.md#shared-completion-gates), plus:

- Exercise inaccessible/deleted files, shared-drive boundaries, interrupted transfers, expired checkpoints, and changed content.
- Verify Drive-only consumers contain neither Gmail nor Calendar modules or required configuration.

