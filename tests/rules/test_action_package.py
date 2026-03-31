import pytest

from twsim.engine import RuleError, available_actions, evaluate_ending, resolve_turn, validate_action_package
from twsim.models import ActionSlot, GameState, Stats


def test_action_package_requires_three_slots():
    with pytest.raises(RuleError):
        validate_action_package(["naval_drill", "cyber_probe"])


def test_action_package_rejects_duplicate_slots():
    with pytest.raises(RuleError):
        validate_action_package(["naval_drill", "precision_patrol", "info_campaign"])


def test_evaluate_ending_priority_is_escalation_first():
    state = GameState(stats=Stats(international_risk=95, pressure_effect=90, opponent_stability=10))
    assert evaluate_ending(state) == "international_escalation"


def test_each_action_slot_has_expanded_content_pool():
    assert len(available_actions(ActionSlot.PRIMARY)) >= 5
    assert len(available_actions(ActionSlot.SECONDARY)) >= 5
    assert len(available_actions(ActionSlot.INFO)) >= 6


def test_turn_summary_uses_localized_ai_label():
    state = GameState(stats=Stats(international_risk=75))
    record = resolve_turn(state, ["precision_patrol", "cyber_probe", "diplomatic_signal"])
    assert "外部降温与内线整补" in record.summary
    assert "deescalate" not in record.summary
