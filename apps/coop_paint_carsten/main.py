import kivy
kivy.require('1.9.1') # replace with your current kivy version !
from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line

import zmq
import json

port = "5559"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:%s" % port)

class MyPaintWidget(Widget):
    color = None

    def on_touch_down(self, touch):
        print(touch)
        self.color = (random(), 1, 1)
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
        messageDict = {"color": list(self.color), "points": list(touch.ud['line'].points) }
        message = json.dumps(messageDict)
        print("Sending message: " + message)
        socket.send(message)


class MyPaintApp(App):

    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget()
        clearbtn = Button(text='Clear')
        clearbtn.bind(on_release=self.clear_canvas)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()


if __name__ == '__main__':
    MyPaintApp().run()