from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string("""
<MenuButtonWidget>:
    Button:
        text: 'Menu'
        on_press: root.miniGameWidget.on_press_menu()
""")
class MenuButtonWidget(BoxLayout):
    miniGameWidget = ObjectProperty()
