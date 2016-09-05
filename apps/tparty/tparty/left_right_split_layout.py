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

from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition




Builder.load_string("""
<LeftSideWidget>:
    size_hint: None,None
    rotation: -90
    do_rotation: False
    do_scale: False
    do_translation: False
""")
class LeftSideWidget(ScatterLayout):
    pass

Builder.load_string("""
<RightSideWidget>:
    size_hint: None,None
    rotation: 90
    do_rotation: False
    do_scale: False
    do_translation: False
""")
class RightSideWidget(ScatterLayout):
    pass



if False:






    Builder.load_string("""
<LeftRightSplitLayout>:

    leftLayout: leftLayout
    rightLayout: rightLayout
    #middleLayout: middleLayout

    FloatLayout:

        LeftSideWidget:
            size: root.height, root.width/2 - root.width/40
            pos_hint: {'x':0, 'y':0}
            BoxLayout:
                id: leftLayout



        RightSideWidget:
            size: root.height, root.width/2 - root.width/40
            pos_hint: {'right':1, 'y':0}
            rotation: 90
            BoxLayout:
                id: rightLayout  

    """)
    class LeftRightSplitLayout(FloatLayout):
        def __init__(self, **kwargs):

            super(LeftRightSplitLayout, self).__init__(**kwargs)


        def pressByPlayer(self, player):
            pass

        def addToMiddl(self, widget):
            self.middleLayout.add_widget(widget)


if True:






    Builder.load_string("""
<LeftRightSplitLayout>:
    
    rotate: False
    leftLayout: leftLayout
    rightLayout: rightLayout
    #middleLayout: middleLayout

    FloatLayout:

        LeftSideWidget:
            rotation: [0,-90][root.rotate]
            size: [root.width/2 - 5,root.height][root.rotate], [root.height,root.width/2 - 5][root.rotate]

            pos_hint: {'x':0, 'y':0}
            BoxLayout:
                id: leftLayout



        RightSideWidget:
            rotation: [0, 90][root.rotate]
            size: [root.width/2 - 5,root.height][root.rotate], [root.height,root.width/2 - 5][root.rotate]
            pos_hint: {'right':1, 'y':0}
            BoxLayout:
                id: rightLayout  

    """)
    class LeftRightSplitLayout(FloatLayout):
        def __init__(self, **kwargs):

            super(LeftRightSplitLayout, self).__init__(**kwargs)


        def pressByPlayer(self, player):
            pass

        def addToMiddl(self, widget):
            self.middleLayout.add_widget(widget)


