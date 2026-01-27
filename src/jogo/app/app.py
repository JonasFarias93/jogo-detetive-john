from kivymd.app import MDApp

from jogo.app.navigation import build_root
from jogo.core.config import AppConfig


class DetetiveJohnApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_model = AppConfig()

    def build(self):
        self.title = "Detetive John"
        self.theme_cls.theme_style = "Dark"
        # REMOVER: self.theme_cls.primary_palette = "BlueGray"
        return build_root(self)
