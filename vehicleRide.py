from gameEvent import *
from vehicle import *

class vehicleRide(gameEvent):
    def __init__(self,row):
        gameEvent.__init__(self, row[1], row[0], row[2], row[3], row[4], row[5])
        self.vehicle = vehicle(row[6], row[7], row[8], row[9])