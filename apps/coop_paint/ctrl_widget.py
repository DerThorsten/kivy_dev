from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter,ScatterPlane
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.lang import Builder
from kivy.properties import *





Builder.load_string("""

<ColorButton@ToggleButton>:
    group: 'colors'

<CtrlWidget>:
    orientation: 'vertical'

    BoxLayout:
        size_hint: (1,0.8)
        orientation: 'horizontal'
        Button:
            text: "Fobar"

        BoxLayout:
            orientation: 'vertical'
            GridLayout:
                size_hint: (1,0.8)
                cols: 2
                ColorButton:
                    background_color: 1,0,0,1
                    on_press: root.selectedColor = (1,0,0,1)
                    state: 'down'
                ColorButton:
                    background_color: 0,1,0,1
                    on_press: root.selectedColor = (0,1,0,1)
                ColorButton:
                    background_color: 0,0,1,1
                    on_press: root.selectedColor = (0,0,1,1)
                ColorButton:
                    background_color: 1,1,0,1
                    on_press: root.selectedColor = (1,1,0,1)

            Slider:
                on_value: root.lineWidth = self.value
                size_hint: (1,0.2)
                min: 1
                max: 20
                value: 1
    Label:
        size_hint: (1,0.2)
        text: 'space..'

"""
)
class CtrlWidget(BoxLayout):
    
    selectedColor = ListProperty((1,0,0,1))
    lineWidth = NumericProperty(1)

