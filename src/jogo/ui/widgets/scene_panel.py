from __future__ import annotations

from typing import Optional

from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from jogo.ui.widgets.card import Card


class ScenePanel(MDBoxLayout):
    """
    Painel central do gameplay (meio), seguindo o mock final:
    - Sem título "CENA"
    - Duas caixas lado a lado:
        esquerda: TEXTO (scroll)
        direita: IMAGENS (imagem da cena)
    """

    def __init__(self, **kwargs):
        super().__init__(
            orientation="horizontal",
            size_hint_y=0.60,
            spacing="18dp",
            **kwargs,
        )

        # typewriter
        self._typing_ev = None
        self._typing_text_full = ""
        self._typing_i = 0
        self._typing_speed = 0.015  # menor = mais rápido

        # refs
        self._text_label: MDLabel | None = None
        self._image: Image | None = None
        self._image_placeholder: MDLabel | None = None
        self._left_card: Card | None = None

        # estado interno
        self._scene_text: str = ""
        self._scene_image_path: str = ""

        self._build()

        # Ajusta wrap quando o layout estiver pronto e em resize
        Clock.schedule_once(lambda *_: self._apply_text_wrap(), 0)
        self.bind(width=lambda *_: self._apply_text_wrap())

    def _build(self) -> None:
        # =========================
        # LEFT: TEXTO (card)
        # =========================
        self._left_card = Card(orientation="vertical", size_hint_x=0.62, padding="14dp")

        scroll = ScrollView(do_scroll_x=False)

        self._text_label = MDLabel(
            text="",
            halign="left",
            valign="top",
            font_size="16sp",
            size_hint_y=None,  # necessário pro scroll
            opacity=0.95,
        )

        # Ajusta altura conforme o texto renderiza
        self._text_label.bind(texture_size=lambda inst, size: setattr(inst, "height", size[1]))

        # definido depois no wrap
        self._text_label.text_size = (0, None)

        scroll.add_widget(self._text_label)
        self._left_card.add_widget(scroll)

        # =========================
        # RIGHT: IMAGENS (card) [overlay]
        # =========================
        right_card = Card(orientation="vertical", size_hint_x=0.38, padding="14dp")

        layer = FloatLayout()
        right_card.add_widget(layer)

        # placeholder quando não tiver imagem
        self._image_placeholder = MDLabel(
            text="IMAGENS",
            halign="center",
            valign="middle",
            font_size="22sp",
            opacity=0.55,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        self._image_placeholder.bind(size=lambda inst, _size: setattr(inst, "text_size", inst.size))
        layer.add_widget(self._image_placeholder)

        # imagem (full area)
        self._image = Image(
            source="",
            fit_mode="contain",
            mipmap=True,
            opacity=0,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layer.add_widget(self._image)

        # monta no container principal (APENAS UMA VEZ)
        self.add_widget(self._left_card)
        self.add_widget(right_card)

    # ---------- API pública (contrato) ----------
    def set_text(self, text: str, *, typewriter: bool = True, on_done=None) -> None:
        self._scene_text = text or ""

        if not self._text_label:
            return

        # cancela digitação anterior
        if self._typing_ev is not None:
            self._typing_ev.cancel()
            self._typing_ev = None

        if not typewriter:
            self._text_label.text = self._scene_text
            self._apply_text_wrap()
            if callable(on_done):
                on_done()
            return

        # inicia digitação
        self._typing_text_full = self._scene_text
        self._typing_i = 0
        self._text_label.text = ""
        self._apply_text_wrap()

        def _tick(_dt):
            if not self._text_label:
                return False

            step = 2
            self._typing_i = min(len(self._typing_text_full), self._typing_i + step)
            self._text_label.text = self._typing_text_full[: self._typing_i]

            if self._typing_i >= len(self._typing_text_full):
                if self._typing_ev is not None:
                    self._typing_ev.cancel()
                    self._typing_ev = None
                if callable(on_done):
                    on_done()
                return False

            return True

        self._typing_ev = Clock.schedule_interval(_tick, self._typing_speed)

    def set_image(self, path: Optional[str]) -> None:
        self._scene_image_path = (path or "").strip()

        if not self._image or not self._image_placeholder:
            return

        if self._scene_image_path:
            self._image.source = self._scene_image_path
            self._image.reload()

            # suaviza scaling (remove “linhas/pontilhado”)
            if self._image.texture:
                self._image.texture.mag_filter = "linear"
                self._image.texture.min_filter = "linear"

            self._image.opacity = 1
            self._image_placeholder.opacity = 0
        else:
            self._image.source = ""
            self._image.opacity = 0
            self._image_placeholder.opacity = 0.55

    def refresh(self) -> None:
        self.set_text(self._scene_text, typewriter=False)
        self.set_image(self._scene_image_path)

    # ---------- Internos ----------
    def _apply_text_wrap(self) -> None:
        if not self._text_label or not self._left_card:
            return

        wrap_w = max(1, int(self._left_card.width) - 28)
        self._text_label.text_size = (wrap_w, None)
