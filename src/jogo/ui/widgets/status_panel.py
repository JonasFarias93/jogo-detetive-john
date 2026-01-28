from __future__ import annotations

from typing import Dict, Optional

from kivy.uix.progressbar import ProgressBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from jogo.ui.widgets.card import Card


class StatusPanel(Card):
    """
    Painel STATUS (topo) — sem título.
    HUD autoexplicativo: barras + valores.
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=0.20, **kwargs)

        self._labels: Dict[str, MDLabel] = {}
        self._pbs: Dict[str, ProgressBar] = {}

        self.stats = {
            "Sono": 0,
            "Energia": 0,
            "Foco": 0,
            "Estresse": 0,
        }

        self._grid: MDBoxLayout | None = None

        self._build()
        self.bind(width=self._on_resize)

    def _build(self) -> None:
        body = MDBoxLayout(
            orientation="vertical",
            spacing="6dp",
            padding=("10dp", "10dp", "10dp", "10dp"),
        )
        self.add_widget(body)

        self._grid = MDBoxLayout(orientation="horizontal", spacing="14dp")

        col_left = MDBoxLayout(orientation="vertical", spacing="6dp", size_hint_x=0.5)
        col_right = MDBoxLayout(orientation="vertical", spacing="6dp", size_hint_x=0.5)

        col_left.add_widget(self._status_row("Sono"))
        col_left.add_widget(self._status_row("Foco"))

        col_right.add_widget(self._status_row("Energia"))
        col_right.add_widget(self._status_row("Estresse"))

        self._grid.add_widget(col_left)
        self._grid.add_widget(col_right)
        body.add_widget(self._grid)

        self._apply_label_wrap()

    def _status_row(self, name: str):
        row = MDBoxLayout(
            orientation="vertical",
            spacing="2dp",
            size_hint_y=None,
            height=44,
        )

        label = MDLabel(
            text=f"{name}: {self.stats.get(name, 0)}",
            halign="left",
            valign="middle",
            font_size="14sp",
            size_hint_y=None,
            height=18,
            shorten=True,
            shorten_from="right",
        )

        bar = ProgressBar(
            max=100,
            value=self.stats.get(name, 0),
            size_hint_y=None,
            height=18,
        )

        self._labels[name] = label
        self._pbs[name] = bar

        row.add_widget(label)
        row.add_widget(bar)
        return row

    # -------- API pública --------
    def set_stats(
        self,
        *,
        sono: Optional[int] = None,
        energia: Optional[int] = None,
        foco: Optional[int] = None,
        estresse: Optional[int] = None,
    ) -> None:
        if sono is not None:
            self.stats["Sono"] = max(0, min(100, int(sono)))
        if energia is not None:
            self.stats["Energia"] = max(0, min(100, int(energia)))
        if foco is not None:
            self.stats["Foco"] = max(0, min(100, int(foco)))
        if estresse is not None:
            self.stats["Estresse"] = max(0, min(100, int(estresse)))

        self.refresh()

    def refresh(self) -> None:
        for key in ("Sono", "Energia", "Foco", "Estresse"):
            if key in self._labels:
                self._labels[key].text = f"{key}: {self.stats[key]}"
            if key in self._pbs:
                self._pbs[key].value = self.stats[key]

    # -------- Internos --------
    def _on_resize(self, *_args):
        self._apply_label_wrap()

    def _apply_label_wrap(self):
        if not self._labels or not self._grid:
            return

        col_w = max(80, int(self._grid.width * 0.5) - 18)
        for lbl in self._labels.values():
            lbl.text_size = (col_w, None)
