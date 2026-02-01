from __future__ import annotations

import asyncio
from dataclasses import dataclass
import flet as ft

from jogo.runtime.config import AppConfig
from jogo.domain import GameEngine, GameState


# ----------------------------
# Helpers internos (typewriter)
# ----------------------------

@dataclass
class TypingJob:
    task: asyncio.Task | None = None


def run_app() -> None:
    ft.run(_main)


def _main(page: ft.Page) -> None:
    page.title = "Detetive John"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 16
    page.spacing = 12

    cfg = AppConfig()
    engine = GameEngine(chapter_id=cfg.default_chapter)
    state = engine.start()

    hint_job = TypingJob()

    # ---------- UI helpers ----------
    def _card(title: str, content: ft.Control, *, expand: bool = False) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=12, weight=ft.FontWeight.W_700),
                    ft.Divider(height=1),
                    content,
                ],
                spacing=8,
                expand=True,
            ),
            padding=12,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=16,
            expand=expand,
        )

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
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=12,
        )

    # ---------- Top (status) ----------
    status_row = ft.Row(spacing=8, wrap=True)

    # ---------- Left (text) ----------
    text_view = ft.Text(value="", selectable=True, size=14)
    text_content = ft.Container(text_view, padding=ft.Padding(top=6))
    text_panel = _card("Narrativa", text_content, expand=True)

    # ---------- Right (image) ----------
    image_view = ft.Image(src="", fit=ft.BoxFit.CONTAIN, expand=True)
    image_content = ft.Container(image_view, padding=ft.Padding(top=6), expand=True)
    image_panel = _card("Cena", image_content, expand=True)

    # ---------- Bottom (actions/config/hints) ----------
    actions_list = ft.Column(spacing=8)
    config_list = ft.Column(spacing=8)

    # Hint area
    hint_text = ft.Text(
        value="",
        size=13,
        selectable=False,
        no_wrap=False,  # permite quebrar linha
    )

    hint_box = ft.Container(
        content=ft.Column(
            [hint_text],
            scroll=ft.ScrollMode.AUTO,  # scroll no hint se ficar grande
            expand=True,
        ),
        padding=ft.Padding(top=3),
        expand=True,
    )


    # Scroll wrappers (nada vaza)
    actions_scroll = ft.Container(
        content=ft.Column([actions_list], scroll=ft.ScrollMode.AUTO),
        expand=True,
    )

    config_scroll = ft.Container(
        content=ft.Column([config_list], scroll=ft.ScrollMode.AUTO),
        expand=True,
    )

    col_actions = _card("Ações", actions_scroll, expand=True)
    col_config = _card("Config", config_scroll, expand=False)
    col_hint = _card("Dicas", hint_box, expand=True)

    # 3 colunas no painel inferior
    bottom_row = ft.Row(
        controls=[
            ft.Container(col_actions, expand=6),
            ft.Container(col_config, expand=2),
            ft.Container(col_hint, expand=3),
        ],
        spacing=12,
        expand=True,
    )

    actions_panel = ft.Container(
        content=bottom_row,
        padding=0,
        expand=1,
        height=260,
    )

    # ---------- Layout root ----------
    body = ft.Row([text_panel, image_panel], 
                  spacing=12, 
                  expand=2)

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

    # ----------------------------
    # Hint helpers (pulse + typing)
    # ----------------------------
    def _cancel_hint_typing() -> None:
        if hint_job.task and not hint_job.task.done():
            hint_job.task.cancel()
        hint_job.task = None

    def _pulse_hint() -> None:
        # mini “chamada” pro olho
        hint_text.opacity = 0.35
        page.update()

        async def _up():
            await asyncio.sleep(0.08)
            hint_text.opacity = 1
            page.update()

        page.run_task(_up)

    def set_hint(text: str, *, typewriter: bool = True, speed: float = 0.02) -> None:
        _cancel_hint_typing()

        full = (text or "")

        if not typewriter:
            hint_text.value = full
            hint_text.opacity = 1
            page.update()
            return

        hint_text.value = ""
        _pulse_hint()

        async def _type():
            try:
                i = 0
                step = 2  # hint mais rápido
                while i < len(full):
                    i = min(len(full), i + step)
                    hint_text.value = full[:i]
                    page.update()
                    await asyncio.sleep(speed)
            except asyncio.CancelledError:
                return

        hint_job.task = page.run_task(_type)

    # ----------------------------
    # Config buttons (placeholder)
    # ----------------------------
    def _config_item(label: str, hint: str) -> ft.Control:
        return ft.Button(
            content=ft.Text(label),
            on_click=lambda _e: set_hint(hint, typewriter=True),
        )

    def build_config_defaults() -> None:
        config_list.controls = [
            _config_item("Mochila", "Mochila / Inventário"),
            _config_item("Atributos", "Árvore de atributos"),
            _config_item("Config", "Configurações do jogo"),
        ]

    # ----------------------------
    # Actions from engine
    # ----------------------------
    def render(s: GameState) -> None:
        status_row.controls = [
            _stat_chip("Sono", s.stats.sono),
            _stat_chip("Energia", s.stats.energia),
            _stat_chip("Foco", s.stats.foco),
            _stat_chip("Estresse", s.stats.estresse),
        ]

        text_view.value = s.text.strip() if s.text else ""

        image_view.src = s.image_path if s.image_path else ""
        image_view.visible = bool(s.image_path)

        def on_choose(e: ft.ControlEvent) -> None:
            choice_key = e.control.data
            new_state = engine.choose(choice_key)

            # hint da escolha (se existir)
            # (o GameState/Choice no seu domain já tem hint? se não, isso fica vazio)
            chosen_hint = getattr(e.control, "hint", "") if hasattr(e.control, "hint") else ""
            if chosen_hint:
                set_hint(chosen_hint, typewriter=True)

            render(new_state)

        actions_list.controls = []

        # default hint inicial (como no Kivy)
        if not hint_text.value:
            set_hint("Passe o olho nas opções.\nCada escolha cobra um preço.", typewriter=False)

        for c in s.choices:
            # Botão compatível com Flet atual: content=Text(...)
            btn = ft.Button(
                content=ft.Text(c.label),
                disabled=not c.enabled,
                data=c.key,
                on_click=on_choose,
            )

            # Guardar hint no botão (compat simples)
            # Se o seu Choice tiver 'hint', funciona. Se não tiver, fica vazio.
            try:
                btn.hint = getattr(c, "hint", "") or ""
            except Exception:
                pass

            actions_list.controls.append(btn)

        build_config_defaults()
        page.update()

    render(state)


if __name__ == "__main__":
    run_app()
