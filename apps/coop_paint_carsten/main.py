import kivy
kivy.require('1.9.1') # replace with your current kivy version !
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Line
from kivy.clock import mainthread

import sys
import cooppaintsocket
import json
import threading
import socket

class MyPaintWidget(Widget):
    color = None
    socket = None
    myId = None
    lock = None

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
        if self.color is not None and 'line' in touch.ud and len(touch.ud['line'].points) > 0:
            messageDict = {
                "id": self.myId,
                "color": list(self.color), 
                "points": list(touch.ud['line'].points) 
            }
            message = json.dumps(messageDict)
            print("Sending message: " + message)
            with self.lock:
                print("Beginning to send...")
                self.socket.send(message)
    
    @mainthread
    def addLine(self, color, points):
        with self.canvas:
            Color(*color, mode='hsv')
            Line(points=points)

class MyPaintApp(App):

    def networkingSetup(self):
        """
        Set up a ZMQ context and an incoming and outgoing socket
        """
        serverIp = self.config.get('CoopPaint', 'ip')
        print("Starting instance with ID {}, connecting to server at {}".format(self.myId, serverIp))

        port = 5559
        self.socket = cooppaintsocket.CoopPaintSocket(serverIp, port)
    
    def networkReceiver(self):
        print("Starting listener thread")
        while True:
            # with self.lock:
            try:
                message = self.socket.receive()
            except socket.error:
                message = None
            if message is not None:
                print("received message: " + message)
                messageDict = json.loads(message)
                if messageDict['id'] != self.myId:
                    self.painter.addLine(messageDict['color'], messageDict['points'])
    
    def teardownNetwork(self):
        print("Closing socket")
        self.socket.close()

    def build(self):
        """
        Setup networking, start listener thread, and create the main painting widget
        """
        self.myId = random.randint(0,100000000)
        self.lock = threading.Lock()

        with self.lock:
            self.networkingSetup()

        parent = Widget()
        self.painter = MyPaintWidget()
        self.painter.socket = self.socket
        self.painter.myId = self.myId
        self.painter.lock = self.lock # lock needed to stop reading once we're changing the network config

        # start thread that waits for network input
        t = threading.Thread(target=self.networkReceiver)
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

    def on_stop(self):
        with self.lock:
            self.teardownNetwork()
    
    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        print("main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
              config, section, key, value))

        if section == "CoopPaint":
            if key == "ip":
                with self.lock:
                    self.teardownNetwork()
                    self.networkingSetup()
                    self.painter.socket = self.socket

if __name__ == '__main__':
    MyPaintApp().run()
    
