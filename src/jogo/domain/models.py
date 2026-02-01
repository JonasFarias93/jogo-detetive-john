from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class PlayerStats:
    sono: int = 65
    energia: int = 55
    foco: int = 70
    estresse: int = 30

    def apply(self, *, sono: int = 0, energia: int = 0, foco: int = 0, estresse: int = 0) -> None:
        self.sono += sono
        self.energia += energia
        self.foco += foco
        self.estresse += estresse


@dataclass(frozen=True)
class Choice:
    key: str
    label: str
    goto: str
    hint: str = ""
    enabled: bool = True


@dataclass(frozen=True)
class GameState:
    chapter_id: str
    scene_id: str
    text: str
    image_path: str
    choices: List[Choice] = field(default_factory=list)
    stats: PlayerStats = field(default_factory=PlayerStats)
