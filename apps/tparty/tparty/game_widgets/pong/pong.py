from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture

from line import LinearFunction

try:
    from ..registered_games import registerGame    
except:
    pass

Builder.load_string("""
<PongPaddle>:



    canvas:
        Color: 
            rgba: self.mainColor
        Rectangle:
            pos: self.x + self.offset, self.y + self.width*0.5
            size: self.width/2.0,  self.height - self.width

        Color: 
            rgba: self.mainColor

        Ellipse:
            pos: self.x, self.y
            size: self.width,self.width
        Ellipse:
            pos: self.x, self.y+self.height-self.width
            size: self.width,self.width       

""")
class PongPaddle(Widget):
    offset = NumericProperty(0)
    score = NumericProperty(0)
    mainColor = ObjectProperty([0,1,1,1])
    def bounce_ball_no_check(self, ball):
        vx, vy = ball.velocity
        offset = (ball.center_y - self.center_y) / (self.height / 2)
        bounced = Vector(-1 * vx, vy)
        vel = bounced * 1.1
        for i in range(2):
            vel[i] = min( 200.0, vel[i])
            vel[i] = max(-200.0, vel[i])
        ball.velocity = vel.x, vel.y + offset




Builder.load_string("""
<PongBall>:
    #size: 50, 50 
    canvas:
        Color: 
            rgba: (1,1,1,1)
        Ellipse:
            pos: self.pos
            size: self.size          
""")
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

Builder.load_string("""
#: import ew kivy.uix.effectwidget
<PongGame>:
    ball: pong_ball
    player0: player_left
    player1: player_right
    labelPlayer0: labelPlayer0
    labelPlayer1: labelPlayer1
    #size_hint: 1,1
    #size: None, None



    FloatLayout:
        size_hint: 1,1

    

        canvas.before:
            Rectangle:
                pos: self.pos
                size: self.size
                texture: root.grassTexture



        canvas:
            Color: 
                rgba: (1,1,1,0.7)
            Rectangle:
                pos: self.center_x-5, 0
                size: 0.01*root.width, self.height
        
        RelativeLayout:
            size_hint: None,None
            pos_hint: {'center_x':0.25, 'center_y':0.25}
            ScatterLayout:
                rotation: 90
                do_rotation: False
                do_scale: False
                do_translation: False
                Label:
                    id: labelPlayer0
                    font_size: 70  
                    text: str(root.player0.score)

        RelativeLayout:
            size_hint: None,None
            pos_hint: {'center_x':0.75, 'center_y':0.75}
            Scatter:
                rotation: -90
                do_rotation: False
                do_scale: False
                do_translation: False
                Label:
                    id: labelPlayer1
                    font_size: 70  
                    text: str(root.player1.score)
            
        PongBall:
            size_hint: 0.05, None
            height: self.width
            id: pong_ball
            center: root.center
            
        PongPaddle:
            mainColor: (242.0/255, 227.0/255, 188.0/255, 1.0)
            offset: self.width*0.5
            size_hint: 0.07, 0.4
            id: player_left
            pos: root.x, root.height/2 - self.height/2
            
        PongPaddle:
            mainColor: (242.0/255, 227.0/255, 188.0/255, 1.0)
            offset: 0.0
            size_hint: 0.07, 0.4 
            id: player_right
            pos: root.width-self.width, root.height/2 - self.height/2
""")
class PongGame(BoxLayout):
    ball = ObjectProperty(None)
    player0 = ObjectProperty(None)
    player1 = ObjectProperty(None)
    grassTexture = ObjectProperty(None)

    def __init__(self,gameLogic, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self.gameLogic = gameLogic
        self.updateEvent = None
        self.startVelMag = 20

        p = 'data/textures/grass/Free_Grass_Texture_TonyTextures.jpg'
        self.grassTexture = Image(source=p).texture
        self.grassTexture.wrap = 'repeat'
        self.grassTexture.uvsize = (2, 2)
        #return Builder.load_string(kv)


    def post_init(self):
        
        print self.size,"wear"
    
        if False:
            s = 200
            self.texture = Texture.create(size=(s, s))
            size = s * s * 3
            buf = [int(x * 255 / size) for x in range(size)]
            buf = b''.join(map(chr, buf))

            self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

            with self.canvas.before:
               self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)

            self.bind(pos=self.update_rect,
                      size=self.update_rect)

    def update_rect(self, *args):
        pass    
        #self.rect.pos = self.pos
        #self.rect.size = self.size




    def initGame(self):
        self.serve_ball()
        self.updateEvent = Clock.schedule_interval(self.update, 1.0 / 60.0)

    def stopGame(self):
        Clock.unschedule(self.updateEvent)


    def serve_ball(self, vel=None):
        if vel is None:
            vel = (self.startVelMag , 0)
            #vel = self.width/1.0,0
        self.ball.center = self.center
        self.ball.velocity = vel


    def update(self, dt):

        pls = [self.player0, self.player1]
        ball = self.ball

        # copy current velocity 
        oldVel = Vector(ball.velocity)
        oldPos = Vector(ball.pos)

        # initial estimate for the new velocity
        newPos = oldPos + oldVel

        # move the ball to the new position
        ball.pos = newPos

        bounced = False

        if oldVel[0] < 0.0:
            if ball.collide_widget(pls[0]):
                pls[0].bounce_ball_no_check(ball)
                bounced = True

            elif newPos[0] <= pls[0].right:
                f = LinearFunction(oldPos, newPos)
                y = f(pls[0].right)
                if y >= pls[0].y and y<= pls[0].top:
                    pls[0].bounce_ball_no_check(ball)
                    bounced = True

        elif oldVel[0] > 0.0:
            # check if right player collides
            if ball.collide_widget(pls[1]) :
                pls[1].bounce_ball_no_check(ball)
                bounced = True

            elif newPos[0] >= pls[1].x:
                f = LinearFunction(oldPos, newPos)
                y = f(pls[1].x)
                if y >= pls[1].y and y<= pls[1].top:
                    pls[1].bounce_ball_no_check(ball)
                    bounced = True

        #bounce ball off bottom or top
        if (ball.y < self.y) or (ball.top > self.top):
            ball.velocity_y *= -1


        if not bounced:
            #went of to a side to score point?
            if self.ball.x < self.x:
                self.player1.score += 1
                if(self.player1.score >= 3):
                    self.playerWon(1)
                else:
                    self.serve_ball(vel=(self.startVelMag, 0))
                


            if self.ball.x > self.right:
                self.player0.score += 1
                if(self.player0.score >= 3):
                    self.playerWon(0)
                else:
                    self.serve_ball(vel=(-1.0*self.startVelMag, 0))


    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player0.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player1.center_y = touch.y


    def playerWon(self, winnerPlayerId):
        self.ball.velocity[0] = 0
        self.ball.velocity[1] = 0
        looserPlayerId = [0, 1][winnerPlayerId==0]
        for pid in range(2):
            labelTxt = ['WIN','LOOSE'][not pid==winnerPlayerId]
            labelColor = [(0,1,0,1),(1,0,0,1)][not pid==winnerPlayerId]
            label = [self.labelPlayer0, self.labelPlayer1][not pid==winnerPlayerId]

            

            label.text = labelTxt
            label.color = labelColor

        scores ={
            winnerPlayerId : 1.0,
            looserPlayerId : 0.0
        }

        def cb(dt):
            self.gameLogic.miniGameDone(scores)
        Clock.schedule_once(cb, 0.5)


try:
    registerGame(PongGame)       
except:
    pass

class PongApp(App):
    def build(self):
        game = PongGame(None)
        
        game.serve_ball()
        game.post_init()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    PongApp().run()
