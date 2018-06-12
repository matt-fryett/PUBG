from datetime import datetime
import calendar

class gameState:
    def __init__(self,row):
        self.time = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.tidx = self.toTimestamp(self.time)+self.time.microsecond/1000000
        self.gameTime = row[1]
        self.safeX = row[2]
        self.safeY = row[3]
        self.safeZ = row[4]
        self.safeR = row[5]
        self.poisonX = row[6]
        self.poisonY = row[7]
        self.poisonZ = row[8]
        self.poisonR = row[9]
        self.redX = row[10]
        self.redY = row[11]
        self.redZ = row[12]
        self.redR = row[13]

    def toTimestamp(self,d):
        return calendar.timegm(d.timetuple())