from __future__ import annotations

import flet as ft

from jogo.domain import GameState

from .widgets.status_tabs import StatusTabs
from .widgets.narrative_panel import NarrativePanel
from .widgets.scene_panel import ScenePanel
from .widgets.actions_panel import ActionsPanel


class AppLayout:
    """
    Composição principal da UI.
    - não conhece engine
    - recebe callbacks e estado
    - expõe dispose() para cleanup (tasks, timers, etc.)
    """

    def __init__(self, page: ft.Page) -> None:
        self.page = page

        self.status_tabs = StatusTabs()
        self.narrative = NarrativePanel()
        self.scene = ScenePanel()
        self.actions = ActionsPanel(page)

        self._title = ft.Text("Holoway — Capítulo 01", size=16, weight=ft.FontWeight.W_700)

        # Miolo (texto + imagem) -> prioridade maior
        self._body = ft.Row(
            controls=[self.narrative.control, self.scene.control],
            spacing=12,
            expand=True,
        )

        # Rodapé fixo (evita scroll espremido)
        self._bottom = ft.Container(
            content=self.actions.control,
            height=210,
        )

        self.root = ft.Column(
            controls=[
                self._title,
                self.status_tabs.control,
                self._body,
                self._bottom,
            ],
            spacing=12,
            expand=True,
        )

    def render(self, state: GameState, *, on_choose) -> None:
        self.status_tabs.render(state)
        self.narrative.render(state)
        self.scene.render(state)
        self.actions.render(state, on_choose=on_choose)

    # ----------------------------
    # Lifecycle / cleanup
    # ----------------------------
    def dispose(self) -> None:
        """
        Cancela tasks penduradas (typewriter, efeitos, etc).
        Chamado no on_disconnect do main.
        """
        for w in (self.actions, self.narrative, self.scene, self.status_tabs):
            if hasattr(w, "dispose"):
                try:
                    w.dispose()
                except Exception:
                    pass
