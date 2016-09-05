from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter,ScatterPlane
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.lang import Builder
from kivy.properties import *
from kivy.graphics.instructions import Instruction,InstructionGroup
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

import datetime
import random

from ...left_right_split_layout import LeftRightSplitLayout
from ...widgets import NiceButton
from ..registered_games import registerGame    




Builder.load_string("""
<EstimateTimeWidget>:
    button: button
    winLooseLabel: winLooseLabel
    BoxLayout:
        size_hint: 1,1
        orientation: 'vertical'  
        Label:
            text: 'Estimate '+str(root.timeToEstimate)+' sec'
            font_name: 'SuperMario256'
            font_size: root.height/18
        Button:
            id: button
            disabled: True
            text: '3'
            font_size: root.height/6
            font_name: 'SuperMario256'
            on_press: root.stoppedTime()

    Label:
        id: winLooseLabel
        pos_hint: {'center_x':0.5, 'center_y':0.5}
        size_hint: 0.1, 0.1
        text:""
        font_name: 'SuperMario256'
        font_size: root.height/6

""")
class EstimateTimeWidget(FloatLayout):
    timeToEstimate =  NumericProperty(0.0)
    diffTime = NumericProperty(float('inf'))
    def __init__(self, miniGameWidget, **kwargs):
        super(EstimateTimeWidget, self).__init__(**kwargs)
        self.miniGameWidget = miniGameWidget
        
    def initGame(self):
        self.timeToEstimate = round(random.uniform(5,10),1)
        self.countDownEvent = Clock.schedule_interval(self.countdown, 1.0 / 60.0)
        self.timeStart = datetime.datetime.now()


    def countdown(self, dt):
        now = datetime.datetime.now()
        dt =  now-self.timeStart
        dtsec =  dt.seconds +  dt.microseconds /1000000.0
        tLeft = 3.0 - dtsec
        tLeft = round(tLeft,1) 
        tLeft = max(0.0, tLeft)
        self.button.text = str(tLeft)

        if tLeft <= 0.0:
            Clock.unschedule(self.countDownEvent)
            self.button.disabled = False
            self.button.text = 'stop'

            self.timeStart = datetime.datetime.now()
            self.toLongEvent = Clock.schedule_once(self.toLong,  self.timeToEstimate*2)
    def stoppedTime(self):
        now = datetime.datetime.now()
        Clock.unschedule(self.toLongEvent)
        self.button.disabled= True

        dt =  now-self.timeStart
        dtsec =  dt.seconds +  dt.microseconds /1000000.0
        dtsec = round(dtsec,2) 
        self.button.text = str(dtsec) +' sec'
        self.button.font_size =  self.height/16
        self.diffTime = abs(self.timeToEstimate-dtsec)
        self.miniGameWidget.playerDone()
    def toLong(self, dt):
        self.button.disabled = True
        if True:#self.timeToEstimate == float('inf'):
            self.button.text = 'to long...'
            self.button.font_size =  self.height/6
            self.diffTime = self.timeToEstimate
            self.miniGameWidget.playerDone()




class EstimateTimeGame(LeftRightSplitLayout):

    def __init__(self,gameLogic, **kwargs):
        super(EstimateTimeGame, self).__init__(**kwargs)
        self.gameLogic = gameLogic

       
        self.did_post_init = False


    def post_init(self,dt=None):


        self.leftWidget = EstimateTimeWidget(playerId=0,miniGameWidget=self)
        self.rightWidget = EstimateTimeWidget(playerId=1,miniGameWidget=self)

        self.leftLayout.add_widget( self.leftWidget)
        self.rightLayout.add_widget(self.rightWidget)

        self.playerWidgets = [self.leftWidget, self.rightWidget]

        self.playersDone = 0

    def initGame(self):

        for i in range(2):
            self.playerWidgets[i].initGame()

    def stopGame(self):
        pass

    def playerDone(self):
        self.playersDone += 1
        if self.playersDone == 2:


            playerDt = [self.playerWidgets[i].diffTime for i in range(2)]
            if round(playerDt[0],2) != round(playerDt[1],2):
                winnerPlayerId = [0, 1][playerDt[1]<playerDt[0]]
                looserPlayerId = [1, 0][playerDt[1]<playerDt[0]]

                scores ={
                    winnerPlayerId : 1.0,
                    looserPlayerId : 0.0
                }

                self.playerWidgets[winnerPlayerId].winLooseLabel.text = "Winner"
                self.playerWidgets[winnerPlayerId].winLooseLabel.color = (0,1,0,1)
                self.playerWidgets[looserPlayerId].winLooseLabel.text = "Looser"
                self.playerWidgets[looserPlayerId].winLooseLabel.color = (1,0,0,1)
            else:
                scores ={
                    winnerPlayerId : 0.0,
                    looserPlayerId : 0.0
                }
                for i in range(2):
                    self.playerWidgets[i].winLooseLabel.text = "Draw"
                    self.playerWidgets[i].winLooseLabel.color = (0.2,0.2,0.2,1)
            def cb(dt):
                self.gameLogic.miniGameDone(scores)
            Clock.schedule_once(cb, 0.5)#

registerGame(EstimateTimeGame)