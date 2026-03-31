from twsim.engine import evaluate_ending
from twsim.models import GameState, Stats


def test_coercive_success_thresholds():
    state = GameState(
        stats=Stats(
            pressure_effect=78,
            opponent_stability=24,
            international_risk=70,
            domestic_strain=70,
        )
    )
    assert evaluate_ending(state) == "coercive_success"


def test_timeout_strategic_failure():
    state = GameState(stats=Stats(pressure_effect=40, opponent_stability=65, international_risk=40))
    assert evaluate_ending(state, force_timeout=True) == "strategic_failure"
