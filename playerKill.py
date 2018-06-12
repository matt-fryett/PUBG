from gameEvent import *
from item import *
from damage import *
from player import *

class playerKill(gameEvent):
    def __init__(self,row):
        self.id = row[0]
        gameEvent.__init__(self,row[1],row[2],row[3],row[4],row[5],row[6])
        self.attacker = player(row[2],row[3],row[4],row[5],row[6])
        self.victim = player(row[7],row[8],row[9],row[10],row[11])
        self.damage = damage(row[12],"PlayerKill",0,row[13])
        #self.item = item(row[15],row[16],row[17],row[18],row[19])
        self.distance = row[14]