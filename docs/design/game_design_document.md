# Game Design Document

## Document Info
- File path: `docs/design/game_design_document.md`
- Project codename: `Strait: Critical Days`
- Scope of this section: Turn Loop, Win/Loss Conditions, Core Systems
- Target build: Prototype v0.1

---

## Workflow Note

- Read this document before changing gameplay rules.
- If a change affects turn logic, combat, supply, or victory rules, update this document together with `docs/design/technical_design.md` and `docs/tasks/backlog.md`.
- Every rule change must be covered by:
  - at least one deterministic test proving the same seed and actions produce the same result
  - at least one rules-focused test covering isolated rule behavior or edge cases
- Log notable rule decisions in `docs/logs/devlog.md` using the fields `Why`, `What Changed`, and `Result`.

---

## 1. Design Goals
This document section defines the core playable structure for a **Flash-style, minimalist UI, single-player, turn-based strategy narrative game** in which **1 turn = 1 day**.

The design goals for this slice are:
1. **Few but meaningful decisions per turn**: the player should make a small number of high-impact choices each day.
2. **Clear end-of-day feedback**: most consequences should resolve at the end of the turn to create a strong daily rhythm.
3. **Limited system count, strong system interaction**: the prototype should remain readable while still producing strategic tension.
4. **Composite outcomes instead of simple military victory**: success and failure should emerge from political, military, economic, and escalation dynamics together.

---

## 2. Turn Loop

### 2.1 Time Unit
- 1 turn = 1 day
- Standard match length: 20–40 days
- Recommended prototype length: 20 days

### 2.2 Daily Turn Structure
Each day is divided into 6 fixed steps.

#### Step 1: Morning Briefing
The system presents a concise summary of what happened during the previous day.

**Displayed information**
- Current date / turn number (`Day X`)
- Current conflict phase
- Key stat changes from yesterday
- Summary of overnight developments
- Assessment of the opponent’s previous action

**Purpose**
- Compress the previous turn into a readable situational overview
- Ensure the player understands the state of play before acting

**Recommended presentation**
- 1 short briefing paragraph (2–4 sentences)
- Arrow indicators for core stat changes
- Optional pop-up event card if a major incident occurred

---

#### Step 2: Player Decision Phase
The player chooses actions for the current day.

**Recommended rule set**
- Choose:
  - 1 Primary Action
  - 1 Secondary Action
  - 1 Information / Diplomatic Action
- Maximum total actions per turn: 3

**Action sources**
- Actions unlocked by the current conflict phase
- Temporary actions granted by events
- Actions gated by system thresholds (for example, readiness level)

**Purpose**
- Keep decision space readable
- Increase the weight of each choice
- Emphasize political judgment under constrained options

---

#### Step 3: AI Response Phase
The AI opponent reacts to the player’s decisions based on the current state of the match.

**Example AI response categories**
- Delay and de-escalate
- Reinforce defenses
- Seek external support
- Attempt to break pressure / blockade conditions
- Conduct limited countermeasures
- Lower visible tension to gain legitimacy

**Purpose**
- Preserve a sense of active opposition
- Make the player feel they are in a live strategic contest rather than pushing static numbers

**Implementation recommendation**
- Use a rule-weighted AI rather than deep simulation
- AI behavior should be influenced by:
  - Current conflict phase
  - Player action categories used this turn
  - Current core stat levels
  - Triggered events

---

#### Step 4: System Resolution
The game resolves all major numerical outcomes for the day.

**Resolved values**
- Tension
- Pressure Effect
- International Risk
- Domestic Strain
- Opponent Stability
- Readiness
- Conflict phase progression checks

**Purpose**
- Close the cause-and-effect loop for the day
- Make the turn feel complete and legible

**Implementation recommendation**
1. Apply base effects from player actions
2. Apply AI response modifiers
3. Apply event modifiers
4. Run threshold checks and phase progression

---

#### Step 5: Event Trigger Phase
The system checks for random, conditional, and threshold-based events.

**Event sources**
- Phase-specific scripted events
- Random incidents
- High-risk threshold events
- Chain events caused by previous choices

**Purpose**
- Prevent the game from feeling mechanically repetitive
- Introduce uncertainty and crisis texture
- Reinforce the narrative of a volatile strategic environment

**Example event types**
- Maritime insurance premiums spike
- Neutral merchant vessel enters a restricted zone
- Port scheduling systems malfunction
- External powers call for restraint
- Escort flotilla approaches the area
- Domestic market panic intensifies

---

#### Step 6: End-of-Day Report
The day concludes with a short report summarizing the strategic effect of the player’s choices.

**Report content should include**
- The main effect of today’s actions
- Whether the opponent’s response was effective
- Whether systemic risk increased or decreased
- The likely strategic direction going into tomorrow

**Purpose**
- Give emotional and narrative closure to the turn
- Reinforce continuity between days
- Prime the player for the next decision cycle

---

### 2.3 Target Feeling of a Good Turn
A successful turn should leave the player with the following impressions:
1. I understand today’s situation.
2. I had to trade one risk against another.
3. My actions clearly changed the state of play.
4. The opponent is adapting.
5. The conflict is moving closer to a specific outcome path.

---

## 3. Win / Loss Conditions

### 3.1 Design Principle
The game should not use a single binary “military victory” condition. Instead, it should use **composite outcomes**.

**Core principle**
- Tactical success does not automatically equal strategic success.
- Limited coercion may be more successful than uncontrolled escalation.
- Failure often comes not from battlefield defeat alone, but from loss of control, excessive cost, or strategic ineffectiveness.

---

### 3.2 Primary Win Conditions

#### Win Type A: Coercive Success
**Logic**
- Pressure Effect reaches a high threshold
- Opponent Stability falls to a low threshold
- International Risk remains below the uncontrollable escalation threshold
- The player retains acceptable internal resilience and readiness

**Meaning**
- The player achieves political leverage through sustained pressure without triggering total strategic collapse
- This is the cleanest and most desirable win state

**Suggested benchmark values**
- Pressure Effect >= 75
- Opponent Stability <= 25
- International Risk < 80
- Domestic Strain < 85

---

#### Win Type B: Costly Success
**Logic**
- The player achieves core objectives
- But either International Risk or Domestic Strain is near critical levels

**Meaning**
- The player technically succeeds, but at dangerously high cost
- This should be presented as a compromised or second-tier victory state

**Suggested benchmark values**
- Pressure Effect >= 80
- Opponent Stability <= 20
- And either:
  - International Risk >= 80, or
  - Domestic Strain >= 80

---

#### Win Type C: Frozen Crisis Advantage
**Logic**
- The game reaches the final day without a collapse state
- The player does not fully break the opponent
- But preserves a favorable high-pressure equilibrium

**Meaning**
- No decisive breakthrough occurs, but the player successfully shapes a harsher strategic status quo
- This is a realistic, non-perfect but valid win-adjacent outcome

**Suggested benchmark values**
- Final turn reached
- International Risk < 90
- Domestic Strain < 90
- Pressure Effect >= 55
- Opponent Stability <= 50

---

### 3.3 Primary Loss Conditions

#### Loss Type A: International Escalation Out of Control
**Logic**
- International Risk reaches maximum threshold
- Or major high-risk chains trigger wider intervention dynamics

**Meaning**
- The player fails to contain the conflict within the intended political and strategic frame
- This is the clearest “loss of control” failure state

**Suggested benchmark**
- International Risk >= 100

---

#### Loss Type B: Domestic Strain Collapse
**Logic**
- Prolonged pressure operations overwhelm the player’s internal capacity to sustain the crisis

**Meaning**
- The player’s external strategy remains incomplete, but internal economic, political, or social strain breaks first

**Suggested benchmark**
- Domestic Strain >= 100

---

#### Loss Type C: Strategic Ineffectiveness
**Logic**
- The player fails to generate lasting pressure
- The opponent remains broadly stable or recovers
- The game ends without meaningful coercive effect

**Meaning**
- The player acted repeatedly but failed to change the structure of the situation

**Suggested benchmark values**
- Final turn reached
- Pressure Effect < 45
- Opponent Stability > 60

---

#### Loss Type D: Uncontrolled War Spiral
**Logic**
- Tension reaches maximum threshold
- Combined with severe international danger and high-risk counter-escalation

**Meaning**
- The conflict has moved beyond the intended design scope of limited crisis management and into general strategic breakdown
- For the prototype, this should count as a failure ending

**Suggested benchmark values**
- Tension >= 100
- And International Risk >= 85

---

### 3.4 End-State Presentation Rules
Each ending should include:
- Ending title
- Short ending description
- Summary of the main causes that led to it
- 3 key statistics from the run

This supports replayability and strengthens post-game reflection.

---

## 4. Core Systems

For the prototype, the game should use **6 primary systems**. This is small enough to support a clean UI, but large enough to generate strong strategic interaction.

---

### 4.1 Tension

#### Definition
Represents how close the conflict is to open war, rapid escalation, or systemic loss of control.

#### Range
- 0–100

#### Functions
- Determines whether conflict phases can escalate
- Increases the probability of high-risk events
- Pushes AI behavior toward harder responses
- Gates access to certain high-intensity actions

#### Main sources of increase
- Expanding exercise zones
- Joint maritime / air pressure actions
- Precision strike escalation
- Ultimatum-style messaging
- Opponent military countermeasures

#### Main sources of decrease
- Negotiation signals
- Humanitarian corridor measures
- Restraint messaging
- AI de-escalation choices

#### Design note
Tension is not a reward stat. It is closer to a rising stake meter. Higher Tension unlocks stronger short-term options, but increases the chance of catastrophic loss states.

---

### 4.2 Pressure Effect

#### Definition
Represents how effectively the player is degrading the opponent’s logistical confidence, systemic stability, and strategic endurance.

#### Range
- 0–100

#### Functions
- Serves as the player’s main forward-progress stat
- Enables coercive outcomes when combined with low Opponent Stability
- Distinguishes meaningful pressure from symbolic posturing

#### Main sources of increase
- Vessel inspections
- Restricting energy flows
- Port and systems disruption
- Maritime / air pressure patrols
- Limited strike actions in later phases

#### Main sources of decrease
- Humanitarian carve-outs
- Voluntary de-escalation
- Successful opponent breakthrough actions
- External escort or support effects

#### Design note
Pressure Effect should always sit in tension with International Risk. The player should not be able to stack pressure without paying strategic cost.

---

### 4.3 International Risk

#### Definition
Represents the probability and severity of external diplomatic, economic, or military involvement.

#### Range
- 0–100

#### Functions
- High values push the game toward intervention or escalation loss states
- Mid-to-high values improve the opponent’s ability to seek outside support
- Changes available event pools, such as escort pressure, sanctions, and mediation

#### Main sources of increase
- Aggressive inspection regimes
- Expanded exclusion zones
- High-visibility coercive actions
- Precision strike escalation
- Civilian disruption incidents

#### Main sources of decrease
- Legal framing / legitimacy messaging
- Humanitarian exemptions
- Negotiation signals
- Visible restraint in response windows

#### Design note
International Risk is a control stat. The player is not trying to reduce it to zero, but must keep it below the level where outside dynamics overwhelm the original strategy.

---

### 4.4 Domestic Strain

#### Definition
Represents the internal economic, political, and social burden of sustaining the player’s strategy.

#### Range
- 0–100

#### Functions
- Acts as the internal endurance limit on prolonged high-pressure play
- Shapes end states related to overextension and self-inflicted collapse
- Encourages periodic stabilizing actions instead of endless escalation

#### Main sources of increase
- Sustained mobilization
- Industrial surge measures
- High-intensity military actions
- Economic disruption blowback
- Long-duration crisis without relief

#### Main sources of decrease
- Domestic stabilization policies
- Reduced operational tempo
- Narrative control / public reassurance measures
- Limited diplomatic cooling

#### Design note
Domestic Strain prevents the player from treating escalation as costless. It is the most important internal balancing mechanism in the prototype.

---

### 4.5 Opponent Stability

#### Definition
Represents the opponent’s ability to preserve social order, logistical continuity, political coherence, and strategic patience.

#### Range
- 0–100

#### Functions
- Serves as the main defensive endurance stat for the AI side
- Must be reduced, directly or indirectly, to achieve coercive success endings
- Influences the opponent’s AI posture and event responses

#### Main sources of decrease
- Effective pressure operations
- Energy and shipping disruption
- Repeated systemic incidents
- Successful information pressure
- Limited strike effects in later phases

#### Main sources of increase
- Successful external support
- AI defensive recovery measures
- Failed player escalation
- Stabilization events

#### Design note
Opponent Stability should not collapse too quickly. The intended pacing is slow erosion under sustained pressure, not rapid depletion in only a few turns.

---

### 4.6 Readiness

#### Definition
Represents the player’s capacity to sustain and escalate operations if needed.

#### Range
- 0–100

#### Functions
- Unlocks certain higher-level actions
- Buffers against failed escalation attempts
- Supports strategic flexibility when the situation shifts rapidly

#### Main sources of increase
- Mobilization measures
- Readiness drills
- Industrial and logistical preparation
- Early low-visibility preparation actions

#### Main sources of decrease
- Continuous high-tempo action
- Resource-intensive escalatory decisions
- Long crisis duration without recovery

#### Design note
Readiness is not the same as victory progress. It is an enabling stat. Players should sometimes invest in it early in order to preserve options later.

---

## 5. System Relationships

The prototype’s strategic depth depends on the interaction of these six systems.

### 5.1 Core Relationship Model
- **Raising Pressure Effect** usually also raises **International Risk** and **Tension**.
- **Lowering Opponent Stability** often requires actions that increase **Domestic Strain**.
- **Reducing Tension** may improve control, but can also weaken **Pressure Effect**.
- **Building Readiness** improves future options, but often increases **Domestic Strain** in the short term.
- **Ignoring International Risk** can invalidate otherwise strong progress.
- **Ignoring Domestic Strain** can turn an apparently successful campaign into internal failure.

### 5.2 Intended Strategic Tradeoff
The central question of the game should be:

> How much pressure can the player apply before political control, international restraint, and domestic sustainability begin to fail?

This is the main balancing philosophy behind the turn loop and win/loss structure.

---

## 6. Prototype Implementation Notes

For the first playable prototype, this section should be implemented with the following priorities:

### Must Have
- 20-day turn structure
- Morning Briefing -> Player Actions -> AI Response -> Resolution -> Events -> End-of-Day Report flow
- 6 core stats fully functional
- At least 3 win states and 4 loss states
- Conflict phase progression driven by thresholds

### Should Have
- End-of-run summary screen with key metrics
- Distinct AI response categories
- Event cards tied to high-risk thresholds

### Can Wait
- Advanced phase-specific modifiers
- Multi-faction diplomacy modeling
- Detailed map-state simulation
- Deep scenario scripting beyond the prototype scope

---

## 7. Summary
This design slice defines the playable backbone of the game:
- A **daily turn loop** built around concise, high-stakes decisions
- **Composite win/loss conditions** centered on control, pressure, and sustainability
- A **minimal but strongly interactive system set** suitable for a clean Flash-style strategy UI

The result should feel readable, tense, and replayable, with each day pushing the player closer to either controlled coercive success or uncontrolled strategic failure.

---

## 2026-03-31 Prototype v0.2 Rules Snapshot (Playable CLI)

为支持“立即可玩”目标，当前版本落地了最小闭环规则：

- 回合长度：20 天（可配置）。
- 每日强制选择 3 个行动：`primary` + `secondary` + `info` 各 1 个。
- 行动、AI 响应、事件共同影响六项核心数值：
  - Tension
  - Pressure Effect
  - International Risk
  - Domestic Strain
  - Opponent Stability
  - Readiness
- 冲突阶段由 Tension 阈值推进：
  - `<40`: STANDOFF
  - `40-64`: PRESSURE
  - `65-84`: CRISIS
  - `>=85`: PRE_WAR
- 终局判定优先级：
  1. 国际失控升级
  2. 内部承压失衡
  3. 威慑达成
  4. 高成本达成
  5. 超时后冻结优势 / 战略失效

该版本强调“可玩 + 可复现 + 可扩展”，后续再逐步加入更细化战术战斗与补给系统。
