# Dev Log

## Entry Template

Use this template for every notable change:

```text
## YYYY-MM-DD
### Short Title
- Why: why the change was needed.
- What Changed: the concrete updates that were made.
- Result: the observed outcome, verification status, or follow-up impact.
```

## 2026-03-31
### Turn-Based Strategy Scaffold
- Why: The repository needed an initial structure aligned to a turn-based war strategy game instead of a generic project template.
- What Changed: Adjusted the scaffold, clarified the core turn loop as intel -> orders -> resolution -> end of turn, and added constraints covering supply, morale, zones of control (ZOC), and deterministic replays.
- Result: The project now has a clearer design direction and a rules-first workflow for future implementation.

## 2026-03-31
### Backlog and Rule-Test Workflow
- Why: The original backlog was too coarse to support 1 to 2 day implementation slices, and the testing/devlog expectations needed to be explicit before rule work begins.
- What Changed: Split the backlog into smaller module-grouped tasks, added an explicit requirement for deterministic and rules coverage on rule changes, reinforced the workflow in the design docs and README, and standardized the devlog entry format.
- Result: The planning docs now support incremental delivery with clearer acceptance criteria, test expectations, and decision logging.
