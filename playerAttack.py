from gameEvent import *
from item import *
from vehicle import *

class playerAttack(gameEvent):
    def __init__(self,row):
        self.id = row[0]
        self.attackType = row[7]
        gameEvent.__init__(self,row[1],row[2],row[3],row[4],row[5],row[6])
        self.item = item(row[8],row[9],row[10],row[11],row[12])
        self.vehicle = vehicle(row[13],row[14],row[15],row[16])