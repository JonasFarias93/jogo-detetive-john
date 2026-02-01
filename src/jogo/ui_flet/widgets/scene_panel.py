from __future__ import annotations

import flet as ft

from jogo.domain import GameState
from .common import card


class ScenePanel:
    def __init__(self) -> None:
        self._img = ft.Image(src="", fit=ft.BoxFit.CONTAIN, expand=True)
        self._img_container = ft.Container(self._img, padding=ft.Padding(top=6), expand=True)

        self.control = card("Cena", self._img_container, expand=True)

    def render(self, state: GameState) -> None:
        self._img.src = state.image_path if state.image_path else ""
        self._img.visible = bool(state.image_path)
