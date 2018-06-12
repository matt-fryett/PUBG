from gameEvent import *
from carePackage import *

class carePackageLand(gameEvent):
    def __init__(self,row):
        gameEvent.__init__(self, row[0], row[1]+"_"+row[0], 0, row[2], row[3], row[4])
        carePackage.__init__(self,row)
