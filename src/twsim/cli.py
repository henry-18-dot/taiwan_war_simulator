from __future__ import annotations

from twsim.engine import RuleError, available_actions, ending_label, resolve_turn
from twsim.models import ActionSlot, GameState


def choose(slot: ActionSlot) -> str:
    actions = available_actions(slot)
    print(f"\n请选择 {slot.value} 行动:")
    for index, action in enumerate(actions, start=1):
        print(f"  {index}. {action.label} ({action.key}) - {action.description}")
    while True:
        raw = input("输入编号: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(actions):
            return actions[int(raw) - 1].key
        print("无效输入，请重试。")


def print_stats(state: GameState) -> None:
    s = state.stats
    print(
        "\n[状态] "
        f"阶段={state.phase} | 紧张={s.tension} 压制={s.pressure_effect} 国际风险={s.international_risk} "
        f"内压={s.domestic_strain} 对手稳定={s.opponent_stability} 战备={s.readiness}"
    )


def run_game(seed: int = 7, max_days: int = 20) -> GameState:
    state = GameState(seed=seed, max_days=max_days)
    print("=== Strait: Critical Days (CLI 可玩原型) ===")
    while not state.ended and state.day <= state.max_days:
        print(f"\n===== Day {state.day} =====")
        print_stats(state)

        picks = [choose(ActionSlot.PRIMARY), choose(ActionSlot.SECONDARY), choose(ActionSlot.INFO)]
        try:
            record = resolve_turn(state, picks)
        except RuleError as exc:
            print(f"规则错误: {exc}")
            continue
        print(f"\n[日报] {record.summary}")

    print("\n=== 终局 ===")
    if state.ending:
        print(f"结果: {ending_label(state.ending)} ({state.ending})")
    else:
        print("结果: 未定义")
    print_stats(state)
    return state


if __name__ == "__main__":
    run_game()
