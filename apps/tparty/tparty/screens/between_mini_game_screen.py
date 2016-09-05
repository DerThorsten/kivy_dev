from kivy.lang import Builder
from kivy.uix.screenmanager import  Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.logger import Logger

from ..left_right_split_layout import LeftRightSplitLayout

from ..game_logic import getGameLogic


Builder.load_string("""
<BetweenMiniGameWidget>:
    #references
    scoreLabel: scoreLabel
    orientation: 'vertical'
    Label:
        id: scoreLabel
        text: "the score"
    Button:
        text:  "next game"
        on_press: root.betweemMiniGameScreen.onPressNextGame()
""")
class BetweenMiniGameWidget(BoxLayout):
    def __init__(self,betweemMiniGameScreen, **kwargs):
        super(BetweenMiniGameWidget, self).__init__(**kwargs)
        self.betweemMiniGameScreen =betweemMiniGameScreen

Builder.load_string("""
<BetweemMiniGameScreen>:
    leftRightSplitLayout: leftRightSplitLayout
    LeftRightSplitLayout:
        id: leftRightSplitLayout
""")
class BetweemMiniGameScreen(Screen):
    def __init__(self, **kwargs):
        super(BetweemMiniGameScreen, self).__init__(**kwargs)
        self.gameLogic = getGameLogic()



        self.leftWidget = BetweenMiniGameWidget(betweemMiniGameScreen=self)
        self.rightWidget = BetweenMiniGameWidget(betweemMiniGameScreen=self)

        self.leftRightSplitLayout.leftLayout.add_widget( self.leftWidget)
        self.leftRightSplitLayout.rightLayout.add_widget(self.rightWidget)

    def on_pre_enter(self):
        Logger.info('on_pre_enter screen %s'%self.name)


        

        scoreStr = "Score:"
        for pid, score in enumerate(self.gameLogic.scores):
            scoreStr+="\nPlayer %d: %d"%(pid,int(score))

        self.leftWidget.scoreLabel.text = scoreStr
        self.rightWidget.scoreLabel.text = scoreStr
    
    def onPressNextGame(self):
        self.manager.current = "miniGameScreen"

    def on_enter(self):
        Logger.info('on_enter screen %s'%self.name)

    def on_pre_leave(self):
        Logger.info('on_pre_leave screen %s'%self.name)

    def on_leave(self):
        Logger.info('on_leave screen %s'%self.name)
