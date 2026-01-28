from __future__ import annotations

from typing import Callable, List, Optional, Dict

from kivy.clock import Clock
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

        # typewriter hint
        self._hint_typing_ev = None
        self._hint_full = ""
        self._hint_i = 0
        self._hint_speed = 0.02  # hint um pouco mais rápido que a cena

        # refs
        self._actions_box: MDBoxLayout | None = None
        self._config_box: MDBoxLayout | None = None
        self._hint_label: MDLabel | None = None
        self._action_buttons: list[Button] = []


        self._build()

        # defaults (Sprint 1)
        self.set_config_actions(
            [
                {"label": "Mochila", "callback": self._default_config_hint("Mochila / Inventário")},
                {"label": "Atributos", "callback": self._default_config_hint("Árvore de atributos")},
                {"label": "Config", "callback": self._default_config_hint("Configurações do jogo")},
            ]
        )

        self.set_hint("Passe o olho nas opções.\nCada escolha cobra um preço.", typewriter=False)

    # -----------------------
    # Build layout (3 colunas)
    # -----------------------
    def _build(self) -> None:
        # Coluna 1: AÇÕES (scroll interno)
        col_actions = Card(orientation="vertical", size_hint_x=0.58, padding="10dp")
        self._actions_box = self._make_scroll_column(parent=col_actions)

        # Coluna 2: CONFIG (scroll interno também)
        col_config = Card(orientation="vertical", size_hint_x=0.20, padding="10dp")
        self._config_box = self._make_scroll_column(parent=col_config)

        # Coluna 3: DICAS
        col_hint = Card(orientation="vertical", size_hint_x=0.22, padding="10dp")
        self._hint_label = MDLabel(
            text="",
            halign="left",
            valign="top",
            font_size="14sp",
            opacity=1,
        )
        # quebra dentro da caixa
        self._hint_label.bind(size=lambda inst, _size: setattr(inst, "text_size", inst.size))
        col_hint.add_widget(self._hint_label)

        # monta as 3 colunas
        self.add_widget(col_actions)
        self.add_widget(col_config)
        self.add_widget(col_hint)

    def _make_scroll_column(self, *, parent: Card) -> MDBoxLayout:
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
        if not self._actions_box:
            return

        self._actions_box.clear_widgets()
        self._action_buttons = []


        for item in (actions or []):
            label = item.get("label", "")
            callback = item.get("callback")
            hint = item.get("hint")

            if not callable(callback):
                continue

            btn = self._make_button(label=label, height=44)
            btn.bind(on_release=lambda _btn, cb=callback, h=hint: self._on_clicked(cb, h))
            self._actions_box.add_widget(btn)
            self._action_buttons.append(btn)

    def set_actions_enabled(self, enabled: bool) -> None:
        for btn in self._action_buttons:
            btn.disabled = not enabled
            btn.opacity = 1.0 if enabled else 0.45

    def set_config_actions(self, actions: List[Dict]) -> None:
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

    def set_hint(self, text: str, *, typewriter: bool = True) -> None:
        if not self._hint_label:
            return

        # cancela typing anterior
        if self._hint_typing_ev is not None:
            self._hint_typing_ev.cancel()
            self._hint_typing_ev = None

        self._hint_full = (text or "")
        self._hint_i = 0

        if not typewriter:
            self._hint_label.text = self._hint_full
            self._hint_label.opacity = 1
            return

        # inicia digitação
        self._hint_label.text = ""
        self._pulse_hint()

        def _tick(_dt):
            if not self._hint_label:
                return False

            step = 2
            self._hint_i = min(len(self._hint_full), self._hint_i + step)
            self._hint_label.text = self._hint_full[: self._hint_i]

            if self._hint_i >= len(self._hint_full):
                if self._hint_typing_ev is not None:
                    self._hint_typing_ev.cancel()
                    self._hint_typing_ev = None
                self._hint_label.opacity = 1
                return False

            return True

        self._hint_typing_ev = Clock.schedule_interval(_tick, self._hint_speed)

    # -----------------------
    # Internos
    # -----------------------
    def _on_clicked(self, callback: Callable, hint: Optional[str]) -> None:
        # sempre atualiza (limpa se vier vazio)
        self.set_hint(hint or "", typewriter=True)
        callback()

    def _pulse_hint(self) -> None:
        if not self._hint_label:
            return

        # mini “chamada” pro olho
        self._hint_label.opacity = 0.35

        def _up(_dt):
            if self._hint_label:
                self._hint_label.opacity = 1

        Clock.schedule_once(_up, 0.08)

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
            self.set_hint(text, typewriter=True)

        return _fn
