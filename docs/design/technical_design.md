# Technical Design

## Document Info

* File path: `docs/design/technical_design.md`
* Project codename: `Strait: Critical Days`
* Scope of this section: State Flow and Data Contracts
* Target build: Prototype v0.1

---

## 1. Purpose

This document defines the runtime state structure and data contracts required to implement the prototype game loop.

The goals of this section are:

1. Establish a clear **state flow** for a 1-day-per-turn strategy game.
2. Define stable **data contracts** between gameplay logic, UI rendering, content data, and AI behavior.
3. Keep implementation lightweight enough for a minimalist Flash-style prototype while preserving clean future extensibility.

This section is intentionally scoped to:

* turn lifecycle state transitions
* runtime data ownership
* payload shapes for core gameplay objects
* separation between authored content and simulation logic

This section does **not** define:

* rendering implementation details
* animation system details
* save/load persistence format beyond the base state shape
* production backend or networking architecture

---

## 2. Technical Design Principles

### 2.1 Single Source of Truth

The game should maintain one authoritative in-memory `GameState` object.
All gameplay systems read from and write to this object through explicit phase transitions.

### 2.2 Deterministic Turn Resolution

Given the same:

* initial state
* player actions
* AI seed / random seed
* content definitions

…the turn result should be reproducible.

This is important for:

* debugging
* balancing
* replay inspection
* future save/load support

### 2.3 Data-Driven Content

Actions, events, endings, and phase definitions should be authored as data wherever possible.
Core simulation code should interpret data rather than hardcode scenario content.

### 2.4 Explicit Phase Boundaries

A turn is divided into clearly defined runtime phases. Each phase has:

* allowed inputs
* expected outputs
* valid state mutations

This reduces hidden coupling and makes UI flow easier to control.

### 2.5 Prototype-First Scope

The design should support a clean prototype with minimal implementation burden. Prefer:

* flat structures over deep inheritance
* explicit enums over implicit strings where practical
* readable payloads over over-abstracted schemas

---

## 3. High-Level State Flow

### 3.1 Turn Lifecycle Overview

Each game day follows this state progression:

1. `MORNING_BRIEFING`
2. `PLAYER_ACTION_SELECTION`
3. `AI_RESPONSE_SELECTION`
4. `TURN_RESOLUTION`
5. `EVENT_RESOLUTION`
6. `END_OF_DAY_REPORT`
7. `PHASE_ADVANCEMENT_CHECK`
8. `WIN_LOSS_CHECK`
9. `NEXT_DAY_SETUP`

This flow repeats until an ending is reached or the maximum turn count is exceeded.

---

### 3.2 Runtime State Machine

The core session can be represented as a finite state machine:

* `BOOT`
* `MAIN_MENU`
* `NEW_GAME_SETUP`
* `IN_GAME_MORNING_BRIEFING`
* `IN_GAME_ACTION_SELECTION`
* `IN_GAME_AI_RESOLUTION`
* `IN_GAME_TURN_RESOLUTION`
* `IN_GAME_EVENT_RESOLUTION`
* `IN_GAME_END_OF_DAY_REPORT`
* `IN_GAME_END_CHECK`
* `ENDING`
* `POST_GAME_SUMMARY`

For prototype purposes, `BOOT`, `MAIN_MENU`, and `NEW_GAME_SETUP` may be minimal.
The main gameplay implementation should focus on the `IN_GAME_*` states.

---

### 3.3 Per-Turn State Transition Detail

#### State: `IN_GAME_MORNING_BRIEFING`

**Input**

* current `GameState`
* previous day summary
* triggered overnight messages

**Output**

* UI-ready briefing payload
* transition to action selection

**Allowed mutations**

* none, except marking briefing as viewed

---

#### State: `IN_GAME_ACTION_SELECTION`

**Input**

* current `GameState`
* available player action pool
* temporary event-driven actions

**Output**

* selected player actions for the turn
* locked action submission payload

**Allowed mutations**

* temporary local selection state
* commit to `pendingTurn.playerActions` on confirm

---

#### State: `IN_GAME_AI_RESOLUTION`

**Input**

* committed player actions
* current `GameState`
* AI rules / weights

**Output**

* chosen AI response package
* explanation tags for briefing/report text

**Allowed mutations**

* commit to `pendingTurn.aiResponses`

---

#### State: `IN_GAME_TURN_RESOLUTION`

**Input**

* `GameState`
* selected player actions
* selected AI responses
* deterministic random seed

**Output**

* stat deltas
* system logs
* intermediate resolution result

**Allowed mutations**

* update core stats
* append resolution logs
* write derived effects to `pendingTurn.resolution`

---

#### State: `IN_GAME_EVENT_RESOLUTION`

**Input**

* updated post-resolution state
* event rules
* trigger conditions
* deterministic random seed

**Output**

* list of triggered events
* event deltas
* optional temporary actions for next turn

**Allowed mutations**

* apply event effects to stats
* append event records to turn history

---

#### State: `IN_GAME_END_OF_DAY_REPORT`

**Input**

* completed turn resolution
* triggered events
* current post-event state

**Output**

* report payload for UI
* summary text tokens / assembled text

**Allowed mutations**

* mark report as viewed

---

#### State: `IN_GAME_END_CHECK`

**Input**

* post-turn `GameState`
* ending rules
* phase progression rules

**Output**

* ending result or next-day progression result

**Allowed mutations**

* update conflict phase
* mark game as ended if any ending condition is met

---

#### State: `NEXT_DAY_SETUP`

**Input**

* resolved game state

**Output**

* incremented day counter
* cleared temporary turn state
* refreshed availability state for the next turn

**Allowed mutations**

* increment `day`
* reset `pendingTurn`
* generate next turn’s available action pool

---

## 4. Data Ownership Model

### 4.1 Authoritative Runtime Containers

The prototype should separate runtime state into four main layers:

1. **Session State**

   * menu state
   * screen state
   * current UI phase

2. **Game State**

   * authoritative simulation values
   * day count
   * phase
   * current stats
   * ending state

3. **Turn State**

   * player selections for the current day
   * AI responses for the current day
   * resolution outputs for the current day
   * triggered events for the current day

4. **Content Data**

   * action definitions
   * event definitions
   * ending definitions
   * phase rules
   * AI behavior tables

---

### 4.2 Ownership Rules

#### Session State owns

* what screen is visible
* what modal is open
* whether the player has confirmed a selection

#### Game State owns

* canonical stat values
* active phase
* total turn history
* active flags that persist across turns
* ending status

#### Turn State owns

* short-lived per-turn working data
* temporary calculations
* selected actions before and after resolution

#### Content Data owns

* authored definitions only
* no mutable runtime values

---

## 5. Core Data Contracts

The examples below use TypeScript-style notation for clarity. The implementation language may differ, but the contract intent should remain the same.

---

### 5.1 Enums and Primitive Types

```ts
type GameScreen =
  | "MAIN_MENU"
  | "MORNING_BRIEFING"
  | "ACTION_SELECTION"
  | "AI_RESOLUTION"
  | "TURN_RESOLUTION"
  | "EVENT_RESOLUTION"
  | "END_OF_DAY_REPORT"
  | "ENDING"
  | "POST_GAME_SUMMARY";

type ConflictPhase =
  | "CRISIS_BUILDUP"
  | "GRAY_ZONE"
  | "QUASI_BLOCKADE"
  | "LIMITED_STRIKE"
  | "FULL_BLOCKADE"
  | "ENDGAME";

type StatKey =
  | "tension"
  | "pressureEffect"
  | "internationalRisk"
  | "domesticStrain"
  | "opponentStability"
  | "readiness";

type ActionCategory =
  | "MILITARY"
  | "BLOCKADE"
  | "INFO_DIPLOMACY"
  | "DOMESTIC";

type AIResponseCategory =
  | "DELAY_DEESCALATE"
  | "REINFORCE_DEFENSE"
  | "SEEK_EXTERNAL_SUPPORT"
  | "BREAK_PRESSURE"
  | "LIMITED_COUNTERMEASURE"
  | "LEGITIMACY_PLAY";

type EndingType =
  | "COERCIVE_SUCCESS"
  | "COSTLY_SUCCESS"
  | "FROZEN_CRISIS_ADVANTAGE"
  | "INTERNATIONAL_ESCALATION"
  | "DOMESTIC_COLLAPSE"
  | "STRATEGIC_INEFFECTIVENESS"
  | "UNCONTROLLED_WAR_SPIRAL";
```

---

### 5.2 Core Stats Contract

```ts
interface CoreStats {
  tension: number;
  pressureEffect: number;
  internationalRisk: number;
  domesticStrain: number;
  opponentStability: number;
  readiness: number;
}
```

**Rules**

* All stat values are clamped to `0..100`
* Stat mutation should go through a shared utility such as `applyStatDelta()`
* All stat changes should be logged in turn history for debugging and end-of-day reporting

---

### 5.3 Game State Contract

```ts
interface GameState {
  sessionId: string;
  seed: number;
  day: number;
  maxDays: number;
  currentScreen: GameScreen;
  conflictPhase: ConflictPhase;
  stats: CoreStats;
  persistentFlags: Record<string, boolean>;
  activeModifiers: ModifierInstance[];
  history: TurnRecord[];
  pendingTurn: PendingTurnState | null;
  ending: EndingResult | null;
  isGameOver: boolean;
}
```

**Field notes**

* `seed`: used for deterministic replay and random resolution
* `persistentFlags`: tracks long-lived scenario state such as “escort pressure active” or “market panic active”
* `activeModifiers`: ongoing effects that persist across multiple turns
* `history`: append-only turn archive
* `pendingTurn`: working state for the currently active day

---

### 5.4 Pending Turn State Contract

```ts
interface PendingTurnState {
  turnNumber: number;
  availableActions: AvailableActionSet;
  playerActions: PlayerActionSelection[];
  aiResponses: AIResponseSelection[];
  baseResolution: ResolutionBundle | null;
  triggeredEvents: EventTriggerResult[];
  finalResolution: ResolutionBundle | null;
  report: EndOfDayReport | null;
}
```

**Purpose**
This object isolates the working state of the current day before its results are finalized into history.

---

### 5.5 Action Definition Contract

```ts
interface ActionDefinition {
  id: string;
  title: string;
  category: ActionCategory;
  phaseAvailability: ConflictPhase[];
  description: string;
  uiTags: string[];
  costs?: Partial<Record<StatKey, number>>;
  effects: StatDelta[];
  requirements?: RequirementRule[];
  grantsFlags?: string[];
  removesFlags?: string[];
  weightTags?: string[];
}
```

**Notes**

* `effects` defines direct stat deltas or derived effect references
* `requirements` supports gating by phase, stat thresholds, or flags
* authored action data should not contain runtime state

---

### 5.6 Player Action Selection Contract

```ts
interface PlayerActionSelection {
  actionId: string;
  lockedAtStep: number;
}
```

This stays intentionally small. Full action metadata should be resolved from content tables, not duplicated in runtime turn state.

---

### 5.7 AI Response Definition Contract

```ts
interface AIResponseDefinition {
  id: string;
  category: AIResponseCategory;
  title: string;
  description: string;
  triggerWeights: WeightRule[];
  effects: StatDelta[];
  grantsFlags?: string[];
  removesFlags?: string[];
  explanationTags?: string[];
}
```

---

### 5.8 AI Response Selection Contract

```ts
interface AIResponseSelection {
  responseId: string;
  score: number;
  category: AIResponseCategory;
}
```

**Purpose**
Stores the chosen AI response and enough metadata to explain selection during debugging or balancing.

---

### 5.9 Event Definition Contract

```ts
interface EventDefinition {
  id: string;
  title: string;
  description: string;
  phaseAvailability?: ConflictPhase[];
  triggerRules: TriggerRule[];
  probability?: number;
  effects: StatDelta[];
  grantsFlags?: string[];
  removesFlags?: string[];
  temporaryActions?: string[];
  priority?: number;
}
```

**Notes**

* Events may be purely informational or may mutate stats/flags
* `priority` helps resolve ordering if multiple events trigger in the same turn
* `temporaryActions` can inject one-turn options into the next action pool

---

### 5.10 Event Trigger Result Contract

```ts
interface EventTriggerResult {
  eventId: string;
  applied: boolean;
  resultingDeltas: StatDelta[];
  grantedFlags: string[];
  removedFlags: string[];
}
```

---

### 5.11 Resolution Bundle Contract

```ts
interface ResolutionBundle {
  statDeltas: StatDelta[];
  finalStats: CoreStats;
  appliedFlags: string[];
  removedFlags: string[];
  logEntries: ResolutionLogEntry[];
}
```

This bundle is used both for intermediate and final turn results.

---

### 5.12 Stat Delta Contract

```ts
interface StatDelta {
  stat: StatKey;
  amount: number;
  sourceType: "ACTION" | "AI" | "EVENT" | "MODIFIER" | "SYSTEM";
  sourceId: string;
}
```

**Rules**

* Every stat mutation should be attributable
* This contract is important for UI tooltips, debugging, and report generation

---

### 5.13 Modifier Instance Contract

```ts
interface ModifierInstance {
  id: string;
  sourceId: string;
  title: string;
  remainingDays: number;
  effectsPerTurn: StatDelta[];
  tags?: string[];
}
```

**Purpose**
Represents multi-turn effects such as “market panic” or “escort pressure”.

---

### 5.14 Requirement Rule Contract

```ts
interface RequirementRule {
  type: "MIN_STAT" | "MAX_STAT" | "HAS_FLAG" | "LACKS_FLAG" | "PHASE_IS";
  stat?: StatKey;
  value?: number;
  flag?: string;
  phase?: ConflictPhase;
}
```

---

### 5.15 Trigger Rule Contract

```ts
interface TriggerRule {
  type: "MIN_STAT" | "MAX_STAT" | "HAS_FLAG" | "DAY_AT_LEAST" | "PHASE_IS";
  stat?: StatKey;
  value?: number;
  flag?: string;
  day?: number;
  phase?: ConflictPhase;
}
```

---

### 5.16 Weight Rule Contract

```ts
interface WeightRule {
  type: "STAT_RANGE" | "PLAYER_USED_CATEGORY" | "HAS_FLAG" | "PHASE_IS";
  stat?: StatKey;
  min?: number;
  max?: number;
  category?: ActionCategory;
  flag?: string;
  phase?: ConflictPhase;
  weight: number;
}
```

This allows the AI to evaluate responses in a data-driven way without requiring heavy procedural logic.

---

### 5.17 Turn Record Contract

```ts
interface TurnRecord {
  turnNumber: number;
  phaseAtStart: ConflictPhase;
  statsAtStart: CoreStats;
  playerActions: PlayerActionSelection[];
  aiResponses: AIResponseSelection[];
  triggeredEvents: EventTriggerResult[];
  resolution: ResolutionBundle;
  phaseAtEnd: ConflictPhase;
  statsAtEnd: CoreStats;
  report: EndOfDayReport;
}
```

---

### 5.18 Ending Result Contract

```ts
interface EndingResult {
  type: EndingType;
  title: string;
  description: string;
  causes: string[];
  summaryStats: Partial<CoreStats>;
  triggeredOnDay: number;
}
```

---

### 5.19 End-of-Day Report Contract

```ts
interface EndOfDayReport {
  headline: string;
  summaryLines: string[];
  highlights: string[];
  statChanges: StatDelta[];
  aiSummaryTags: string[];
  eventSummaryTags: string[];
}
```

This payload should be UI-ready so the report screen can render without recomputing simulation logic.

---

### 5.20 Available Action Set Contract

```ts
interface AvailableActionSet {
  primary: string[];
  secondary: string[];
  infoDiplomacy: string[];
  temporary: string[];
}
```

The values are action IDs only. UI and logic should look up full definitions from content tables.

---

## 6. Turn Processing Pipeline

### 6.1 Pipeline Order

A single turn should be processed in the following order:

1. Generate available actions
2. Accept player action selections
3. Evaluate AI response candidates
4. Select AI response package
5. Apply player action effects
6. Apply AI response effects
7. Apply active modifier effects
8. Resolve event triggers
9. Apply event effects
10. Clamp stats
11. Check conflict phase progression
12. Check endings
13. Build end-of-day report
14. Archive `TurnRecord`
15. Prepare next turn

This order should remain fixed unless there is a deliberate design change.

---

### 6.2 Why This Order Matters

* Player actions should define the primary direction of a turn.
* AI responses should react to the player, not precede them.
* Ongoing modifiers should apply before event triggering if they are intended to help create trigger thresholds.
* Endings should be checked only after all daily changes are fully applied.
* Reporting should happen after the simulation is final for the day.

---

## 7. Validation Rules

### 7.1 Hard Validation

The runtime should reject or guard against:

* invalid action IDs
* duplicate actions where duplicates are not allowed
* actions selected outside their allowed category
* state transitions that skip required phases
* null final resolution entering archive
* stat values outside `0..100`

### 7.2 Soft Validation

The runtime should log warnings for:

* empty AI response sets
* events with conflicting flag mutations
* missing report tags for important outcomes
* undefined temporary actions referenced by events

---

## 8. Persistence Boundaries

### 8.1 Minimum Save Contract

For prototype save/load support, the minimum persisted payload is:

* `GameState`
* content version identifier
* RNG seed and progression state

### 8.2 Non-Persisted Data

The following should be reconstructable and do not need separate persistence:

* resolved action definitions
* resolved event definitions
* derived UI view models

---

## 9. UI Integration Contract

### 9.1 UI Should Read, Not Simulate

The UI layer should consume prepared view data and dispatch player intent. It should not perform gameplay calculations.

### 9.2 View Model Recommendation

For each major screen, create a small derived view model from `GameState` and `pendingTurn`, for example:

* `MorningBriefingViewModel`
* `ActionSelectionViewModel`
* `EndOfDayReportViewModel`
* `EndingViewModel`

This keeps simulation logic separate from presentation logic.

---

## 10. Example Minimal State Snapshot

```ts
const gameState: GameState = {
  sessionId: "run_001",
  seed: 17291,
  day: 4,
  maxDays: 20,
  currentScreen: "ACTION_SELECTION",
  conflictPhase: "GRAY_ZONE",
  stats: {
    tension: 28,
    pressureEffect: 18,
    internationalRisk: 16,
    domesticStrain: 12,
    opponentStability: 79,
    readiness: 54,
  },
  persistentFlags: {
    marketPanic: false,
    escortPressure: false,
    legitimacyCampaignActive: true,
  },
  activeModifiers: [],
  history: [],
  pendingTurn: {
    turnNumber: 4,
    availableActions: {
      primary: ["expand_exercise_zone", "joint_patrol"],
      secondary: ["raise_readiness", "stabilize_market"],
      infoDiplomacy: ["issue_warning", "signal_negotiation"],
      temporary: [],
    },
    playerActions: [],
    aiResponses: [],
    baseResolution: null,
    triggeredEvents: [],
    finalResolution: null,
    report: null,
  },
  ending: null,
  isGameOver: false,
};
```

---

## 11. Implementation Summary

This technical slice defines:

* a fixed and deterministic **state flow** for the daily turn loop
* a single authoritative **GameState** with isolated per-turn working state
* data-driven **contracts** for actions, AI responses, events, modifiers, reports, and endings
* clean separation between simulation logic and UI presentation

The intended result is a prototype architecture that is:

* easy to debug
* easy to balance
* readable to implement
* extensible enough for future scenario growth without overengineering the first build
