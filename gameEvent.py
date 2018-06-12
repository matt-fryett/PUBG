from datetime import datetime
import calendar

class gameEvent:
    def __init__(self,t,accountId,h,x,y,z):
        self.time = datetime.strptime(t,"%Y-%m-%dT%H:%M:%S.%fZ")
        self.tidx = self.toTimestamp(self.time)+self.time.microsecond/1000000
        self.accountId = accountId
        self.health = h
        self.x = x
        self.y = y
        self.z = z

    def toTimestamp(self,d):
        return calendar.timegm(d.timetuple())