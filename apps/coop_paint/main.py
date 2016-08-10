from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import ScatterPlane
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.lang import Builder



class PaintAreaWidget(ScatterPlane):
    pass


class PaintAreaBackgroundWidget(BoxLayout):

    def on_touch_down(self, touch):
        print "on touch down"
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))
        super(PaintAreaBackgroundWidget,self).on_touch_move(touch)
    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]
        super(PaintAreaBackgroundWidget,self).on_touch_move(touch)


Builder.load_string("""
<TopCtrlWidget>:
    Button:
        text: "Fobar"
"""
)
class TopCtrlWidget(BoxLayout):
    pass


Builder.load_string("""
<PaintWidget>:
    orientation: 'vertical'

    PaintAreaWidget:
        translation_touches: 2
        PaintAreaBackgroundWidget:
            size_hint: 1, 1
            pos_hint: {'center_x':0.5,'center_y':0.5}

            canvas:
                Color:
                    rgb: (0.2, 0.2, 0.2)
                Rectangle:
                    pos: self.pos
                    size: self.size

        Scatter:
            Button:
                text: 'fo'
                
    TopCtrlWidget:
        id: topCtrlWidget
        size_hint: (1,0.1)
        pos_hint: {'x':0,'top':1.001}

    TopCtrlWidget:
        size_hint: (1,0.1)
        id: topCtrlWidget


"""
)
class PaintWidget(FloatLayout):
    pass









class MyPaintApp(App):

    def build(self):
        return PaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()
