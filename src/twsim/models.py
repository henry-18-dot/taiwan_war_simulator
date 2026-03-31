from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ActionSlot(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    INFO = "info"


@dataclass(frozen=True)
class ActionDef:
    key: str
    slot: ActionSlot
    label: str
    description: str
    tension: int
    pressure: int
    risk: int
    strain: int
    readiness: int
    opponent_stability: int


@dataclass
class Stats:
    tension: int = 35
    pressure_effect: int = 15
    international_risk: int = 20
    domestic_strain: int = 20
    opponent_stability: int = 70
    readiness: int = 50

    def clamp(self) -> None:
        for field_name in (
            "tension",
            "pressure_effect",
            "international_risk",
            "domestic_strain",
            "opponent_stability",
            "readiness",
        ):
            value = getattr(self, field_name)
            setattr(self, field_name, min(100, max(0, value)))


@dataclass
class TurnRecord:
    day: int
    player_actions: list[str]
    ai_response: str
    event: str
    summary: str
    stats_after: Stats


@dataclass
class GameState:
    day: int = 1
    max_days: int = 20
    phase: str = "STANDOFF"
    ended: bool = False
    ending: str | None = None
    seed: int = 7
    stats: Stats = field(default_factory=Stats)
    history: list[TurnRecord] = field(default_factory=list)


@dataclass(frozen=True)
class EndingRule:
    key: str
    label: str
    description: str
