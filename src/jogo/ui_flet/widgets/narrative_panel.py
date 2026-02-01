from __future__ import annotations

import flet as ft

from jogo.domain import GameState
from .common import card


class NarrativePanel:
    """
    Painel de narrativa com scroll correto (barra no limite direito do card).
    Fix: usar ListView como host do scroll.
    """

    def __init__(self) -> None:
        self._text = ft.Text(value="", selectable=True, size=14, no_wrap=False)

        self._scroll = ft.ListView(
            expand=True,
            spacing=0,
            padding=ft.padding.only(top=6, right=8, bottom=6),
            controls=[self._text],
            auto_scroll=False,
        )

        self.control = card("Narrativa", self._scroll, expand=True)

    def render(self, state: GameState) -> None:
        self._text.value = (state.text or "").strip()
