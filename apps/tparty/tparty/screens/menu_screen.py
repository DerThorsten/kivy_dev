from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import  Screen
from kivy.uix.button import Button
from kivy.logger import Logger

from ..widgets import NiceButton


Builder.load_string("""
<MenuScreen>:
    startButton: startButton
    BoxLayout:
        orientation: 'vertical'


        AutoSizeNiceButton:
            id: startButton
            on_press: root.manager.current = 'betweemMiniGameScreen'
            markup: True
        AutoSizeNiceButton:
            id: exitButton
            text: 'Quit'
            on_press: root.manager.current = 'betweemMiniGameScreen'
""")
class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)


        t =  '[color=ff0000]S[/color]' # red
        t += '[color=009933]t[/color]' # green
        t += '[color=0033cc]a[/color]' # blue
        t += '[color=ff0000]r[/color]' # red 
        t += '[color=009933]t[/color]' # green
        self.startButton.text = t


    def on_pre_enter(self):
        Logger.info('on_pre_enter menue screen')

    def on_enter(self):
        Logger.info('on_enter menue screen')

    def on_pre_leave(self):
        Logger.info('on_pre_leave menue screen')

    def on_leave(self):
        Logger.info('on_leave menue screen')









