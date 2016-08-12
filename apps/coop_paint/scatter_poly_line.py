from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatter import Scatter
from kivy.graphics import Color, Ellipse, Line,Rectangle
from kivy.graphics.instructions import Instruction,InstructionGroup

import numpy
import math

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









class ScatterPolyLineWidget(Scatter):
    
    def __init__(self,paintWidget,**kwargs):

        self.paintWidget = paintWidget
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

        super(ScatterPolyLineWidget, self).__init__(**kwargs)


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



        self.boundingBoxGroup = InstructionGroup()
        self.boundingBoxGroup.add(Color(1, 1, 1, 0.4))
        self.boundingBoxGroup.add(Line(rectangle=(0,0,self.width,self.height),dash_offset=2))
        self.isSelected = False
        self.selectedBy = None
        self.canvas.add(self.lg)

        
        # the bounding box
    def select(self,touchId):
        self.paintWidget.selectedItem = self
        self.isSelected = True
        self.selectedBy = touchId
        self.canvas.add(self.boundingBoxGroup)

    def unselect(self):
        self.paintWidget.selectedItem = None
        self.isSelected = False
        self.canvas.remove(self.boundingBoxGroup)

    def minDist(self, p):

        d = float('inf')

        for c in range(self.points.shape[0]-1):

            lStatrt = self.points[c,:]
            lEnd = self.points[c+1,:]

            d = min(dist(lStatrt[0],lStatrt[1], lEnd[0], lEnd[1], p[0], p[1]), d)

        return d
    

    def collide_point(self, x, y):
        
        if super(ScatterPolyLineWidget,self).collide_point(x,y):

            wPoints = self.to_widget(x,y)

            minDist = self.minDist(wPoints)
            #print wPoints
            #print minDist

            
            if minDist<50.0:
                return True
        else:
            return  False

    def on_touch_down(self, touch):
        if not self.paintWidget.paintAreaBackgroundWidget.isDrawing:
            if self.isSelected or self.paintWidget.selectedItem is None:

                if self.collide_point(*touch.pos):
                    if not self.isSelected:
                        self.select(touch.id)
                    return super(ScatterPolyLineWidget, self).on_touch_down(touch)
                else:
                    return False

    def on_touch_move(self, touch):
        if not self.paintWidget.paintAreaBackgroundWidget.isDrawing:
            if super(ScatterPolyLineWidget, self).on_touch_move(touch):
                pass

    def on_touch_up(self, touch):
        if not self.paintWidget.paintAreaBackgroundWidget.isDrawing:
            print "touch up",touch.id
            if self.isSelected and touch.id == self.selectedBy:
                self.unselect()
            return super(ScatterPolyLineWidget, self).on_touch_up(touch)
