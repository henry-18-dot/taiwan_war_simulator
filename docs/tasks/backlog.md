# Backlog (Turn-Based War Strategy)

This backlog is grouped by module and split into tasks that should each fit within 1 to 2 days of focused work.

## Workflow Rules

- Read `docs/design/game_design_document.md` before changing gameplay rules.
- If a task changes turn logic, combat, supply, or victory rules, update:
  - `docs/design/game_design_document.md`
  - `docs/design/technical_design.md`
  - `docs/tasks/backlog.md`
- Every rule change must add or update:
  - at least one deterministic test in `tests/deterministic/`
  - at least one rules-focused test in `tests/rules/`
- Every notable change must append an entry to `docs/logs/devlog.md` that states:
  - why the change was made
  - what changed
  - the result

| ID | Module | Task | Priority | Status | Acceptance Criteria |
|---|---|---|---|---|---|
| TW-001 | Core | Create the initial source tree for `src/` modules and align it with the documented runtime layers | P0 | todo | `src/` contains the agreed top-level modules; ownership boundaries match the technical design; no gameplay rules are implemented yet |
| TW-002 | Core | Create the baseline test harness configuration and test command | P0 | todo | A minimal test runner/config exists; the repo has a documented command for running tests; empty test suites can execute without editing tracked files |
| TW-003 | Core | Add placeholder suites for deterministic and rules testing | P0 | todo | `tests/deterministic/` and `tests/rules/` exist; each folder contains a placeholder test or keep file; the test command discovers both suites |
| TW-004 | Core | Implement the phase enum, turn state machine shell, and legal phase transitions | P0 | todo | The runtime can move through the documented turn phases in order; invalid transitions are rejected; deterministic and rules tests cover the transition flow |
| TW-005 | Core | Implement pending turn action submission with a fixed three-slot selection contract | P0 | todo | The player can commit 1 primary, 1 secondary, and 1 information/diplomatic action; invalid combinations are rejected; deterministic and rules tests cover submission behavior |
| TW-006 | Core | Implement turn history logging and end-of-day archive records | P1 | todo | Each resolved turn appends an immutable history record; phase outputs are preserved for replay/debugging; deterministic tests confirm repeatable history output |
| TW-007 | Combat | Define data-driven unit combat stats and terrain modifier contracts | P0 | todo | Unit and terrain stat shapes are documented in code/data contracts; no hardcoded per-unit branching is required; rules tests cover schema validation or lookup behavior |
| TW-008 | Combat | Implement base hit chance and penetration resolution | P0 | todo | Combat resolution applies the documented hit and penetration formulas; deterministic and rules tests cover repeated resolution with fixed seeds and expected formula outputs |
| TW-009 | Combat | Implement morale damage and retreat resolution | P0 | todo | Morale loss and retreat outcomes resolve from combat results; deterministic and rules tests cover threshold and edge-case behavior |
| TW-010 | Combat | Implement combat log output for replay inspection | P1 | todo | Each combat generates a readable structured log; logs include key rolls, modifiers, and outcomes; deterministic tests confirm the same seed yields the same log output |
| TW-011 | Economy | Define the supply network model and disruption state contract | P0 | todo | Supply line data structures and disruption states are explicit; responsibilities between map, economy, and combat are documented; rules tests cover supply connectivity evaluation |
| TW-012 | Economy | Implement supply line tracing and supply status evaluation | P0 | todo | Units or regions can be marked supplied, strained, or cut off using deterministic logic; deterministic and rules tests cover representative map cases |
| TW-013 | Economy | Implement disruption penalties on readiness, combat efficiency, or movement budgets | P0 | todo | Supply disruption applies the documented penalties only through shared rule utilities; deterministic and rules tests cover penalty application and clamping |
| TW-014 | Economy | Implement end-of-turn supply recovery and persistence rules | P1 | todo | Recovery, persistence, and removal of supply penalties are resolved at a defined phase boundary; deterministic and rules tests cover repeated multi-turn outcomes |
| TW-015 | AI | Define the first tactical AI scoring inputs, weights, and output contract | P1 | todo | AI scoring inputs are data-driven and documented; outputs map cleanly to legal action packages; rules tests cover score calculation inputs and tie-breaking policy |
| TW-016 | AI | Implement baseline tactical AI action scoring | P1 | todo | The AI can score available actions and choose a legal response package; deterministic and rules tests verify the same state and seed produce the same choice |
| TW-017 | AI | Implement AI explanation tags for briefing and report text | P2 | todo | Chosen AI responses produce explanation tags suitable for UI summaries; deterministic tests confirm the same decisions emit the same tags |
| TW-018 | AI | Run a 50-turn stability regression for the baseline AI loop | P2 | todo | A repeatable automated run completes 50 turns without invalid state transitions or missing actions; deterministic regression output is captured for comparison |
| TW-019 | Scenario | Define the prototype scenario data package for map, factions, starting state, and limits | P1 | todo | The first scenario has explicit authored data for map, starting stats, and turn limit; scenario data can be loaded without rule-specific hardcoding |
| TW-020 | Scenario | Implement conflict phase advancement checks and scenario end-of-day progression hooks | P1 | todo | Phase advancement runs after end-of-day resolution using explicit thresholds; deterministic and rules tests cover forward progression and no-change cases |
| TW-021 | Scenario | Implement victory and loss evaluation for the documented prototype endings | P0 | todo | Coercive success, costly success, frozen crisis advantage, international escalation, domestic collapse, strategic ineffectiveness, and uncontrolled war spiral can be evaluated; deterministic and rules tests cover benchmark thresholds and edge cases |
| TW-022 | Scenario | Add a 20-turn scenario regression covering phase flow and victory evaluation | P1 | todo | The prototype scenario can run 20 turns with reproducible results; deterministic regression output confirms the same seed and actions yield the same ending |

## Notes for Future Task Updates

- Keep each new task independently completable in 1 to 2 days.
- Prefer data contracts and deterministic utilities before content-heavy implementation.
- When a task changes rules, update the affected acceptance criteria to explicitly mention deterministic coverage, rules coverage, and the required doc/devlog updates.
