



class RegisteredGames(object):
    
    def __init__(self):
        self.gamesSet = set()
        self.gamesList = list()

    def registerGame(self, game):
        print "register game",str(game)," len(self) ",len(self)
        if game not in self.gamesSet:
            self.gamesSet.add(game)
            self.gamesList.append(game)


    def __len__(self):
        return len(self.gamesList)

    def __getitem__(self, key):
        return self.gamesList[key]

__registeredGames = RegisteredGames()


def getGameReg():
    global __registeredGames
    return __registeredGames


def registerGame(game):
    global __registeredGames
    __registeredGames.registerGame(game)



