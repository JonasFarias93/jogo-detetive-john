from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

try:
    from kivymd.uix.button import MDRaisedButton as PrimaryButton  # KivyMD 2.x
except Exception:
    from kivy.uix.button import Button as PrimaryButton  # fallback


class MenuScreen(MDScreen):
    def on_enter(self, *args):
        self.clear_widgets()

        root = MDBoxLayout(orientation="vertical", padding="24dp", spacing="16dp")

        # Título (sem depender de font_style)
        root.add_widget(
            MDLabel(
                text="DETETIVE JOHN",
                halign="center",
                font_size="32sp",
                bold=True,
            )
        )

        root.add_widget(
            MDLabel(
                text="Noir ASCII • Casos • Padrões",
                halign="center",
                font_size="16sp",
            )
        )

        btn_start = PrimaryButton(text="Iniciar", pos_hint={"center_x": 0.5})
        btn_start.bind(on_release=lambda *_: self._go_gameplay())
        root.add_widget(btn_start)

        btn_exit = PrimaryButton(text="Sair", pos_hint={"center_x": 0.5})
        btn_exit.bind(on_release=lambda *_: self._exit())
        root.add_widget(btn_exit)

        self.add_widget(root)

    def _go_gameplay(self):
        self.manager.current = "gameplay"

    def _exit(self):
        from kivy.app import App
        App.get_running_app().stop()
