from gameEvent import *
from item import *

class itemDetach(gameEvent):
    def __init__(self,row):
        gameEvent.__init__(self, row[1], row[0], row[2], row[3], row[4], row[5])
        self.parentItem = item(row[6],row[7],row[8],row[9],row[10])
        self.childItem = item(row[11], row[12], row[13], row[14], row[15])