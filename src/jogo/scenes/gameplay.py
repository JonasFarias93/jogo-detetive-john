from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView

try:
    # Algumas builds do KivyMD 2.x
    from kivymd.uix.appbar import MDTopAppBar  # type: ignore
except Exception:
    try:
        # Outras builds do KivyMD 2.x
        from kivymd.uix.topappbar import MDTopAppBar  # type: ignore
    except Exception:
        # Último fallback: usa a barra do Kivy "puro"
        from kivy.uix.boxlayout import BoxLayout as MDTopAppBar  # type: ignore



ASCII_INTRO = """\
┌──────────────────────────────────────────┐
│             DELEGACIA — 02:13            │
└──────────────────────────────────────────┘

Você é John. Detetive. Problemas demais.
E uma cidade que não dorme.
O primeiro caso parece pequeno...
até você notar o padrão.
"""


class GameplayScreen(MDScreen):
    def on_enter(self, *args):
        self.clear_widgets()

        root = MDBoxLayout(orientation="vertical", padding="16dp", spacing="12dp")

        try:
            bar = MDTopAppBar(
                title="Capítulo 01",
                left_action_items=[["arrow-left", lambda *_: self._back()]],
            )
        except TypeError:
            # fallback tosco (se cair no BoxLayout)
            bar = MDBoxLayout(size_hint_y=None, height="48dp")

        root.add_widget(bar)

        scroll = ScrollView(do_scroll_x=False)

        label = MDLabel(
            text=ASCII_INTRO,
            halign="left",
            valign="top",
            size_hint_y=None,
        )
        label.bind(texture_size=lambda inst, size: setattr(inst, "height", size[1]))
        label.text_size = (0, None)  # será ajustado ao entrar
        scroll.add_widget(label)

        root.add_widget(scroll)
        self.add_widget(root)

        # Ajuste do wrap na largura disponível
        label.text_size = (self.width, None)

    def _back(self):
        self.manager.current = "menu"
