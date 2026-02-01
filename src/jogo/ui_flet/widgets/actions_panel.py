from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Callable, Optional

import flet as ft

from jogo.domain import GameState
from .common import card


@dataclass
class _TypingJob:
    task: Optional[asyncio.Task] = None


class ActionsPanel:
    """
    Rodapé em 3 colunas:
      [ AÇÕES (scroll) | CONFIG | DICAS (scroll + typewriter) ]

    Fix principal:
    - Trocar Column(scroll=...) por ListView(expand=True)
      => scrollbar vai pro limite direito do painel (e não “no meio”).
    """

    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self._typing = _TypingJob()

        # --------------------
        # Ações (ListView)
        # --------------------
        self._actions_lv = ft.ListView(
            expand=True,
            spacing=8,
            padding=ft.padding.only(top=6, right=8, bottom=6),
            auto_scroll=False,
        )

        # --------------------
        # Config (ListView)
        # --------------------
        self._config_lv = ft.ListView(
            expand=True,
            spacing=8,
            padding=ft.padding.only(top=6, right=8, bottom=6),
            auto_scroll=False,
        )

        # --------------------
        # Dicas (ListView + typewriter)
        # --------------------
        self._hint_text = ft.Text(value="", size=13, no_wrap=False)
        self._hint_lv = ft.ListView(
            expand=True,
            spacing=0,
            padding=ft.padding.only(top=6, right=8, bottom=6),
            controls=[self._hint_text],
            auto_scroll=False,
        )

        # Cards
        self._col_actions = card("Ações", self._actions_lv, expand=True)
        self._col_config = card("Config", self._config_lv, expand=False)
        self._col_hint = card("Dicas", self._hint_lv, expand=True)

        # Root row
        self.control = ft.Row(
            controls=[
                ft.Container(self._col_actions, expand=6),
                ft.Container(self._col_config, expand=2),
                ft.Container(self._col_hint, expand=3),
            ],
            spacing=12,
            expand=True,
        )

        # Defaults
        self.set_config_defaults()
        self.set_hint("Passe o olho nas opções.\nCada escolha cobra um preço.", typewriter=False)

    # --------------------
    # Hint (typewriter)
    # --------------------
    def _cancel_typing(self) -> None:
        if self._typing.task and not self._typing.task.done():
            self._typing.task.cancel()
        self._typing.task = None

    def _pulse_hint(self) -> None:
        self._hint_text.opacity = 0.35
        self.page.update()

        async def _up() -> None:
            await asyncio.sleep(0.08)
            self._hint_text.opacity = 1
            self.page.update()

        self.page.run_task(_up)

    def set_hint(self, text: str, *, typewriter: bool = True, speed: float = 0.02) -> None:
        self._cancel_typing()
        full = text or ""

        if not typewriter:
            self._hint_text.value = full
            self._hint_text.opacity = 1
            self.page.update()
            return

        self._hint_text.value = ""
        self._pulse_hint()

        async def _type() -> None:
            try:
                i = 0
                step = 2
                while i < len(full):
                    i = min(len(full), i + step)
                    self._hint_text.value = full[:i]
                    self.page.update()
                    await asyncio.sleep(speed)
            except asyncio.CancelledError:
                return

        self._typing.task = self.page.run_task(_type)

    # --------------------
    # Config
    # --------------------
    def _config_button(self, label: str, hint: str) -> ft.Control:
        return ft.Button(
            content=ft.Text(label, size=13, weight=ft.FontWeight.W_600),
            height=40,
            on_click=lambda _e: self.set_hint(hint, typewriter=True),
        )

    def set_config_defaults(self) -> None:
        self._config_lv.controls = [
            self._config_button("Mochila", "Mochila / Inventário"),
            self._config_button("Atributos", "Árvore de atributos"),
            self._config_button("Config", "Configurações do jogo"),
        ]

    # --------------------
    # Ações
    # --------------------
    def render(self, state: GameState, *, on_choose: Callable[[str], None]) -> None:
        def _make_on_click(choice_key: str):
            def _handler(_e):
                on_choose(choice_key)
            return _handler

        controls: list[ft.Control] = []

        for c in state.choices:
            btn = ft.Button(
                content=ft.Text(c.label, size=13, weight=ft.FontWeight.W_600),
                disabled=not c.enabled,
                height=42,
                on_click=_make_on_click(c.key),
            )
            btn.opacity = 1.0 if c.enabled else 0.45
            controls.append(btn)

        if not controls:
            controls = [ft.Text("—", opacity=0.6)]

        self._actions_lv.controls = controls
        self.page.update()
