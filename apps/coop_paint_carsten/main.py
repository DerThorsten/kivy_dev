import kivy
kivy.require('1.9.1') # replace with your current kivy version !
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import mainthread

import sys
import zmq
import json
import threading

class MyPaintWidget(Widget):
    color = None
    outgoingSocket = None
    myId = None

    def on_touch_down(self, touch):
        self.color = (random.random(), 1, 1)
        with self.canvas:
            Color(*self.color, mode='hsv')
            # d = 30.
            # Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        print(touch)
        touch.ud['line'].points += [touch.x, touch.y]
    
    def on_touch_up(self, touch):
        # serialize line and send via server
        messageDict = {
            "id": self.myId,
            "color": list(self.color), 
            "points": list(touch.ud['line'].points) 
        }
        message = json.dumps(messageDict)
        print("Sending message: " + message)
        self.outgoingSocket.send(message)
    
    @mainthread
    def addLine(self, color, points):
        with self.canvas:
            Color(*color, mode='hsv')
            Line(points=points)

def networkReceiver(widget, inputSocket, myId):
    print("Starting listener thread")
    while True:
        message = inputSocket.recv()
        print("received message: " + message)
        messageDict = json.loads(message)
        if messageDict['id'] != myId:
            widget.addLine(messageDict['color'], messageDict['points'])

class MyPaintApp(App):

    def networkingSetup(self):
        context = zmq.Context()
        self.myId = random.randint(0,100000000)
        print("Starting instance with ID {}".format(self.myId))

        outgoingPort = "5559"
        self.outgoingSocket = context.socket(zmq.PUB)
        self.outgoingSocket.connect("tcp://localhost:%s" % outgoingPort)

        incomingPort = "5560"
        self.inputSocket = context.socket(zmq.SUB)
        self.inputSocket.connect("tcp://localhost:%s" % incomingPort)
        self.inputSocket.setsockopt(zmq.SUBSCRIBE, "")

    def build(self):

        self.networkingSetup()

        parent = Widget()
        self.painter = MyPaintWidget()
        self.painter.outgoingSocket = self.outgoingSocket
        self.painter.myId = self.myId

        # start thread that waits for network input
        t = threading.Thread(target=networkReceiver, args=[self.painter, self.inputSocket, self.myId])
        t.setDaemon(True) # daemon threads are killed automatically when the program quits
        t.start()

        parent.add_widget(self.painter)
        return parent

if __name__ == '__main__':
    MyPaintApp().run()
    
