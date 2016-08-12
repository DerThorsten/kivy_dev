from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
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

from ctrl_widget import CtrlWidget
from scatter_poly_line import ScatterPolyLineWidget

import math
import numpy




    
class PaintAreaBackgroundWidget(RelativeLayout):

    selectedColor = ListProperty([1,0,0,1])

    def __init__(self, *args, **kwargs):
        super(PaintAreaBackgroundWidget, self).__init__(*args, **kwargs)

        self.lineGroup = None
        self.line = None
        self.isDrawing = False

    def on_touch_down(self, touch):

        # only draw if no widget is selected 
        if self.paintWidget.selectedItem is None:

            if self.collide_point(*touch.pos):

                self.isDrawing = True

                width = self.lineWidth
                self.lineGroup = InstructionGroup()
                #print self.lineGroup
                self.line = Line(points=(touch.x, touch.y),width=width,dash_offset=2)
                self.lineGroup.add(Color(*self.selectedColor))
                self.lineGroup.add(self.line)
                self.canvas.add(self.lineGroup)

    def on_touch_move(self, touch):
        if self.paintWidget.selectedItem is None:
            if self.collide_point(*touch.pos):
                self.line.points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.paintWidget.selectedItem is None:
            if self.collide_point(*touch.pos) and len(self.line.points)>1:
                    

                self.canvas.remove(self.lineGroup)

                lp = numpy.array(self.line.points)
                scatterPolyLine = ScatterPolyLineWidget(paintWidget=self.paintWidget,
                    linePoints=lp, lineWidth=self.lineWidth, lineColor=self.selectedColor)


                self.line.points = []
        
                scatterPolyLine.pos =  [scatterPolyLine.minX,
                                        scatterPolyLine.minY]
                #.size = polyLineWidget.size
                self.addPaintedThingsWidget.add_widget(scatterPolyLine)
                #self.addedOne = True
            self.isDrawing = False

class FloatStencil(FloatLayout, StencilView):
    pass


Builder.load_string("""
<PaintWidget>:
    
    # references
    ctrlWidget:                 ctrlWidget
    addPaintedThingsWidget:     addPaintedThingsWidget
    paintAreaBackgroundWidget:  paintAreaBackgroundWidget


    orientation: 'vertical'
    CtrlWidget:
        id: ctrlWidget
        size_hint: (1,0.2)
        #pos_hint: {'x':0,'top':1.000}

   
    

    FloatStencil:
        PaintAreaBackgroundWidget:
            id: paintAreaBackgroundWidget

            size_hint: 1,1
            selectedColor: ctrlWidget.selectedColor
            lineWidth: ctrlWidget.lineWidth

            paintWidget: root
            addPaintedThingsWidget: addPaintedThingsWidget

            
        FloatLayout:
            id: addPaintedThingsWidget

"""
)
class PaintWidget(BoxLayout):
    
    def __init__(self):
        super(PaintWidget, self).__init__()
        self.selectedItem = None









class MyPaintApp(App):

    def build(self):
        return PaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()
