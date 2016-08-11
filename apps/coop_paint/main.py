from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter,ScatterPlane
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse, Line
from kivy.lang import Builder
from kivy.properties import *
from kivy.graphics.instructions import Instruction,InstructionGroup
from ctrl_widget import CtrlWidget

import numpy



class MyScatter(Scatter):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print "scatter down"
            self.bg.doPaint = False
        super(MyScatter,self).on_touch_down(touch)
            
    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            print "scatter move"
        super(MyScatter,self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            print "scatter up"
            self.bg.doPaint = True
        super(MyScatter,self).on_touch_up(touch)
        

class PaintAreaBackgroundWidget(FloatLayout):

    selectedColor = ListProperty(None)

    def __init__(self, *args, **kwargs):
        super(PaintAreaBackgroundWidget, self).__init__(*args, **kwargs)

        self.lineGroup = None
        self.line = None

        self.doPaint = True

    def on_touch_down(self, touch):
        #print "bruu"
        if self.doPaint and self.collide_point(*touch.pos):
            width = self.lineWidth
            self.lineGroup = InstructionGroup()
            print self.lineGroup
            self.line = Line(points=(touch.x, touch.y),width=width)
            self.lineGroup.add(Color(*self.selectedColor))
            self.lineGroup.add(self.line)
            self.canvas.add(self.lineGroup)
            
    def on_touch_move(self, touch):
        #print "bruu move"
        if self.doPaint and self.collide_point(*touch.pos):
            self.line.points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.doPaint and self.collide_point(*touch.pos):
            self.canvas.remove(self.lineGroup)

            lp = numpy.array(self.line.points)
            lpx = lp[::2]
            lpy = lp[1::2]
            print lpx.shape,lpy.shape

            s = MyScatter()
            #s.size_hint = (1,1)
            
            
            w  = Widget()

            minX = float(numpy.min(lpx))
            minY = float(numpy.min(lpy))
            maxX = float(numpy.max(lpx))
            maxY = float(numpy.max(lpy))


            s.size_hint = None,None
            s.pos = minX,minY

            s.bg = self
            #w.pos = minX,minY+100
            
            s.size = maxX-minX,maxY-minY
            s.add_widget(w)



            newPoints = []
            for x,y in zip(lpx,lpy):
                xx = x-minX
                yy = y-minY
                newPoints.append(xx)
                newPoints.append(yy)

            l = Line(points=newPoints,width=self.line.width)
            lg = InstructionGroup()
            lg.add(Color(*self.selectedColor))
            lg.add(l)

            self.line.points = []
            w.canvas.add(lg)
            self.addPaintedThingsWidget.add_widget(s)




class BoxStencil(BoxLayout, StencilView):
    pass


Builder.load_string("""
<PaintWidget>:
    orientation: 'vertical'
    
    BoxStencil:
        BoxLayout:
            #FloatLayout:
            #    id: addPaintedThingsWidget
    
    FloatLayout:
        id: addPaintedThingsWidget
    CtrlWidget:
        id: ctrlWidget
        size_hint: (1,0.2)
        pos_hint: {'x':0,'top':1.000}
    
    PaintAreaBackgroundWidget:
    

        size_hint: 1,1
        selectedColor: ctrlWidget.selectedColor
        lineWidth: ctrlWidget.lineWidth
        addPaintedThingsWidget: addPaintedThingsWidget


"""
)
class PaintWidget(FloatLayout):
    pass









class MyPaintApp(App):

    def build(self):
        return PaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()
