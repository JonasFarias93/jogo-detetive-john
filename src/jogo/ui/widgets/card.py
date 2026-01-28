from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout

KV = """
<Card>:
    padding: dp(16)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [root.radius,]
        Color:
            rgba: root.border_color
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, root.radius)
            width: root.border_width
"""
Builder.load_string(KV)


class Card(BoxLayout):
    bg_color = ListProperty([0.08, 0.08, 0.08, 1])
    border_color = ListProperty([0.35, 0.35, 0.35, 1])
    border_width = NumericProperty(1.1)
    radius = NumericProperty(14)
