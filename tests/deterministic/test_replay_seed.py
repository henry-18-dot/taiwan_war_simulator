from twsim.engine import resolve_turn
from twsim.models import GameState

SCRIPTED_ACTIONS = [
    ["precision_patrol", "cyber_probe", "info_campaign"],
    ["naval_drill", "logistics_recovery", "diplomatic_signal"],
    ["precision_patrol", "cyber_probe", "diplomatic_signal"],
    ["naval_drill", "cyber_probe", "info_campaign"],
]


def run(seed: int):
    state = GameState(seed=seed)
    for actions in SCRIPTED_ACTIONS:
        if state.ended:
            break
        resolve_turn(state, actions)
    return (
        state.day,
        state.phase,
        state.ending,
        state.stats.tension,
        state.stats.pressure_effect,
        state.stats.international_risk,
        state.stats.domestic_strain,
        state.stats.opponent_stability,
        state.stats.readiness,
        [(r.ai_response, r.event) for r in state.history],
    )


def test_same_seed_same_result():
    assert run(42) == run(42)


def test_different_seed_different_timeline():
    assert run(42) != run(43)
