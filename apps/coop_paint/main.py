from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.scatterlayout import ScatterLayout
from kivy.graphics import Color, Ellipse, Line
from kivy.lang import Builder



class PaintAreaWidget(BoxLayout):

    def on_touch_down(self, touch):
        print "on touch down"
        with self.canvas:
            Color(1, 1, 0)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

        

    def on_touch_move(self, touch):
        if 'line' in touch.ud:
            touch.ud['line'].points += [touch.x, touch.y]


Builder.load_string("""
<TopCtrlWidget>:
    Button:
        text: "Fobar"
"""
)
class TopCtrlWidget(BoxLayout):
    pass


class BoxStencil(BoxLayout, StencilView):
    pass

Builder.load_string("""
<PaintWidget>:
    orientation: 'vertical'
    TopCtrlWidget:
        id: topCtrlWidget
        size_hint: (1,0.1)
    BoxStencil:
        size_hint: (1,0.1)
        ScatterLayout:
            translation_touches: 2
            #BoxLayout:
            PaintAreaWidget:
                id: paintAreaWidget
    TopCtrlWidget:
        size_hint: (1,0.1)
        id: topCtrlWidget
"""
)
class PaintWidget(BoxLayout):
    pass









class MyPaintApp(App):

    def build(self):
        return PaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()
