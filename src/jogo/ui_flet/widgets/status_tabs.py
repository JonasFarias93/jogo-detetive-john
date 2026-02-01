from __future__ import annotations

import flet as ft

from jogo.domain import GameState
from .common import card, stat_chip, subtle_bg


class StatusTabs:
    """
    Tabs compatíveis com Flet (0.25+): Containers clicáveis + troca de conteúdo.
    Visual: underline na aba ativa + fundo sutil na aba ativa.
    """

    def __init__(self) -> None:
        # ---------- Views ----------
        self._chips = ft.Row(spacing=8, wrap=True)
        self._local_text = ft.Text(value="—", selectable=True, size=13, no_wrap=False)
        self._arquivo_text = ft.Text(value="Em breve: pistas, objetivos, tags.", size=13)

        self._status_view = ft.Container(self._chips, padding=ft.padding.only(top=6))
        self._local_view = ft.Container(self._local_text, padding=ft.padding.only(top=6))
        self._arquivo_view = ft.Container(self._arquivo_text, padding=ft.padding.only(top=6))

        self._content_host = ft.Container(content=self._status_view)

        # ---------- Tabs ----------
        self._active = "status"
        self._tab_status = self._tab("Status", "status")
        self._tab_local = self._tab("Local", "local")
        self._tab_arquivo = self._tab("Arquivo", "arquivo")

        self._tabs_row = ft.Row(
            controls=[self._tab_status, self._tab_local, self._tab_arquivo],
            spacing=8,
            wrap=True,
        )

        # ---------- Root control ----------
        self.control = card(
            "Sessão",
            ft.Column([self._content_host], spacing=8, expand=True),
            header_actions=self._tabs_row,
            expand=False,
        )

        self._refresh_tabs()

    # ---------- Tab building ----------
    def _tab(self, label: str, name: str) -> ft.Container:
        txt = ft.Text(label, size=13, weight=ft.FontWeight.W_600)

        # Algumas versões suportam "ink", outras não. Então tentamos sem travar.
        kwargs = dict(
            content=txt,
            padding=ft.padding.symmetric(horizontal=14, vertical=8),
            border_radius=12,
            on_click=lambda _e, n=name: self._select(n),
        )
        try:
            c = ft.Container(**kwargs, ink=True)  # type: ignore[arg-type]
        except TypeError:
            c = ft.Container(**kwargs)

        c.data = {"name": name, "text": txt}
        return c

    def _select(self, name: str) -> None:
        self._active = name

        if name == "status":
            self._content_host.content = self._status_view
        elif name == "local":
            self._content_host.content = self._local_view
        else:
            self._content_host.content = self._arquivo_view

        self._refresh_tabs()
        # layout/page.update() fica com quem chamou (main/layout)

    def _refresh_tabs(self) -> None:
        for t in (self._tab_status, self._tab_local, self._tab_arquivo):
            meta = t.data or {}
            name = meta.get("name", "")
            is_active = (name == self._active)

            txt = meta.get("text")
            if isinstance(txt, ft.Text):
                txt.opacity = 1.0 if is_active else 0.55
                txt.weight = ft.FontWeight.W_700 if is_active else ft.FontWeight.W_600

            t.bgcolor = subtle_bg(0.06) if is_active else None

            # underline: ativo forte, inativo invisível mas mantendo altura
            t.border = ft.border.only(
                bottom=ft.BorderSide(
                    3,
                    ft.Colors.PRIMARY if is_active else ft.Colors.with_opacity(0.0, ft.Colors.ON_SURFACE),
                )
            )

    # ---------- Render ----------
    def render(self, state: GameState) -> None:
        s = state.stats
        self._chips.controls = [
            stat_chip("Sono", s.sono),
            stat_chip("Energia", s.energia),
            stat_chip("Foco", s.foco),
            stat_chip("Estresse", s.estresse),
        ]

    def set_location(self, text: str) -> None:
        self._local_text.value = text or "—"
