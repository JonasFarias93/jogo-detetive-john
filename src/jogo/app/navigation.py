from kivy.uix.screenmanager import FadeTransition, ScreenManager

from jogo.scenes.gameplay import GameplayScreen
from jogo.scenes.menu import MenuScreen


def build_root(app) -> ScreenManager:
    sm = ScreenManager(transition=FadeTransition(duration=0.15))
    sm.add_widget(MenuScreen(name="menu"))
    sm.add_widget(GameplayScreen(name="gameplay"))
    sm.current = "menu"
    return sm
