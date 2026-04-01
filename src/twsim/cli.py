from __future__ import annotations

import argparse

from twsim.engine import RuleError, available_actions, ending_label, resolve_turn
from twsim.models import ActionSlot, GameState
from twsim.visual_style import visual_style_prompt


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Strait: Critical Days CLI")
    parser.add_argument("--seed", type=int, default=7, help="随机种子")
    parser.add_argument("--max-days", type=int, default=20, help="最大天数")
    parser.add_argument(
        "--visual-style-prompt",
        action="store_true",
        help="输出游戏视觉与渲染风格提示词（用于美术/UI/前端协作）",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.visual_style_prompt:
        print(visual_style_prompt())
        return
    run_game(seed=args.seed, max_days=args.max_days)


if __name__ == "__main__":
    main()
