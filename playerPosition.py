from gameEvent import *
from item import *

class playerPosition(gameEvent):
    def __init__(self,row):
        gameEvent.__init__(self, row[1], row[0], row[3], row[4], row[5], row[6])
        self.gameTime = row[2]