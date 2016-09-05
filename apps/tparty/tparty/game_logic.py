from game_widgets import getGameReg

import random 

class GameLogic(object):
    def __init__(self):
        self.gameScreenManager = None
        self.scores = [0,0]
        self.gameReg = getGameReg()

    def randomMiniGame(self):

        index = random.randint(0, len(self.gameReg)-1)
        MiniGame = self.gameReg[index]
        miniGame = MiniGame(self)
        miniGame.post_init()
        return miniGame


    def miniGameDone(self, scores):
        
        for playerId in scores.keys():
            self.scores[playerId] += scores[playerId]

        assert self.gameScreenManager is not None
        self.gameScreenManager.current = 'betweemMiniGameScreen'



__gameLogic = GameLogic()



def getGameLogic():
    global __gameLogic
    return __gameLogic
