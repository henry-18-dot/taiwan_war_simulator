# Codex Prompting (Turn-Based War Strategy)

## General Task Template
```text
Goal:
Game layer: strategic / tactical / resolution
Scope of changes:
Input documents:
Output files:
Acceptance criteria:
Determinism requirement: same seed + same action sequence => same result
```

## Example 1: Supply Line Rules
```text
Goal: implement a "supply line disruption penalty"
Game layer: resolution
Scope of changes: only modify the supply resolution module and the related tests
Input documents: docs/design/game_design_document.md
Output files: src/economy/*, tests/rules/*
Acceptance criteria:
1) After 2 consecutive turns without supply, mobility is reduced by 30%
2) After 3 consecutive turns, firepower is reduced by 20%
3) Tests cover boundary conditions
```

## Example 2: Tactical AI Action Scoring
```text
Goal: raise the AI's priority for contesting key strongpoints
Game layer: tactical
Scope of changes: src/ai/tactical/*
Input documents: docs/design/game_design_document.md, docs/design/technical_design.md
Output files: src/ai/tactical/*, tests/simulation/*
Acceptance criteria: across 100 simulations, key strongpoint capture rate improves without overfitting win rate
```
