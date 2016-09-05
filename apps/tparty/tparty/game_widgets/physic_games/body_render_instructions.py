from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import *
import math



class BodyRenderInstructionBase(object):
    def __init__(self, body, instruction, offset=None):
        #self.size = size
        self.body = body
        self.instructionGroup = InstructionGroup()



        self.instructionGroup.add(PushMatrix())

        self.s = Scale(50.0)
        self.t = Translate(0,0)
        self.r = Rotate(0.0)

        #self.rect  = Rectangle(pos=(0,0), size=(1, 1))

        self.instructionGroup.add(self.s)
        self.instructionGroup.add(self.t)
        self.instructionGroup.add(self.r)
        if offset is not None:
            self.instructionGroup.add(Translate(offset[0], offset[1]))

        #g = InstructionGroup()
        #g.add(Color(1,1,1,1))
        #g.add(self.rect)

        self.instructionGroup.add(instruction)

        #self.instructionGroup.add(Color(1,1,1,1))
        #self.instructionGroup.add(self.rect)


        self.instructionGroup.add(PopMatrix())

    def update(self):
        self.t.xy = self.body.position
        self.r.angle = math.degrees(self.body.angle)




class TextrueRect(BodyRenderInstructionBase):
    def __init__(self, body, size, texture=None, halfShift=True):

        ig = InstructionGroup()
        ig.add(Color(1,1,1, 1.0))
        ig.add(Rectangle(pos=(0,0), size=size, texture=texture))

        offset = None
        if halfShift:
            offset = [-1.0*s/2.0 for s in size]

        super(TextrueRect, self).__init__(body, instruction=ig, offset=offset)
