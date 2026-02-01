from __future__ import annotations

import flet as ft

from jogo.app.config import AppConfig
from jogo.domain import GameEngine, GameState


def run_app() -> None:
    ft.app(target=_main)


def _main(page: ft.Page) -> None:
    page.title = "Detetive John"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.spacing = 12

    cfg = AppConfig()
    engine = GameEngine(chapter_id=cfg.default_chapter)
    state = engine.start()

    # ---------- UI helpers ----------

    def _stat_chip(label: str, value: int) -> ft.Control:
        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(label, size=12, weight=ft.FontWeight.W_600),
                    ft.Text(str(value), size=12),
                ],
                spacing=6,
                tight=True,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=6),
            border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
            border_radius=12,
        )

    # ---------- Top (status) ----------
    status_row = ft.Row(spacing=8, wrap=True)

    # ---------- Left (text) ----------
    text_view = ft.Text(value="", selectable=True, size=14)

    text_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Narrativa", size=12, weight=ft.FontWeight.W_700),
                ft.Divider(height=1),
                ft.Container(text_view, padding=ft.padding.only(top=6)),
            ],
            spacing=8,
        ),
        padding=12,
        border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
        border_radius=16,
        expand=True,
    )

    # ---------- Right (image) ----------
    image_view = ft.Image(
        src="",
        fit=ft.ImageFit.CONTAIN,
        expand=True,
    )

    image_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Cena", size=12, weight=ft.FontWeight.W_700),
                ft.Divider(height=1),
                ft.Container(image_view, padding=ft.padding.only(top=6), expand=True),
            ],
            spacing=8,
            expand=True,
        ),
        padding=12,
        border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
        border_radius=16,
        expand=True,
    )

    # ---------- Bottom (actions) ----------
    actions_col = ft.Column(spacing=8)

    actions_panel = ft.Container(
        content=ft.Column(
            [
                ft.Text("Ações", size=12, weight=ft.FontWeight.W_700),
                ft.Divider(height=1),
                actions_col,
            ],
            spacing=8,
        ),
        padding=12,
        border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
        border_radius=16,
    )

    # ---------- Layout root ----------
    body = ft.Row(
        [text_panel, image_panel],
        spacing=12,
        expand=True,
    )

    root = ft.Column(
        [
            ft.Text("Detetive John — Capítulo 01", size=16, weight=ft.FontWeight.W_700),
            status_row,
            body,
            actions_panel,
        ],
        spacing=12,
        expand=True,
    )

    page.add(root)

    # ---------- Render ----------
    def render(s: GameState) -> None:
        status_row.controls = [
            _stat_chip("Sono", s.stats.sono),
            _stat_chip("Energia", s.stats.energia),
            _stat_chip("Foco", s.stats.foco),
            _stat_chip("Estresse", s.stats.estresse),
        ]

        text_view.value = s.text.strip() if s.text else ""

        # imagem pode ser "" (permitido)
        image_view.src = s.image_path if s.image_path else ""
        image_view.visible = bool(s.image_path)

        def on_choose(e: ft.ControlEvent) -> None:
            choice_key = e.control.data
            new_state = engine.choose(choice_key)
            render(new_state)

        actions_col.controls = []
        for c in s.choices:
            btn = ft.FilledButton(
                text=c.label,
                disabled=not c.enabled,
                data=c.key,
                on_click=on_choose,
            )
            actions_col.controls.append(btn)

        page.update()

    render(state)
