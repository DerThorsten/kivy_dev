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
        if self.color is not None and len(touch.ud['line'].points) > 0:
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

def networkReceiver(widget, incomingSocket, myId):
    print("Starting listener thread")
    while True:
        message = incomingSocket.recv()
        print("received message: " + message)
        messageDict = json.loads(message)
        if messageDict['id'] != myId:
            widget.addLine(messageDict['color'], messageDict['points'])

class MyPaintApp(App):

    def networkingSetup(self):
        """
        Set up a ZMQ context and an incoming and outgoing socket
        """
        serverIp = self.config.get('CoopPaint', 'ip')
        print("Starting instance with ID {}, connecting to server at {}".format(self.myId, serverIp))

        outgoingPort = "5559"
        self.outgoingSocket = self.context.socket(zmq.PUB)
        self.outgoingSocket.connect("tcp://{}:{}".format(serverIp, outgoingPort))

        incomingPort = "5560"
        self.incomingSocket = self.context.socket(zmq.SUB)
        self.incomingSocket.connect("tcp://{}:{}".format(serverIp, incomingPort))
        self.incomingSocket.setsockopt(zmq.SUBSCRIBE, "")
    
    def teardownNetwork(self):
        # Fixme: because the networkReceiver thread doesn't know that the socket is closed, 
        # it's still trying to read from it and the app will crash when the server is changed.
        self.incomingSocket.close()
        self.outgointSocket.close()

    def build(self):
        """
        Setup networking, start listener thread, and create the main painting widget
        """
        self.context = zmq.Context()
        self.myId = random.randint(0,100000000)
        self.networkingSetup()

        parent = Widget()
        self.painter = MyPaintWidget()
        self.painter.outgoingSocket = self.outgoingSocket
        self.painter.myId = self.myId

        # start thread that waits for network input
        t = threading.Thread(target=networkReceiver, args=[self.painter, self.incomingSocket, self.myId])
        t.setDaemon(True) # daemon threads are killed automatically when the program quits
        t.start()

        parent.add_widget(self.painter)
        return parent
    
    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults('CoopPaint', {'ip': 'localhost'})

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        settingsJson = '''
        [
            {
                "type": "string",
                "title": "Server IP",
                "desc": "Server IP address",
                "section": "CoopPaint",
                "key": "ip"
            }
        ]
        '''

        settings.add_json_panel('CoopPaint', self.config, data=settingsJson)
    
    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        print("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
              config, section, key, value))

        if section == "CoopPaint":
            if key == "ip":
                self.teardownNetwork()
                self.networkingSetup()

if __name__ == '__main__':
    MyPaintApp().run()
    
