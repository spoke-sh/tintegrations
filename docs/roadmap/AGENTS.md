# Working on the roadmap

This directory owns delivery scope, dependencies, acceptance criteria, and
milestone status. Read the [roadmap index](README.md) and the affected milestone
before editing. The structure follows Transit's roadmap, adapted to this repo's
integration ownership and existing development tools.

## Define executable outcomes

Start with the service resources and workflows an application needs and the
outcomes it must inspect. Name the public operations, authentication profile,
state ownership, failure/recovery behavior, and prerequisites. Separate planned
source, executable support, deterministic tests, and live provider verification.

Keep shared protocol behavior in `tpackages` and runtime/compiler work in Transit
or transitc. Record missing upstream capabilities as prerequisites; never turn
an expected compiler failure into successful integration qualification.

## Maintain the sequence

Follow the [sequencing rule](README.md#maintaining-the-sequence). Keep one numbered,
descriptively named file per milestone and one ordered index. Use `Planned`,
`In Progress`, or `Completed` consistently in its header and index row.

State dependencies explicitly. Delivery order does not create a runtime dependency
between integrations. When inserting or reordering work, update numbering, index
rows, dependency references, and inbound links together. Preserve completed work
and its evidence when splitting a milestone.

## Close or reopen with evidence

Mark a milestone `Completed` only when its completion criteria pass. Record the
tested source/toolchain/API revisions, commands, results, and limits in the
milestone or a linked evidence record. Put supported usage and concrete limits in
the integration's README/docs, then update the milestone and index together.
Keep completed files.

If an unmet criterion is found, reopen the milestone as `In Progress`, preserve
prior evidence, and name the remaining work. Before finishing documentation
changes, check local links and anchors, milestone numbering and statuses, and
`git diff --check`. Runtime checks are needed when executable behavior changes;
documentation edits alone do not establish new runtime support.
