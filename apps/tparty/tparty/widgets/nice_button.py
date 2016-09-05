from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.lang import Builder





Builder.load_string("""
<NiceLabel>:
    mainColor: 0,0,0.1,0.1
    borderColor: 0,1,1,1
    borderColor2: 0,0.7,0.7,0.7
    canvas.before:

        Color:
            rgba: self.borderColor2
        RoundedRectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.borderColor
        RoundedRectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.width-4, self.height-4

        Color:
            rgba: root.mainColor
        RoundedRectangle:
            pos: self.pos[0]+10, self.pos[1]+10
            size: self.width-20, self.height-20

    canvas.after:
        Color:
            rgba: 0,0,0,0
    font_name: 'SuperMario256'
    #font_size: self.height*0.70
    background_color: (0,0,0,0)
""")
class NiceLabel(Label):
    pass



Builder.load_string("""
<NiceButton>:
    mainColor: 0,0,0.2,0.2
    borderColor: 0,1,1,1
    borderColor2: 0,0.7,0.7,0.7
    canvas.before:

        Color:
            rgba: self.borderColor2
        RoundedRectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.borderColor
        RoundedRectangle:
            pos: self.pos[0]+2, self.pos[1]+2
            size: self.width-4, self.height-4

        Color:
            rgba: root.mainColor
        RoundedRectangle:
            pos: self.pos[0]+10, self.pos[1]+10
            size: self.width-20, self.height-20

    canvas.after:
        Color:
            rgba: 0,0,0,0
    font_name: 'SuperMario256'
    #font_size: self.height*0.70
    background_color: (0,0,0,0)
""")
class NiceButton(Button):
    pass


Builder.load_string("""
<AutoSizeNiceButton>:
    font_size: self.height*0.70
""")
class AutoSizeNiceButton(NiceButton):
    pass
