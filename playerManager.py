import numpy as np
from scipy.interpolate import interp1d
import calendar
from armorDestroy import *
from swimEnd import *
from swimStart import *
from itemAttach import *
from itemDetach import *
from itemDrop import *
from itemEquip import *
from itemPickup import *
from itemUnequip import *
from playerAttack import *
from playerKill import *
from playerPosition import *
from playerTakeDamage import *
from swimStart import *
from swimEnd import *
from vehicleDestroy import *
from vehicleLeave import *
from vehicleRide import *
import os
import pandas as pd

class playerManager:
    def __init__(self,accountId):
        self.accountId = accountId
        self.events = []
        self.x = np.array([])
        self.y = np.array([])
        self.z = np.array([])
        self.t = np.array([])
        self.df = None
        self.loc = None
        self.swim = None
        self.minTime = None
        self.maxTime = None

    def add(self,obj):
        self.events.append(obj)
        #if isinstance(obj,swimStart) or isinstance(obj,swimEnd):
        #    print(obj)




    def buildTimeline(self):
        self.events.sort(key=lambda x: x.time)
        self.minTime = self.events[0].tidx
        self.maxTime = self.events[-1].tidx

        self.x = np.array([x.x for x in self.events])
        self.y = np.array([x.y for x in self.events])
        self.z = np.array([x.z for x in self.events])
        self.t = [x.tidx for x in self.events]
        i=0
        tHold = [self.t[0],0000]
        for i in range(1,len(self.t)):
            if self.t[i]==tHold[0]:
                tHold[1] += 0.0001
                self.t[i]+=tHold[1]
            else:
                tHold[0] = self.t[i]
                tHold[1] = 0.0000
        self.t = np.array(self.t)

        self.loc = interp1d(self.t, np.array([self.x, self.y, self.z]), bounds_error=False, fill_value=np.nan)

        dfData = {}
        dfData["x"] = self.x
        dfData["y"] = self.y
        dfData["z"] = self.z
        dfData["t"] = self.t

        scrapeList = {}
        scrapeList["armorDestroy"] = armorDestroy
        scrapeList["itemAttach"] = itemAttach
        scrapeList["itemDetach"] = itemDetach
        scrapeList["itemDrop"] = itemDrop
        scrapeList["itemEquip"] = itemEquip
        scrapeList["itemPickup"] = itemPickup
        scrapeList["itemUnequip"] = itemUnequip
        scrapeList["playerAttack"] = playerAttack
        scrapeList["playerKill"] = playerKill
        scrapeList["playerPosition"] = playerPosition
        scrapeList["playerTakeDamage"] = playerTakeDamage
        scrapeList["swimStart"] = swimStart
        scrapeList["swimEnd"] = swimEnd
        scrapeList["vehicleDestroy"] = vehicleDestroy
        scrapeList["vehicleLeave"] = vehicleLeave
        scrapeList["vehicleRide"] = vehicleRide
        for y in zip(scrapeList.keys(),scrapeList.values()):
            dfData[y[0]] = np.array([x if isinstance(x,y[1]) else np.nan for x in self.events])

        vfunc = np.vectorize(lambda x: np.nan if pd.isnull(x) else np.float(x.gameTime))
        dfData["elapsedTime"] = vfunc(dfData["playerPosition"])
        dfData["swim"] =  np.array([True if isinstance(x,swimStart) else False if isinstance(x,swimEnd) else np.nan for x in self.events])

        self.df = pd.DataFrame(data=dfData,index=self.t)
        self.df["swim"].fillna(method="ffill", inplace=True)
        self.df["swim"].fillna(value=0, inplace=True)
        directory = "./dataframes/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.df.to_csv(directory+str(self.accountId)+".csv")


    def getDiscreteCoords(self,**kwargs):
        t = np.array([x.time for x in self.events])
        h = np.array([x.health for x in self.events])
        x = np.array([x.x for x in self.events])
        y = np.array([x.y for x in self.events])
        z = np.array([x.z for x in self.events])
        if "noSky" in kwargs:
            f = z<2000
            t,h,x,y,z = t[f], h[f], x[f], y[f], z[f]

        return t,h,x,y,z