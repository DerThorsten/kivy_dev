from kivy.app import App
#from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scatterlayout import ScatterLayout,ScatterPlane
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.graphics import *

from kivy.graphics.instructions import InstructionGroup


import numpy
import pybox2d as b2d

from debug_draw import DrawKivy
from callbacks import AABBCallback



class PhysicalWorld(object):
    def __init__(self,gravity=b2d.vec2(0,-9.81), debugDrawGroup=None):
        self.debugDrawGroup = debugDrawGroup
        self.world = b2d.b2World(gravity)
        self.groundbody = self.world.createStaticBody()
        self.ppm = 50
        self.offset = (0,0)
        self.debugDraw = DrawKivy(self.debugDrawGroup)
        self.debugDraw.appendFlags([
                'shape',
                'joint',
                'aabb',
                'pair',
                'centerOfMass',
                'particle'
        ])
        self.world.setDebugDraw(self.debugDraw)


    def step(self, dt, doDebugDraw):

        if doDebugDraw:
            self.debugDrawGroup.clear()
            self.debugDrawGroup.add(PushMatrix())
            self.debugDrawGroup.add(Translate(self.offset[0], self.offset[1]))
            self.debugDrawGroup.add(Scale(self.ppm))

        self.world.step(dt, 5, 5, 3)

        if doDebugDraw:
            self.world.drawDebugData()
            self.debugDrawGroup.add(PopMatrix())





class ContactListener(b2d.ContactListener):

    def __init__(self, box2dWidget):
        super(ContactListener,self).__init__()

        self.box2dWidget = box2dWidget

    def beginContact(self, contact):
        self.box2dWidget.beginContact( contact)

    def endContact(self, contact):
        self.box2dWidget.endContact(contact)

    def beginContactParticleBody(self, particleSystem, particleBodyContact):
        self.box2dWidget.beginContactParticleBody(particleSystem, particleBodyContact)

    def beginContactParticle(self, particleSystem, indexA, indexB):
        self.box2dWidget.beginContactParticle(particleSystem, indexA, indexB)

    def endContactParticle(self, particleSystem, indexA, indexB):
        self.box2dWidget.endContactParticle(particleSystem, indexA, indexB)

    def preSolve(self, contact, oldManifold):
        self.box2dWidget.preSolve(contact, oldManifold)

    def postSolve(self, contact, impulse):
        self.box2dWidget.postSolve(contact, impulse)


class DestructionListener(b2d.DestructionListener):

    def __init__(self, box2dWidget):
        super(DestructionListener,self).__init__()
        self.box2dWidget = box2dWidget
    def sayGoodbyeJoint(self, joint):
        self.box2dWidget.sayGoodbyeJoint(joint)
    def sayGoodbyeFixture(self, fixture):
        self.box2dWidget.sayGoodbyeFixture(fixture)
    def sayGoodbyeParticleGroup(self, particleGroup):
        self.box2dWidget.sayGoodbyeParticleGroup(particleGroup)
    def sayGoodbyeParticleSystem(self, particleSystem,index):
        self.box2dWidget.sayGoodbyeParticleSystem(particleSystem, index)



class ContactFilter(b2d.ContactFilter):

    def __init__(self, box2dWidget):
        super(ContactFilter,self).__init__()
        self.box2dWidget = box2dWidget

    def shouldCollideFixtureFixture(self, fixtureA, fixtureB):
        self.box2dWidget.shouldCollideFixtureFixture(fixtureA, fixtureB)

    def shouldCollideFixtureParticle(self, fixture, particleSystem, particleIndex):
        self.box2dWidget.shouldCollideFixtureParticle(fixture, particleSystem, particleIndex)

    def shouldCollideParticleParticle(self, particleSystem, particleIndexA, particleIndexB):
        self.box2dWidget.shouldCollideParticleParticle(particleSystem, particleIndexA, particleIndexB)





class Box2DWidgetSettings(object):
    def __init__(self):
        self.ignoreSensorFixturesOnTouch = True
        self.doDebugDraw = True


Builder.load_string("""
#: import ew kivy.uix.effectwidget
<Box2DWidget>:

""")
class Box2DWidget(ScatterPlane):
 

    def __init__(self, settings=None, nLayers = 10, **kwargs):
        super(Box2DWidget, self).__init__(**kwargs)
        
        self.settings = settings
        if settings is None:
            self.settings = Box2DWidgetSettings()

        self.nLayers = nLayers        
        self.layers = [InstructionGroup() for x in range(nLayers)]

        # add all layers to canvas
        for i in range(nLayers):
            self.canvas.add(self.layers[i])

        # add debug draw to the top layer
        self.debugDrawGroup = InstructionGroup()
        self.layers[nLayers-1].add(self.debugDrawGroup) 

        
        self.physicalWorld = PhysicalWorld(debugDrawGroup=self.debugDrawGroup)
        self.groundbody = self.physicalWorld.groundbody
        self.world = self.physicalWorld.world
        self.ppm = 50
        self.offset = (0,0)
        self.physicalWorld.ppm = self.ppm
        self.physicalWorld.offset = self.offset
        self.nTouchDown = 0
        self.fixtureTouch = dict()



        # install contact listener
        self.contactListener = ContactListener(self)
        self.world.setContactListener(self.contactListener)

        # install destruction listener
        self.destructionListener = DestructionListener(self)
        self.world.setDestructionListener(self.destructionListener)

        # install contact filter
        self.contactFilter = ContactFilter(self)
        self.world.setContactFilter(self.contactFilter)


    def update_rect(self, *args):
        pass    

    def initGame(self):
        self.updateEvent = Clock.schedule_interval(self.update, 1.0 / 60.0)

    def stopGame(self):
        Clock.unschedule(self.updateEvent)

    def update(self, dt):
        self.physicalWorld.step(dt,self.settings.doDebugDraw)

    def on_touch_down(self, touch):
        self.nTouchDown += 1
        if touch.is_mouse_scrolling:
            #print touch.button
            if touch.button == 'scrolldown':
                self.zoomIn()
            else:
                self.zoomOut()
        else:
            touchPos = touch.pos
            localTouchPos = self.to_local(*touchPos)
            p = self.widgetToWorldCoord(localTouchPos)
           

            box =  b2d.aabb(lowerBound=p - b2d.vec2(0.001, 0.001),
                      upperBound=p + b2d.vec2(0.001, 0.001))

            ignoreSensors = self.settings.ignoreSensorFixturesOnTouch
            query = AABBCallback(p,ignoreSensorFixtures=ignoreSensors)
            self.world.queryAABB(query, box)

            if query.fixture is not None:
                fixture = query.fixture
                body = fixture.body
               
                self.fixtureTouch[touch.id] = fixture 
                self.on_touch_down_fixture(touch, p, fixture)
            else:
                super(Box2DWidget, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.id in self.fixtureTouch:
            wpos = self.widgetToWorldCoord(self.to_local(*touch.pos))
            pwpos = self.widgetToWorldCoord(self.to_local(*touch.ppos))
            self.on_touch_move_fixture(touch, wpos, pwpos, self.fixtureTouch[touch.id])
        else:
            super(Box2DWidget, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.id in self.fixtureTouch:
            
            p = self.widgetToWorldCoord(self.to_local(*touch.pos))
            self.on_touch_up_fixture(touch, p, self.fixtureTouch[touch.id])
            del self.fixtureTouch[touch.id]
        else:
            super(Box2DWidget, self).on_touch_up(touch)


    def on_touch_down_fixture(self, touch, wpos, fixture):
        pass
    def on_touch_move_fixture(self, touch, wpos, pwpos, fixture):
        pass

    def on_touch_up_fixture(self, touch, wpos, fixture):
        pass

    def widgetToWorldCoord(self, pos):
        pos = numpy.array(pos)
        offset = numpy.array(self.offset)
        pos -= (offset[0], offset[1])
        pos /= self.ppm
        
        return pos


    def zoomIn(self):
        self.scale = self.scale * 1.5
    def zoomOut(self):
        self.scale = self.scale / 1.5


    def createMouseJoint(self, body, target, maxForceMult=10000.0 ):
        mj = self.world.createMouseJoint(
            bodyA=self.groundbody,
            bodyB=body,
            target=b2d.vec2(target),
            maxForce=maxForceMult * body.mass)   
        return mj


    # CONTACT LISTENER
    def beginContact(self, contact):
        pass
    def endContact(self, contact):
        pass
    def beginContactParticleBody(self, particleSystem, particleBodyContact):
        pass
    def beginContactParticle(self, particleSystem, indexA, indexB):
        pass
    def endContactParticle(self, particleSystem, indexA, indexB):
        pass
    def preSolve(self, contact, oldManifold):
        pass
    def postSolve(self, contact, impulse):
        pass

    # DESTRUCTION LISTENER
    def sayGoodbyeJoint(self, joint):
        pass
    def sayGoodbyeFixture(self, fixture):
        pass
    def sayGoodbyeParticleGroup(self, particleGroup):
        pass
    def sayGoodbyeParticleSystem(self, particleSystem,index):
        pass

    # CONTACT FILTER
    def shouldCollideFixtureFixture(self, fixtureA, fixtureB):
        pass
    def shouldCollideFixtureParticle(self, fixture, particleSystem, particleIndex):
        pass
    def shouldCollideParticleParticle(self, particleSystem, particleIndexA, particleIndexB):
        pass   