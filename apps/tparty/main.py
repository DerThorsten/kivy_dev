from kivy.app import App
from kivy.core.text import LabelBase  


from tparty.game_logic import getGameLogic
from tparty.screens import GameScreenManager

import pybox2d

# register font
LabelBase.register(name="SuperMario256",  
                    fn_regular="data/fonts/SuperMario256.ttf",
                   fn_bold="data/fonts/SuperMario256.ttf",
                   fn_italic="data/fonts/SuperMario256.ttf",
                   fn_bolditalic="data/fonts/SuperMario256.ttf")


class TabletPartyApp(App):
    def build(self):

        gameScreenManager = GameScreenManager()
        gameLogic = getGameLogic()
        gameLogic.gameScreenManager = gameScreenManager

        return gameScreenManager                #                #canvas.before:
                #    #Rectangle:
                #    #    pos: self.pos
                #    #    size: self.size
                #    #    #source: 'data/images/rounded.png'background_color: (0,0,0,0)
            #Image:
            #    source: 'data/images/rounded.png'
            #    y: self.parent.y
            #    x: self.parent.x
            #    size: root.width, root.startButton.height
            #    allow_stretch: True
            #    keep_ratio: False


if __name__ == '__main__':
    TabletPartyApp().run()
