from math import *
from functools import partial
import re

import kivy
kivy.require('1.0.6') # replace with your current kivy version !

from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.lang import Builder


saveList =  ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 
'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
#use the list to filter the local namespace
safeDict = dict([ (k, locals().get(k, None)) for k in saveList ])
#add any needed builtins back in.
safeDict['abs'] = abs


def funcOfX(x, userString):
    global safeDict
    safeDict['x']=x
    y = eval(userString,{"__builtins__":None}, safeDict)
    return y

def dx(f, x):
    return abs(0-f(x))

def df(f, x, h):
    return (f(x+h)  - f(x-h))/h

def newtonsMethod(f, x0, e=0.000000001, roundDigits=6, maxIter = 10000000, h=0.00001):

    delta = abs(0-f(x0))
    iteration = 0
    while delta > e:
        x0 = x0 - f(x0)/df(f, x0, h=h)
        delta = abs(0-f(x0))
        iteration +=1
        if iteration >= maxIter:
            raise RuntimeError("to many iterations")

    x0 = round(x0, roundDigits)
    y0 = round(f(x0), roundDigits)

    print 'Root is at: ', x0
    print 'f(x) at root is: ', y0
    return x0, y0


class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


def genPopup(title, buttonText="OK"):
    closeButton = Button(text=buttonText)
    popup = Popup(title=title, content=closeButton,
      auto_dismiss=True, size_hint=(None, None), size=(400, 200))
    popup.open()
    def buttonOnPres():
        popup.dismiss()
    closeButton.on_press  = buttonOnPres



Builder.load_string("""
<NewtonSolverWidget>:

    resultLabel: resultLabel
    x0Input: x0Input
    hInput: hInput
    epsInput: epsInput

    orientation: 'vertical'
    BoxLayout:
        size_hint: (1, 0.8)
        orientation: 'horizontal'
        Label:
            text: "f(x) = "
            size_hint: (0.1,1)
        TextInput:
            id: functionTextInput
            size_hint: (0.7,1)
            text: "x"
            #background_color: (0,0,0,0)
            #color: (0.3,1,0.3,1)
            #font_size: 80
        Button:
            size_hint: (0.2,1)
            text: "Ok"
            on_press: root.finishedEdit(functionTextInput.text)
    BoxLayout:
        size_hint: (1, 0.1)
        orientation: 'horizontal'

        BoxLayout:
            orientation: 'horizontal'
            Label:
                size_hint: (0.3, 1)
                text: "x0:"
            TextInput:
                id: x0Input
                size_hint: (0.7, 1)
                text: "0.0"

        BoxLayout:
            orientation: 'horizontal'
            Label:
                size_hint: (0.3, 1)
                text: "h:"
            TextInput:
                id: hInput
                size_hint: (0.7, 1)
                text: "0.0000001"

        BoxLayout:
            orientation: 'horizontal'
            Label:
                size_hint: (0.3, 1)
                text: "eps:"
            TextInput:
                id: epsInput
                size_hint: (0.7, 1)
                text: "0.0000001"


    Label:
        id: resultLabel
        size_hint: (1, 0.2)
        text: "the result is:"
"""
)
class NewtonSolverWidget(BoxLayout):
    
    def __init__(self,*args, **kwargs):
        super(NewtonSolverWidget, self).__init__(*args, **kwargs)
        self.functionText = "x"
        self.function = None
        self.doNewtonMethod = True
        self.updateFunctionFromText(self.functionText)

    def updateFunctionFromText(self, text):



        self.function = partial(funcOfX, userString=text)
        x0 = float(self.x0Input.text)

        try:
            self.doNewtonMethod = True
            self.function(x0)
        except NameError as e:
            self.doNewtonMethod = False
            genPopup('InvalidFunction','OK')
        except ValueError as e:
            self.doNewtonMethod = False
            genPopup('Math Error','OK')
        except SyntaxError as e:
            self.doNewtonMethod = False
            genPopup('SyntaxError','OK')
        except Exception as e:
            self.doNewtonMethod = False
            genPopup('Unknown Error %s'%str(e),'OK')



    def finishedEdit(self, text):
        print "finished edit",text
        self.updateFunctionFromText(text)
        self.functionText = text

        if self.doNewtonMethod:
            print "do newton method"
            try:
                x0, y0 = newtonsMethod(f=self.function, x0=float(self.x0Input.text), 
                    e=float(self.epsInput.text), h=float(self.hInput.text))
                self.resultLabel.text = "the result is: f( %f ) = %f "%(x0, y0)
            except ZeroDivisionError as e:
                genPopup('ZeroDivision Error, maybe try a differrent staring point','OK')
            except Exception as e:
                genPopup('Unknown Error %s'%str(e),'OK')

        else:
            self.resultLabel.text = "invalid function"

class NewtonSolverApp(App):

    def build(self):
        return NewtonSolverWidget()

    def on_pause(self):
        return True

if __name__ == '__main__':
    NewtonSolverApp().run()
