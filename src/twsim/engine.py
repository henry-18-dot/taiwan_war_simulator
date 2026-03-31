from __future__ import annotations

import random
from dataclasses import replace

from twsim.content import ACTIONS, AI_RESPONSE_LABELS, AI_RESPONSES, ENDINGS, EVENTS
from twsim.models import ActionDef, ActionSlot, GameState, Stats, TurnRecord


class RuleError(ValueError):
    pass


def available_actions(slot: ActionSlot) -> list[ActionDef]:
    return [action for action in ACTIONS.values() if action.slot == slot]


def validate_action_package(action_keys: list[str]) -> list[ActionDef]:
    if len(action_keys) != 3:
        raise RuleError("每回合必须恰好提交 3 个行动（主/次/信息各 1）。")
    actions = [ACTIONS[key] for key in action_keys]
    slots = {action.slot for action in actions}
    if slots != {ActionSlot.PRIMARY, ActionSlot.SECONDARY, ActionSlot.INFO}:
        raise RuleError("行动组合非法：必须包含 primary / secondary / info 各一个。")
    return actions


def select_ai_response(state: GameState, action_defs: list[ActionDef], rng: random.Random) -> str:
    aggression = sum(action.tension + action.risk for action in action_defs)
    if state.stats.international_risk >= 70:
        return "deescalate"
    if aggression >= 20:
        return "counter_pressure" if rng.random() > 0.35 else "defensive_reinforce"
    return "defensive_reinforce" if rng.random() > 0.45 else "deescalate"


def resolve_turn(state: GameState, action_keys: list[str]) -> TurnRecord:
    if state.ended:
        raise RuleError("游戏已结束，无法继续回合。")

    actions = validate_action_package(action_keys)
    rng = random.Random(state.seed + state.day * 97)
    ai = select_ai_response(state, actions, rng)

    stats = replace(state.stats)
    for action in actions:
        stats.tension += action.tension
        stats.pressure_effect += action.pressure
        stats.international_risk += action.risk
        stats.domestic_strain += action.strain
        stats.readiness += action.readiness
        stats.opponent_stability += action.opponent_stability

    ai_delta = AI_RESPONSES[ai]
    stats.tension += ai_delta["tension"]
    stats.international_risk += ai_delta["risk"]
    stats.pressure_effect += ai_delta["pressure"]
    stats.opponent_stability += ai_delta["opp"]

    event_name, event_delta = EVENTS[rng.randrange(0, len(EVENTS))]
    stats.tension += event_delta.get("tension", 0)
    stats.international_risk += event_delta.get("risk", 0)
    stats.domestic_strain += event_delta.get("strain", 0)
    stats.readiness += event_delta.get("readiness", 0)

    stats.clamp()
    state.stats = stats

    ai_label = AI_RESPONSE_LABELS.get(ai, ai)
    summary = (
        f"D{state.day}: 你执行 {', '.join(a.label for a in actions)}；"
        f"对手采取 {ai_label}；事件：{event_name}。"
    )
    record = TurnRecord(
        day=state.day,
        player_actions=action_keys,
        ai_response=ai,
        event=event_name,
        summary=summary,
        stats_after=replace(stats),
    )
    state.history.append(record)
    state.phase = advance_phase(stats)
    evaluate_ending(state)
    state.day += 1
    if state.day > state.max_days and not state.ended:
        evaluate_ending(state, force_timeout=True)
    return record


def advance_phase(stats: Stats) -> str:
    if stats.tension < 40:
        return "STANDOFF"
    if stats.tension < 65:
        return "PRESSURE"
    if stats.tension < 85:
        return "CRISIS"
    return "PRE_WAR"


def evaluate_ending(state: GameState, force_timeout: bool = False) -> str | None:
    s = state.stats
    if s.international_risk >= 90:
        return _set_ending(state, "international_escalation")
    if s.domestic_strain >= 90 and s.readiness <= 30:
        return _set_ending(state, "domestic_collapse")
    if s.pressure_effect >= 75 and s.opponent_stability <= 25 and s.international_risk < 80 and s.domestic_strain < 85:
        return _set_ending(state, "coercive_success")
    if s.pressure_effect >= 75 and s.opponent_stability <= 30:
        return _set_ending(state, "costly_success")
    if force_timeout:
        if s.pressure_effect >= 60 and s.opponent_stability <= 40 and s.international_risk < 85:
            return _set_ending(state, "frozen_advantage")
        return _set_ending(state, "strategic_failure")
    return None


def _set_ending(state: GameState, key: str) -> str:
    state.ended = True
    state.ending = key
    return key


def ending_label(key: str) -> str:
    return next(rule.label for rule in ENDINGS if rule.key == key)
