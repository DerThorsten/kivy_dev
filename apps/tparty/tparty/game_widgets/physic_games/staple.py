from kivy.app import App
from kivy.core.image import Image as CoreImage
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
#from kivy.graphics import *
from kivy.graphics.texture import Texture
from kivy.graphics.instructions import InstructionGroup
from kivy.logger import Logger
from kivy.clock import Clock

import datetime

import numpy
import pybox2d as b2d
import networkx as nx


from body_render_instructions import *
from box2d_widget import Box2DWidget, Box2DWidgetSettings

from ...left_right_split_layout import LeftRightSplitLayout

try:
    from ..registered_games import registerGame    
except:
    pass




p = "data/images/icebrick.png"
brickTexture = CoreImage.load(p).texture
        

class StableBlock(TextrueRect):
    def __init__(self, *args, **kwargs):
        super(StableBlock, self).__init__(*args, **kwargs)

class GroundBody(object):
    def __init__(self, body):
        self.body = body

    def update(self):
        pass






Builder.load_string("""
<StapleCanvasWidget>:
    
    canvas.before:
        #Color:
        #    rgb: 1, 1, 1
        #Rectangle:
        #    pos: -1024*5,-432*5
        #    size: 1024*15,432*15
        #    texture: root.bgTexture


        Color:
            rgba: (0,0,0,1)
        Rectangle:
            pos: -1024-5,0-5
            size: 1024*3,432*3
            source: "data/images/bg0.jpg"

        Color:
            rgba: (1,1,1,1)
""")
class StapleCanvasWidget(Box2DWidget):
    currentHeight = NumericProperty(0.0)
    bgTexture = ObjectProperty(None)
    def __init__(self, **kwargs):
        
        settings = Box2DWidgetSettings()
        settings.doDebugDraw = False

        super(StapleCanvasWidget, self).__init__(settings=settings, do_rotation=False, **kwargs)
        self.contactGraph = nx.Graph()
        self.bodyInSensor = None
        self.initWorld()
        self.touchMouseJoints = dict()

        self.addBodyInNexyFrame = False
        self.graphics()

        self._set_scale(1.0)

    def on_transform(self, instance, value):
        #print value

        p0 = self.bbox[0]
        p1 = self.bbox[1]
        if p0[1] > 0 :
            self._set_pos((p0[0], 0.0))
        elif p0[0] > 0 :
            self._set_pos((0.0, p0[1]))
        else:
            super(StapleCanvasWidget, self).on_transform(instance, value)


    def graphics(self):

        bgLayer = self.layers[0]

        tileStart = 10, 128
        tileSize = 256

        texBg = CoreImage("data/images/PNG/Background.png").texture
        size = (texBg.width, texBg.height)
        bg = Rectangle(pos=(0, -tileSize), size=size, texture=texBg)
        bgLayer.add(bg)



        texGrassLeft = CoreImage("data/images/PNG/Tile_1.png").texture
        texGrassMid = CoreImage("data/images/PNG/Tile_2.png").texture
        texGrassRight = CoreImage("data/images/PNG/Tile_3.png").texture

        texFreeGrass = CoreImage("data/images/PNG/Tile_13.png").texture

        texDirtLeft = CoreImage("data/images/PNG/Tile_4.png").texture
        texDirtMid = CoreImage("data/images/PNG/Tile_5.png").texture
        texDirtRight = CoreImage("data/images/PNG/Tile_6.png").texture

        texFlower = CoreImage("data/images/PNG/Object_1.png").texture
        texGrassA = CoreImage("data/images/PNG/Object_6.png").texture
        texGrassB = CoreImage("data/images/PNG/Object_7.png").texture

        def placeTile(x,y,tex, z=1):
            tile = Rectangle(pos=(tileStart[0]+ x*tileSize, tileStart[1] +  y*tileSize), size=(256,256), texture=tex)
            self.layers[z].add(tile)


        placeTile(0,  0, texGrassLeft)
        placeTile(0, -1, texDirtLeft)

        for x in range(1,6):
            placeTile(x,  0, texGrassMid)
            placeTile(x, -1, texDirtMid)

        placeTile(6,  0, texGrassRight)
        placeTile(6, -1, texDirtRight)

        

        # place free tile
        placeTile(0.5, 0.5, texFreeGrass,0)

         # place free tile
        placeTile(1, 0.5, texGrassA, 3)
        placeTile(1.5, 0.5, texGrassB, 3)
        placeTile(1.75, 0.5, texGrassA, 3)
        placeTile(2.2, 0.5, texGrassB, 3)

        placeTile(3+1, 0.5, texGrassA, 3)
        placeTile(3+1.5, 0.5, texGrassB, 3)
        placeTile(3+1.75, 0.5, texGrassA, 3)
        placeTile(3+2.2, 0.5, texGrassB, 3)


    def initWorld(self):

        tileSize = 256.0
        sTileSize = 256.0/50.0
        gSize = (3.0*256/50.0, 128.0/50.0)


        self.groundFixture = b2d.fixtureDef(shape=b2d.polygonShape(box=gSize))
        self.ground = self.world.createStaticBody(position=( 3.5*sTileSize, 0.5*sTileSize), fixtures=self.groundFixture)

        gSize = (0.37*256/50.0, 50.0/50.0)
        self.startFixture = b2d.fixtureDef(shape=b2d.polygonShape(box=gSize))
        self.start = self.world.createStaticBody(position=( 1.05*sTileSize, 1.3*sTileSize), fixtures=self.startFixture)

        self.ground.userData = GroundBody(body=self.ground)

        assert isinstance(self.ground.userData, GroundBody)
        self.contactGraph.add_node(self.ground)

        

        # senor for box supply
        self.sensorFixture = b2d.fixtureDef(shape=b2d.polygonShape(box=(3, 3)),isSensor=True)
        self.sensor = self.world.createStaticBody(position=(5, (256.0+128)/50.0 + 3), fixtures=self.sensorFixture)

        # but box into the sensor


        self.putBoxInSensor()

    def putBoxInSensor(self):

        fixture = b2d.fixtureDef(shape=b2d.polygonShape(box=(1, 1)),
                               density=5, friction=0.05)
        body = self.world.createDynamicBody(
                bodyDef=b2d.bodyDef(linearDamping=0.5, angularDamping=0.5),                                          
                position=(5, (256.0+128)/50.0 + 1),
                fixtures=fixture)

        self.bodyInSensor = body



        # graphics
        ud = StableBlock(body, size=(2,2), texture=brickTexture)
        body.userData = ud
        self.layers[2].add(ud.instructionGroup)



    def on_touch_down_fixture(self, touch, wpos, fixture):
        body = fixture.body
        body.awake = True
        self.touchMouseJoints[touch.id] = self.createMouseJoint(body, wpos)

    def on_touch_move_fixture(self, touch, wpos, pwpos, fixture):
        mj = self.touchMouseJoints[touch.id]
        mj.SetTarget(b2d.vec2(wpos))

    def on_touch_up_fixture(self, touch, wpos, fixture):
        self.world.destroyJoint(self.touchMouseJoints[touch.id])
        del self.touchMouseJoints[touch.id]


    def update(self, dt):
        super(StapleCanvasWidget, self).update(dt)

        if self.addBodyInNexyFrame:
            self.putBoxInSensor()
            self.addBodyInNexyFrame = False

        for body in self.world.bodyList:
            ud = body.userData
            if ud is not None:
                ud.update()

                if isinstance(ud, StableBlock):
                    if ud.body.position[1] < -1.0:
                        self.layers[2].remove(ud.instructionGroup)
                        body = ud.body
                        self.world.destroyBody(ud.body)


        self.computeMaximumHeight()

    def computeMaximumHeight(self):
        connectedBlock = nx.node_connected_component(self.contactGraph, self.ground)   
        maxP = 0.0
        for cb in connectedBlock:
            if cb is not self.ground:

                maxP = max(cb.position[1],maxP)

        self.currentHeight = maxP

        #print "max height",self.currentHeight

    def beginContact(self, contact):

        bA = contact.fixtureA.body
        bB = contact.fixtureB.body

        udA = bA.userData
        udB = bB.userData

        if isinstance(udA,(StableBlock, GroundBody)) and isinstance(udB,(StableBlock, GroundBody)):
            if bA != self.bodyInSensor and bB != self.bodyInSensor:
                self.contactGraph.add_edge(bA, bB)


    def endContact(self, contact):
        bA = contact.fixtureA.body
        bB = contact.fixtureB.body

        udA = bA.userData
        udB = bB.userData
  
        if isinstance(udA,(GroundBody, StableBlock)) and isinstance(udB,(GroundBody, StableBlock)):
            self.contactGraph.add_edge(bA, bB)

            try:
                #print "remove node"
                self.contactGraph.remove_edge(bA, bB)
            except:
                pass
        else:
            # check if "new" block is removed
            # from sensor 
            if self.bodyInSensor is not None:
                if (bA == self.sensor and bB == self.bodyInSensor) or \
                   (bB == self.sensor and bA == self.bodyInSensor):
                    self.bodyInSensor = None
                    self.addBodyInNexyFrame = True

    def stopGame(self):
        super(StapleCanvasWidget,self).stopGame()

Builder.load_string("""
<StapleWidget>:
    stapleCanvasWidget: stapleCanvasWidget
    heightLabel: heightLabel
    timeLabel: timeLabel
    winLooseLabel: winLooseLabel
    FloatLayout:
        size_hint: 1,1

        canvas.before:
            Color:
                rgb: 101.0/255, 204.0/255, 153.0/255
            Rectangle:
                pos: self.pos
                size: self.size
                texture: root.bgTexture

        StencilView:
            StapleCanvasWidget:
                id: stapleCanvasWidget
                size_hint: 1,1
                
        Label:
            id: heightLabel
            size_hint: 0.1, 0.1
            pos_hint: {'x':0.2,'top':0.9}
            text: 'height:'+ str(round(stapleCanvasWidget.currentHeight,2))
            font_name: 'SuperMario256'
            font_size: root.height*0.05
            color: (0.2,0.2,0.2,1)

        Label:
            id: timeLabel
            size_hint: 0.1, 0.1
            pos_hint: {'right':0.8,'top':0.9}
            text: '30.0'
            font_name: 'SuperMario256'
            font_size: root.height*0.05
            color: (0.2,0.2,0.2,1)

        Label:
            id: winLooseLabel
            size_hint: 0.1, 0.1
            pos_hint: {'center_x':0.59,'center_y':0.5}
            text: ""
            font_name: 'SuperMario256'
            font_size: root.height*0.2
            color: (0.2,0.2,0.2,1)
""")
class StapleWidget(BoxLayout):

    bgTexture = ObjectProperty()

    def __init__(self,gameLogic, **kwargs):
        super(StapleWidget, self).__init__(**kwargs)

        #p = "data/images/Brick_Block.png"
        #self.bgTexture = CoreImage.load(p).texture
        #self.bgTexture.wrap = 'repeat'
        #self.bgTexture.uvsize = (32, 32)

        self.updateTimeEvent = None
        self.timeStart = None
    def post_init(self):
        pass 
    

    def initGame(self):
        self.stapleCanvasWidget.initGame()



    def stopGame(self):
        self.stapleCanvasWidget.stopGame()


class StapleMiniGame(LeftRightSplitLayout):

    def __init__(self,gameLogic, **kwargs):
        super(StapleMiniGame, self).__init__(**kwargs)
        self.gameLogic = gameLogic





    def post_init(self,dt=None):
        Logger.info("StapleMiniGame: post_init")
     

        self.plrWidgets = [StapleWidget(gameLogic=self.gameLogic) for x in range(2)]


        self.leftLayout.add_widget( self.plrWidgets[0])
        self.rightLayout.add_widget(self.plrWidgets[1])

        for i in range(2):
            self.plrWidgets[i].post_init()


    

    def on_press_menu(self):
        self.miniGameScreen.manager.current = 'menuScreen'

    def initGame(self):
        Logger.info("StapleMiniGame: initGame")
        for i in range(2):
            self.plrWidgets[i].initGame()

        self.updateTimeEvent = Clock.schedule_interval(self.updateTime, 1.0 / 60.0)
        self.timeStart = datetime.datetime.now()

    def updateTime(self, dt):
        now = datetime.datetime.now()

        dt =  now-self.timeStart
        dtsec =  dt.seconds +  dt.microseconds /1000000.0
        tLeft = 40.0 - dtsec
        tLeft = max(0.0, tLeft)

        for i in range(2):
            tl = self.plrWidgets[i].timeLabel
            tl.text = "%.1f"%round(tLeft,2) 
            if tLeft <= 3.0:
                tl.color = (1,0,0,1)

        if tLeft <=0.000000000001:
            Clock.unschedule(self.updateTimeEvent)
            self.getWinner()

    def getWinner(self):
        heights = [self.plrWidgets[i].stapleCanvasWidget.currentHeight for i in range(2)]
        
        if(round(heights[0],3) != round(heights[1],3)):

            winnerPlayerId = [0, 1][heights[1]>heights[0]]
            looserPlayerId = [1, 0][heights[1]>heights[0]]

            scores ={
                winnerPlayerId : 1.0,
                looserPlayerId : 0.0
            }

            self.plrWidgets[winnerPlayerId].winLooseLabel.text = "Winner"
            self.plrWidgets[winnerPlayerId].winLooseLabel.color = (0,1,0,1)
            self.plrWidgets[looserPlayerId].winLooseLabel.text = "Looser"
            self.plrWidgets[looserPlayerId].winLooseLabel.color = (1,0,0,1)

        else:
            scores ={
                0 : 0.0,
                1 : 0.0
            }

            for i in range(2):
                self.plrWidgets[i].winLooseLabel.text = "Draw"
                self.plrWidgets[i].winLooseLabel.color = (0.2,0.2,0.2,1)

        def cb(dt):
            self.gameLogic.miniGameDone(scores)
        Clock.schedule_once(cb, 0.7)


    def stopGame(self):
        for i in range(2):
            self.plrWidgets[i].stopGame()


        
registerGame(StapleMiniGame)       
