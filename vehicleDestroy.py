from gameEvent import *
from damage import *
from vehicle import *

class vehicleDestroy(gameEvent):
    def __init__(self,row):
        self.id = row[0]
        gameEvent.__init__(self,row[1], row[2],row[3],row[4],row[5],row[6])
        self.vehicle = vehicle(row[7], row[8], row[9], row[10])
        self.damage = damage(row[11],"Destroyed",0,row[12])
        self.distance = row[13]