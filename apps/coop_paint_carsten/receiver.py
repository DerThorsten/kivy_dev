import kivy
kivy.require('1.9.1') # replace with your current kivy version !
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

import zmq
import json
import threading

port = "5560"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, "")

class MyPaintWidget(Widget):
    def addLine(self, color, points):
        with self.canvas:
            Color(*color, mode='hsv')
            Line(points=points)

def networkReceiver(widget):
    print("Starting listener thread")
    while True:
        message = socket.recv()
        print("received message: " + message)
        messageDict = json.loads(message)
        widget.addLine(messageDict['color'], messageDict['points'])

class MyPaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()

        # start thread that waits for network input
        t = threading.Thread(target=networkReceiver, args=[self.painter])
        t.start()

        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()