from __future__ import annotations

import flet as ft

# ============================================================
# UI Tokens (centralização de estilo)
# ============================================================

RADIUS_CARD = 16
RADIUS_CHIP = 12

PAD_CARD = 12
PAD_INNER_TOP = 6

BORDER_W = 1


def outline_color() -> str:
    """
    Cor padrão de contorno (borda). Em algumas versões o tema muda,
    então manter isso encapsulado ajuda a trocar depois.
    """
    return ft.Colors.OUTLINE_VARIANT


def subtle_bg(opacity: float = 0.06) -> str:
    """Fundo sutil para estados ativos/hover (quando aplicável)."""
    return ft.Colors.with_opacity(opacity, ft.Colors.ON_SURFACE)


# ============================================================
# Primitives
# ============================================================

def card(
    title: str,
    content: ft.Control,
    *,
    expand: bool = False,
    subtitle: str | None = None,
    header_actions: ft.Control | None = None,
    scroll: bool = False,
) -> ft.Container:
    """
    Card padrão do jogo:
    - título + divider + conteúdo
    - borda, padding e radius consistentes

    Params:
      - subtitle: texto menor abaixo do título (opcional)
      - header_actions: widget no header (ex: tabs, botões) (opcional)
      - scroll: se True, envolve o conteúdo em Column com scroll
    """

    header_left = ft.Column(
        controls=[
            ft.Text(title, size=12, weight=ft.FontWeight.W_700),
            *( [ft.Text(subtitle, size=11, opacity=0.75)] if subtitle else [] ),
        ],
        spacing=2,
        expand=True,
    )

    header = ft.Row(
        controls=[
            header_left,
            *( [header_actions] if header_actions else [] ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    body: ft.Control
    if scroll:
        body = ft.Column(
            controls=[content],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    else:
        body = content

    return ft.Container(
        content=ft.Column(
            controls=[
                header,
                ft.Divider(height=1),
                body,
            ],
            spacing=8,
            expand=True,
        ),
        padding=PAD_CARD,
        border=ft.border.all(BORDER_W, outline_color()),
        border_radius=RADIUS_CARD,
        expand=expand,
    )


def stat_chip(
    label: str,
    value: int,
    *,
    min_width: int | None = None,
    value_opacity: float = 1.0,
) -> ft.Control:
    """
    Chip de status:
      [Label  65]
    """

    row = ft.Row(
        controls=[
            ft.Text(label, size=12, weight=ft.FontWeight.W_600),
            ft.Text(str(value), size=12, opacity=value_opacity),
        ],
        spacing=6,
        tight=True,
    )

    return ft.Container(
        content=row,
        padding=ft.padding.symmetric(horizontal=10, vertical=6),
        border=ft.border.all(BORDER_W, outline_color()),
        border_radius=RADIUS_CHIP,
        width=min_width,
    )


def section_title(text: str) -> ft.Text:
    """Título padrão de seção (quando não usar card())."""
    return ft.Text(text, size=12, weight=ft.FontWeight.W_700)


def spacer(h: int = 8) -> ft.Container:
    """Espaçador vertical simples."""
    return ft.Container(height=h)
