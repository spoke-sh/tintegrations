# Documentation

- [Roadmap](roadmap/README.md): initial integrations, delivery order, prerequisites,
  acceptance criteria, and milestone status.
- [Implementation plan](roadmap/integration-implementation-plan.md): proposed
  native Transit composition, transactions, recovery, delivery units, and tests.
- [Integration state/dataflow models](roadmap/integration-state-models.md):
  concrete primitive ownership and first workflows for all 18 integrations.
- [Integration conventions](../integrations/README.md): package layout, public
  entries, dependency boundaries, and contribution workflow.
- [Repository README](../README.md): development environment and commands.

Delivery plans belong in `docs/roadmap/`. Keep current integration behavior,
configuration, examples, and supported API profiles beside the owning integration
under `integrations/<name>/`. A roadmap entry does not establish implemented
support.
