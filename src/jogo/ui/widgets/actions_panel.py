from __future__ import annotations

from typing import Callable, List, Optional, Dict

from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from jogo.ui.widgets.card import Card


class ActionsPanel(Card):
    """
    Rodapé (Actions Bar) — 3 colunas:
      [ AÇÕES (scroll interno) | CONFIG (scroll interno) | DICAS ]

    Regras:
    - nada vaza: listas ficam dentro de ScrollView.
    - set_actions/set_config_actions só mexem no conteúdo interno.
    """

    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=0.22,
            spacing="14dp",
            padding="12dp",
            **kwargs,
        )

        self._actions_box: MDBoxLayout | None = None
        self._config_box: MDBoxLayout | None = None
        self._hint_label: MDLabel | None = None

        self._build()

        # defaults (Sprint 1)
        self.set_config_actions(
            [
                {"label": "Mochila", "callback": self._default_config_hint("Mochila / Inventário")},
                {"label": "Atributos", "callback": self._default_config_hint("Árvore de atributos")},
                {"label": "Config", "callback": self._default_config_hint("Configurações do jogo")},
            ]
        )

        self.set_hint("Passe o olho nas opções.\nCada escolha cobra um preço.")

    # -----------------------
    # Build layout (3 colunas)
    # -----------------------
    def _build(self) -> None:
        # Coluna 1: AÇÕES (scroll interno)
        col_actions = Card(orientation="vertical", size_hint_x=0.58, padding="10dp")
        self._actions_box = self._make_scroll_column(parent=col_actions)

        # Coluna 2: CONFIG (scroll interno também, anti-vazamento)
        col_config = Card(orientation="vertical", size_hint_x=0.20, padding="10dp")
        self._config_box = self._make_scroll_column(parent=col_config)

        # Coluna 3: DICAS
        col_hint = Card(orientation="vertical", size_hint_x=0.22, padding="10dp")
        self._hint_label = MDLabel(
            text="",
            halign="left",
            valign="top",
            font_size="13sp",
            opacity=0.85,
        )
        # garante alinhamento topo e quebra dentro da caixa
        self._hint_label.bind(size=lambda inst, _size: setattr(inst, "text_size", inst.size))
        col_hint.add_widget(self._hint_label)

        # monta as 3 colunas
        self.add_widget(col_actions)
        self.add_widget(col_config)
        self.add_widget(col_hint)

    def _make_scroll_column(self, *, parent: Card) -> MDBoxLayout:
        """
        Cria uma coluna com ScrollView que nunca vaza.
        Retorna o box interno onde os botões são adicionados.
        """
        scroll = ScrollView(do_scroll_x=False, bar_width=6)

        box = MDBoxLayout(
            orientation="vertical",
            spacing="8dp",
            size_hint_y=None,
        )
        box.bind(minimum_height=lambda inst, h: setattr(inst, "height", h))

        scroll.add_widget(box)
        parent.add_widget(scroll)
        return box

    # -----------------------
    # API pública
    # -----------------------
    def set_actions(self, actions: List[Dict]) -> None:
        """
        actions: lista de dicts:
          {
            "label": str,
            "callback": callable,
            "hint": str | None
          }
        """
        if not self._actions_box:
            return

        self._actions_box.clear_widgets()

        for item in (actions or []):
            label = item.get("label", "")
            callback = item.get("callback")
            hint = item.get("hint")

            if not callable(callback):
                continue

            btn = self._make_button(label=label, height=44)
            btn.bind(on_release=lambda _btn, cb=callback, h=hint: self._on_clicked(cb, h))
            self._actions_box.add_widget(btn)

    def set_config_actions(self, actions: List[Dict]) -> None:
        """
        actions: lista de dicts:
          {
            "label": str,
            "callback": callable,
            "hint": str | None
          }
        """
        if not self._config_box:
            return

        self._config_box.clear_widgets()

        for item in (actions or []):
            label = item.get("label", "")
            callback = item.get("callback")
            hint = item.get("hint")

            if not callable(callback):
                continue

            btn = self._make_button(label=label, height=40)
            btn.bind(on_release=lambda _btn, cb=callback, h=hint: self._on_clicked(cb, h))
            self._config_box.add_widget(btn)

    def set_hint(self, text: str) -> None:
        if self._hint_label:
            self._hint_label.text = text or ""

    # -----------------------
    # Internos
    # -----------------------
    def _on_clicked(self, callback: Callable, hint: Optional[str]) -> None:
        self.set_hint(hint or "")
        callback()


    def _make_button(self, *, label: str, height: int) -> Button:
        btn = Button(
            text=label,
            size_hint_y=None,
            height=height,
            halign="center",
            valign="middle",
        )
        btn.background_normal = ""
        btn.background_color = (0.15, 0.15, 0.15, 1)
        btn.color = (0.92, 0.92, 0.92, 1)
        return btn

    def _default_config_hint(self, text: str) -> Callable:
        def _fn():
            self.set_hint(text)

        return _fn
