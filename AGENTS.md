# AGENTS.md

## Repository Intent
This project is a **turn-based war strategy game**. All contributions should protect deterministic simulation, reproducible replays, and clear rule ownership.

## Mandatory workflow
1. Read `docs/design/game_design_document.md` before changing game rules.
2. If changing turn logic/combat/supply/victory rules, update:
   - `docs/design/game_design_document.md`
   - `docs/design/technical_design.md`
   - `docs/tasks/backlog.md`
3. Add or update deterministic tests for any rules change.
4. Log notable design decisions in `docs/logs/devlog.md`.

## Design constraints for turn-based war game
- Determinism first: identical seed + actions => identical result.
- Rules are data-driven when possible (unit stats, terrain modifiers, costs).
- Keep strategic layer and tactical resolution clearly separated.
- Preserve replayability: avoid hidden side effects in turn resolution.

## PR checklist
- [ ] Rule changes documented in design docs.
- [ ] Task status updated in backlog.
- [ ] Deterministic tests added/updated.
- [ ] Any balancing assumptions explicitly listed.
