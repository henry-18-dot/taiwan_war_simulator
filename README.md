# taiwan_war_simulator

A Codex collaboration scaffold for a **turn-based war strategy game**.
The goal is to let AI and humans iterate reliably within a workflow where rules are clear, data is tunable, and replays are verifiable.

## Directory Structure (for Turn-Based War Strategy)

```text
.
├── AGENTS.md
├── README.md
├── docs/
│   ├── design/
│   │   ├── game_design_document.md      # Core experience, victory/defeat, factions, resources, turn loop
│   │   └── technical_design.md          # Module boundaries, state machine, save/replay
│   ├── narrative/
│   │   └── worldbuilding.md             # Faction background, event arcs, political narrative
│   ├── prompts/
│   │   └── codex_prompting.md           # AI task templates (systems/campaign/AI/balance)
│   ├── tasks/
│   │   └── backlog.md                   # Tasks and version milestones
│   └── logs/
│       └── devlog.md                    # Decision log for each iteration
└── tools/
    └── ai/
        └── README.md                    # Content generation, balance validation, and battle report analysis scripts
```

## Suggested Code and Data Layers (can be created next)

```text
src/
├── core/             # Turn state machine, event bus, random seed
├── campaign/         # Campaign progress, victory resolution, chapter objectives
├── combat/           # Hit/penetration/morale/terrain/supply resolution
├── ai/               # Tactical AI, strategic AI, action scoring
├── map/              # Tiles, vision, pathing, zones of control (ZOC)
├── economy/          # Resources, production, repairs, supply lines
└── diplomacy/        # Relations, ceasefires, aid, sanctions

data/
├── units/            # Unit templates (mobility, firepower, armor, supply consumption)
├── factions/         # Faction attributes and tech trees
├── scenarios/        # Scenario maps, starting deployments, victory conditions
├── balance/          # Versioned balance parameters
└── localization/     # Multilingual text

tests/
├── deterministic/    # Reproducible tests with fixed seeds
├── simulation/       # Multi-turn automated battle regressions
└── rules/            # Unit tests for combat/supply/victory rules
```

## Suggested Development Order

1. First fill out the "turn loop + victory/defeat + key systems" sections in `docs/design/game_design_document.md`.
2. Then define the "state flow and data contracts" in `docs/design/technical_design.md`.
3. Break work down into tasks that can be finished in 1 to 2 days via `docs/tasks/backlog.md`.
4. Before deeper rule work, set up a minimal test harness plus `tests/deterministic/` and `tests/rules/`.
5. Every rule change must be accompanied by corresponding tests, at minimum `deterministic` and `rules`.
6. Record why a change was made, what changed, and the result in `docs/logs/devlog.md`.

## Workflow Expectations

- Keep backlog items scoped to 1 to 2 days of focused work.
- If a change affects turn logic, combat, supply, or victory rules, update:
  - `docs/design/game_design_document.md`
  - `docs/design/technical_design.md`
  - `docs/tasks/backlog.md`
- Deterministic tests verify that the same seed and the same actions produce the same outcome.
- Rules tests verify isolated gameplay behavior, thresholds, and edge cases.
- Each notable change should add a devlog entry with:
  - why the change was made
  - what changed
  - the result
