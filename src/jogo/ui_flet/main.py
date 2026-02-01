from __future__ import annotations

import flet as ft

from jogo.runtime.config import AppConfig
from jogo.domain import GameEngine, GameState
from jogo.ui_flet.layout import AppLayout


def run_app() -> None:
    ft.run(_main)


def _main(page: ft.Page) -> None:
    page.title = "Detetive John"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.spacing = 12

    cfg = AppConfig()
    engine = GameEngine(chapter_id=cfg.default_chapter)

    layout = AppLayout(page)
    page.add(layout.root)

    def render(state: GameState) -> None:
        def on_choose(choice_key: str) -> None:
            # hint: aparece antes? (se quiser, a gente liga aqui também)
            new_state = engine.choose(choice_key)
            render(new_state)

        layout.render(state, on_choose=on_choose)
        page.update()

    render(engine.start())


if __name__ == "__main__":
    run_app()
