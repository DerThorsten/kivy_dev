from kivy.uix.screenmanager import ScreenManager, RiseInTransition
from menu_screen import MenuScreen
from mini_game_screen import MiniGameScreen
from between_mini_game_screen import BetweemMiniGameScreen
from tparty.game_logic import getGameLogic
from ..tools import  Singleton



class GameScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(GameScreenManager, self).__init__(
            #transition=RiseInTransition(),
            **kwargs)

        self.add_widget(MenuScreen(name='menuScreen'))
        self.add_widget(BetweemMiniGameScreen(name='betweemMiniGameScreen'))
        self.add_widget(MiniGameScreen(name='miniGameScreen'))


    