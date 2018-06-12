from gameEvent import *

class swimStart(gameEvent):
    def __init__(self,row):
        gameEvent.__init__(self, row[1], row[0], row[2], row[3], row[4], row[5])