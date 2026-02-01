from __future__ import annotations

from dataclasses import replace
from typing import Optional

from jogo.content import registry
from jogo.domain.models import Choice, GameState, PlayerStats


class GameEngine:
    """
    Engine mínima:
    - Carrega cenas via registry (manifest.json)
    - Mantém stats em memória
    - Escolhas aplicam efeitos e mudam a cena
    """

    def __init__(self, *, chapter_id: str, stats: Optional[PlayerStats] = None):
        self.chapter_id = chapter_id
        self.stats = stats or PlayerStats()
        self.scene_id = registry.get_entry_scene_id(chapter_id)

    def start(self) -> GameState:
        return self._build_state(self.scene_id)

    def choose(self, action_key: str) -> GameState:
        scene = registry.get_scene(self.chapter_id, self.scene_id)

        action = next((a for a in scene.actions if a.key == action_key), None)
        if action is None:
            # não explode: só re-renderiza a mesma cena
            return self._build_state(self.scene_id)

        # aplica efeitos
        self.stats.apply(
            sono=action.effects.sono,
            energia=action.effects.energia,
            foco=action.effects.foco,
            estresse=action.effects.estresse,
        )

        # navega para próxima cena
        self.scene_id = action.goto
        return self._build_state(self.scene_id)

    def _build_state(self, scene_id: str) -> GameState:
        scene = registry.get_scene(self.chapter_id, scene_id)

        choices = [
            Choice(
                key=a.key,
                label=a.label,
                goto=a.goto,
                hint=a.hint,
                enabled=True,
            )
            for a in scene.actions
        ]

        # snapshot para evitar UI mutar engine
        stats_snapshot = replace(self.stats)

        return GameState(
            chapter_id=self.chapter_id,
            scene_id=scene.id,
            text=scene.text,
            image_path=scene.image,
            choices=choices,
            stats=stats_snapshot,
        )
