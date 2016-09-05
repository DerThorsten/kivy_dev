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




Builder.load_string("""
<CarouselWidget>:
    direction: 'top'
    loop: True
""")
class CarouselWidget(Carousel):
    
    def __init__(self,**kwargs):


        super(CarouselWidget, self).__init__(**kwargs)

        for i in range(10):
            l = Label(text="text %d"%i)
            self.add_widget(l)
    
    def animate(self):
        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(index=0, t='out_bounce')
        animation += Animation(index=9, t='out_bounce')

        # apply the animation on the button, passed in the "instance" argument
        # Notice that default 'click' animation (changing the button
        # color while the mouse is down) is unchanged.
        #animation.start(self)




class CarouselApp(App):
    def build(self):
        w =  CarouselWidget()
        w.animate()
        return w
CarouselApp().run()