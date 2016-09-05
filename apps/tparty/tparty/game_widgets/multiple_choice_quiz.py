from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger

from functools import partial
from time import sleep

from ..left_right_split_layout import LeftRightSplitLayout
from menu_button_widget import MenuButtonWidget

from ..widgets import NiceButton
from registered_games import registerGame    


questionList = [
{
    'question' : 'Was machen sachen?',
    'answers':[
        ('blub', True),
        ('bla',  False),
        ('bla',  False),
        ('bla',  False)
    ]
}
]




Builder.load_string("""
<MultipleChoiceQuizWidget>:
    
    # references
    questionLabel: questionLabel
    answersLayout: answersLayout
    winLooseLabelLayout: winLooseLabelLayout
    BoxLayout:
        size_hint: 1,1
        orientation: 'vertical'
        NiceLabel:
            size_hint: (1, 0.25)
            id: questionLabel
            text: 'This Is The Question'
        GridLayout:
            size_hint: (1, 0.75)
            id: answersLayout
            cols: 2
    BoxLayout:
        id: winLooseLabelLayout
        size_hint: (1,1)
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        
""")
class MultipleChoiceQuizWidget(FloatLayout):

    def __init__(self,playerId, miniGameWidget, **kwargs):
        super(MultipleChoiceQuizWidget, self).__init__(**kwargs)
        self.playerId = playerId
        self.miniGameWidget = miniGameWidget

    def setQuestion(self, q):

        # remove old answers from layout
        # and ensure that the layout is not disabled
        self.answersLayout.clear_widgets()
        self.answersLayout.disabled = False

        # remove old laberls
        self.winLooseLabelLayout.clear_widgets()

        # insert the answer labels
        q = questionList[0]
        questionText = q['question']
        answers = q['answers']
        self.questionLabel.text = questionText
        for a in answers:
            aButton = NiceButton(text=a[0])

            aButton.bind(on_press= partial(self.playerAnswered,correctAnswer=a[1]))
            self.answersLayout.add_widget(aButton)

    def playerAnswered(self, instance, correctAnswer):
        self.miniGameWidget.playerAnswered(self.playerId, correctAnswer)

        self.setWinOrLoose(correctAnswer)

    def otherPlayerAnswered(self, correctAnswer):
        self.setWinOrLoose(not correctAnswer)

    def setWinOrLoose(self, winOrLoose):
        self.answersLayout.disabled = True
        labelTxt = ['WIN','LOOSE'][not winOrLoose]
        labelColor = [(0,1,0,1),(1,0,0,1)][not winOrLoose]
        label = Label(text=labelTxt, font_size='80sp', color=labelColor)
        
        self.winLooseLabelLayout.add_widget(label)

class MultipleChoiceQuizMiniGame(LeftRightSplitLayout):

    def __init__(self,gameLogic, **kwargs):
        super(MultipleChoiceQuizMiniGame, self).__init__(**kwargs)
        self.gameLogic = gameLogic

        Logger.info('INIT')
        #Clock.schedule_once(self._post_init, 0)
        self.did_post_init = False

    def post_init(self):
        if not self.did_post_init:
            self._post_init()

    def _post_init(self,dt=None):
        Logger.info('POST_INIT')
        self.did_post_init = True
        #self.menuButtonWidget = MenuButtonWidget()
        #self.menuButtonWidget.miniGameWidget = self
        #self.middleLayout.add_widget(self.menuButtonWidget)

        self.leftQuizWidget = MultipleChoiceQuizWidget(playerId=0,miniGameWidget=self)
        self.rightQuizWidget = MultipleChoiceQuizWidget(playerId=1,miniGameWidget=self)

        self.leftLayout.add_widget( self.leftQuizWidget)
        self.rightLayout.add_widget(self.rightQuizWidget)

        self.playerWidgets = [self.leftQuizWidget, self.rightQuizWidget]

    def on_press_menu(self):
        self.miniGameScreen.manager.current = 'menuScreen'

    def initGame(self):

        self.leftQuizWidget.setQuestion(questionList[0])
        self.rightQuizWidget.setQuestion(questionList[0])

    def stopGame(self):
        pass

    def playerAnswered(self, playerId, correctAnswer):

        Logger.info('player %d Answered %s'%(playerId, str(correctAnswer)))
        otherPlayerId = [0,1][playerId==0]

        winnerPlayerId = [otherPlayerId, playerId][correctAnswer]
        looserPlayerId = [otherPlayerId, playerId][not correctAnswer]
        self.playerWidgets[otherPlayerId].otherPlayerAnswered(correctAnswer)
        
        scores ={
            winnerPlayerId : 1.0,
            looserPlayerId : 0.0
        }

        def cb(dt):
            self.gameLogic.miniGameDone(scores)
        Clock.schedule_once(cb, 0.5)

        

registerGame(MultipleChoiceQuizMiniGame)