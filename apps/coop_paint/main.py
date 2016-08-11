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

import math

import numpy



def dist(x1,y1, x2,y2, x3,y3): # x3,y3 is the point
    px = x2-x1
    py = y2-y1

    something = px*px + py*py

    u =  ((x3 - x1) * px + (y3 - y1) * py) / float(something)

    if u > 1:
        u = 1
    elif u < 0:
        u = 0

    x = x1 + u * px
    y = y1 + u * py

    dx = x - x3
    dy = y - y3

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    dist = math.sqrt(dx*dx + dy*dy)

    return dist

class ScatterPolyLine(Scatter):
    def __init__(self,**kwargs):
        super(ScatterPolyLine,self).__init__(**kwargs)
        self.size_hint = None,None
        self.polyLineWidget = PolyLineWidget(**kwargs)
        self.add_widget(self.polyLineWidget)
        self.size = self.polyLineWidget.size
    def collide_point(self, x, y):
        
        if super(ScatterPolyLine,self).collide_point(x,y):

            wPoints = self.polyLineWidget.to_widget(x,y)

            minDist = self.polyLineWidget.minDist(wPoints)
            #print wPoints
            #print minDist

            
            if minDist<5.0:
                return True
        else:
            return  False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            #print "USING TOUCH IN SCATTER"
            return super(ScatterPolyLine, self).on_touch_down(touch)
        else:
            return False

    def on_touch_move(self, touch):
        
        if super(ScatterPolyLine, self).on_touch_move(touch):
            pass

    def on_touch_up(self, touch):
        #print "UP SCATTER"
        return super(ScatterPolyLine, self).on_touch_up(touch)


class PolyLineWidget(RelativeLayout):
    
    def __init__(self,**kwargs):

        self.linePoints = kwargs.pop('linePoints',[])
        self.lineColor = kwargs.pop('lineColor',(1,0,0,1))
        self.lineWidth = kwargs.pop('lineWidth',2.0)

        lp = numpy.array(self.linePoints)
        lpx = lp[::2]
        lpy = lp[1::2]

        minX = float(numpy.min(lpx))
        minY = float(numpy.min(lpy))
        maxX = float(numpy.max(lpx))
        maxY = float(numpy.max(lpy))

        self.minX = minX
        self.minY = minY

        super(PolyLineWidget, self).__init__(**kwargs)


        self.size_hint = None,None
        #self.pos_hint = None,None
        #self.pos = minX,minY
        self.size = maxX-minX, maxY-minY

        self.points = numpy.zeros(shape=(len(lpx),2))

        newPoints = []
        for c,(x,y) in enumerate(zip(lpx,lpy)):
            xx = x-minX
            yy = y-minY
            newPoints.append(xx)
            newPoints.append(yy)
            self.points[c,0] = xx
            self.points[c,1] = yy

        self.l = Line(points=newPoints,width=self.lineWidth)
        self.lg = InstructionGroup()
        self.lg.add(Color(*self.lineColor))
        self.lg.add(self.l)

        #self.lg.add(Color(0, 1, 0, 0.4))
        #self.lg.add(Rectangle(pos=(0, 0), size=self.size))
        self.canvas.add(self.lg)
        
        # the bounding box


    def minDist(self, p):

        d = float('inf')

        for c in range(self.points.shape[0]-1):

            lStatrt = self.points[c,:]
            lEnd = self.points[c+1,:]

            d = min(dist(lStatrt[0],lStatrt[1], lEnd[0], lEnd[1], p[0], p[1]), d)

        return d
            
    
class PaintAreaBackgroundWidget(RelativeLayout):

    selectedColor = ListProperty([1,0,0,1])

    def __init__(self, *args, **kwargs):
        super(PaintAreaBackgroundWidget, self).__init__(*args, **kwargs)

        self.lineGroup = None
        self.line = None


    def on_touch_down(self, touch):
        #print "using touch in bg"
        if self.collide_point(*touch.pos):
            width = self.lineWidth
            self.lineGroup = InstructionGroup()
            #print self.lineGroup
            self.line = Line(points=(touch.x, touch.y),width=width)
            self.lineGroup.add(Color(*self.selectedColor))
            self.lineGroup.add(self.line)
            self.canvas.add(self.lineGroup)

    def on_touch_move(self, touch):
        #print "MOVE BG"
        if self.collide_point(*touch.pos):
            self.line.points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and len(self.line.points)!=0:
                

            self.canvas.remove(self.lineGroup)

            lp = numpy.array(self.line.points)
            scatterPolyLine = ScatterPolyLine(linePoints=lp, lineWidth=self.lineWidth, lineColor=self.selectedColor)


            self.line.points = []
    
            scatterPolyLine.pos =  [scatterPolyLine.polyLineWidget.minX,
                                    scatterPolyLine.polyLineWidget.minY]
            #.size = polyLineWidget.size
            self.addPaintedThingsWidget.add_widget(scatterPolyLine)
                #self.addedOne = True

class FloatStencil(FloatLayout, StencilView):
    pass


Builder.load_string("""
<PaintWidget>:
    orientation: 'vertical'
    
    
    

    CtrlWidget:
        id: ctrlWidget
        size_hint: (1,0.2)
        #pos_hint: {'x':0,'top':1.000}

   
    

    FloatStencil:
        PaintAreaBackgroundWidget:
        

            size_hint: 1,1
            selectedColor: ctrlWidget.selectedColor
            lineWidth: ctrlWidget.lineWidth
            addPaintedThingsWidget: addPaintedThingsWidget

            
        FloatLayout:
            id: addPaintedThingsWidget

"""
)
class PaintWidget(BoxLayout):
    pass









class MyPaintApp(App):

    def build(self):
        return PaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()
