from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.graphics import *
import numpy
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import *

from pybox2d import *


class DrawKivy(DebugDraw):

    def __init__(self, instructionGroup, alpha=0.5):
        super(DrawKivy,self).__init__()

        self.alpha = alpha
        self.instructionGroup = instructionGroup

        
    def DrawSolidCircle(self, center, radius, axis, c):
        #print "circle"
        _center = (numpy.array(center)-radius)
        size = numpy.array([radius*2,radius*2])
        #print "color",color
        #with self.canvas:
        print "axis",axis
        a = numpy.array(axis)
        a /= numpy.linalg.norm(a)
        a *= radius
        #a /= 2.0

        p0 = _center - a + radius
        p1 = _center + a + radius

        print p0,p1,_center+radius
        e = Ellipse(pos=_center,size=size)
        l1 = Line(points=[tuple(p0),tuple(p1)], width=1)
        l2 = Line(circle=(center[0], center[1], radius))

        self.instructionGroup.add(Color(c[0],c[1],c[2],self.alpha))
        self.instructionGroup.add(e)
        self.instructionGroup.add(Color(0.75*c[0],0.75*c[1],0.75*c[2],self.alpha))
        self.instructionGroup.add(l1)
        self.instructionGroup.add(Color(0.75*c[0],0.75*c[1],0.75*c[2],self.alpha))
        self.instructionGroup.add(l2)

    def DrawCircle(self, center, radius, c):
        #e = Ellipse(pos=_center,size=size ,color=Color(c[0],c[1],c[2],1.0))
        l = Line(circle=(center[0], center[1], radius))
        self.instructionGroup.add(Color(c[0],c[1],c[2],self.alpha))
        self.instructionGroup.add(l)


    def DrawSegment(self,v1, v2, c):
        l = Line(points=[v1[0],v1[1],v2[0], v2[1]], width=1)
        self.instructionGroup.add(Color(c[0],c[1],c[2],self.alpha))
        self.instructionGroup.add(l)

    def DrawPolygon(self,vertices, c):
        vertices = numpy.array(vertices)
        line = []
        for i in range(vertices.shape[0]):
            line.extend([vertices[i,0],vertices[i,1]])

        line.extend([vertices[0,0],vertices[0,1]])
        l = Line(points=line,width=1)
        
        self.instructionGroup.add(Color(c[0],c[1],c[2],self.alpha))
        self.instructionGroup.add(l)


    def DrawSolidPolygon(self,vertices, c):
        vertices = numpy.array(vertices)
      

        v = [] 
        indices = []
        line = []
        for i in range(vertices.shape[0]):
            v.extend([vertices[i,0],vertices[i,1],0,0])
            indices.append(i)
            line.extend([vertices[i,0],vertices[i,1]])
        m = Mesh(vertices=v,indices=indices,mode='triangle_fan')
        l = Line(points=line)
        
        self.instructionGroup.add(Color(c[0],c[1],c[2],self.alpha))
        self.instructionGroup.add(m)            
        self.instructionGroup.add(Color(0.75*c[0],0.75*c[1],0.75*c[2],self.alpha))
        self.instructionGroup.add(l)

    def DrawParticles(self, centers, radius, colors=None):
        #nparticles = centers.shape[0]
        #pl = []
        #for i in range(nparticles):
        #    pl.append(float(centers[i,0]))
        #    pl.append(float(centers[i,1]))
        p = Point(points=centers.reshape(-1), pointsize=radius)
        self.instructionGroup.add(Color(0,0,1,0.3))
        self.instructionGroup.add(p)

        #for p in range(nparticles):
        #    self.DrawSolidCircle(center=centers[p,:],radius=radius,axis=(1,0),c=(1,1,1))



