from __future__ import annotations

from typing import Optional

from kivy.clock import Clock
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
            text="TEXTO",
            halign="left",
            valign="top",
            font_size="16sp",
            size_hint_y=None,  # necessário pro scroll
            opacity=0.95,
        )

        # Ajusta altura conforme o texto renderiza
        self._text_label.bind(
            texture_size=lambda inst, size: setattr(inst, "height", size[1])
        )

        # definido depois no wrap
        self._text_label.text_size = (0, None)

        scroll.add_widget(self._text_label)
        self._left_card.add_widget(scroll)

        # =========================
        # RIGHT: IMAGENS (card)
        # =========================
        right_card = Card(orientation="vertical", size_hint_x=0.38, padding="14dp")

        # placeholder quando não tiver imagem
        self._image_placeholder = MDLabel(
            text="IMAGENS",
            halign="center",
            valign="middle",
            font_size="22sp",
            opacity=0.55,
        )
        right_card.add_widget(self._image_placeholder)

        self._image = Image(
            source="",
            allow_stretch=True,
            keep_ratio=True,
            opacity=1,
        )
        # começa invisível (até ter imagem)
        self._image.opacity = 0
        right_card.add_widget(self._image)

        # monta no container principal
        self.add_widget(self._left_card)
        self.add_widget(right_card)

    # ---------- API pública (contrato) ----------
    def set_text(self, text: str) -> None:
        self._scene_text = (text or "").strip()

        if not self._text_label:
            return

        if self._scene_text:
            self._text_label.text = self._scene_text
            self._text_label.opacity = 1.0
        else:
            # placeholder visual como no mock
            self._text_label.text = "TEXTO"
            self._text_label.opacity = 0.55

        self._apply_text_wrap()

    def set_image(self, path: Optional[str]) -> None:
        self._scene_image_path = (path or "").strip()

        if not self._image or not self._image_placeholder:
            return

        if self._scene_image_path:
            self._image.source = self._scene_image_path
            self._image.opacity = 1
            self._image_placeholder.opacity = 0
            self._image.reload()
        else:
            # sem imagem: mostra placeholder "IMAGENS"
            self._image.source = ""
            self._image.opacity = 0
            self._image_placeholder.opacity = 0.55

    def refresh(self) -> None:
        self.set_text(self._scene_text)
        self.set_image(self._scene_image_path)

    # ---------- Internos ----------
    def _apply_text_wrap(self) -> None:
        if not self._text_label or not self._left_card:
            return

        # largura real do card esquerdo menos “respiro”
        wrap_w = max(1, int(self._left_card.width) - 28)
        self._text_label.text_size = (wrap_w, None)
