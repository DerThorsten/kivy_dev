from kivy.lang import Builder
from kivy.uix.screenmanager import  Screen
from kivy.logger import Logger

from ..game_logic import getGameLogic


Builder.load_string("""
<MiniGameScreen>:
    miniGameLayout: miniGameLayout
    BoxLayout:
        id: miniGameLayout
""")
class MiniGameScreen(Screen):
    def __init__(self, **kwargs):
        super(MiniGameScreen, self).__init__(**kwargs)
        self.gameLogic = getGameLogic()
        self.miniGameWidget = None

    def on_pre_enter(self):
        Logger.info('on_pre_enter screen %s'%self.name)

        self.miniGameWidget = self.gameLogic.randomMiniGame()
        self.miniGameWidget.initGame()
        self.miniGameLayout.add_widget(self.miniGameWidget)
        

    def on_enter(self):
        Logger.info('on_enter screen %s'%self.name)

    def on_pre_leave(self):
        Logger.info('on_pre_leave screen %s'%self.name)
        self.miniGameWidget.stopGame()
        self.miniGameLayout.clear_widgets()

    def on_leave(self):
        Logger.info('on_leave screen %s'%self.name)
