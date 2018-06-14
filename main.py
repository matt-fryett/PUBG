from os import listdir
from os.path import isfile, join
import json
from scipy.interpolate import RegularGridInterpolator
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib import cm, patches
import matplotlib.cbook as cbook
from scipy.misc import imread
from mpl_toolkits.mplot3d import Axes3D
import random
import sqlite3
from telemetryParser import *

# convertMatchesToSql=False

# if convertMatchesToSql:
#     for file in random.sample(files,len(files)):
#         telePro = telemetryParser(path,matchPath,file)


#conn = sqlite3.connect("./matches.db")
#cursor = conn.cursor()
#cursor.execute("SELECT matchId FROM matchInfo WHERE gameMode = 'solo-fpp' AND mapName = 'Erangel_Main'")







from carePackageLand import *
from carePackageSpawn import *
from gameStateManager import *
from playerManager import *

match = "61340f80-c08a-46f1-b82e-56727d4bc3c6"
teleConn = sqlite3.connect("./"+match+".db")
teleCursor = teleConn.cursor()

scrapeList = {}
scrapeList["armorDestroy"] = armorDestroy
scrapeList["carePackageLand"] = carePackageLand
scrapeList["carePackageSpawn"] = carePackageSpawn
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

events = []
players = {}
teleCursor.execute("SELECT * FROM gameStatePeriodic")

gameStateManager = gameStateManager(teleCursor.fetchall())

gameStateManager.buildTimeline()


for s in scrapeList:
    teleCursor.execute("SELECT * FROM "+s)
    for row in teleCursor.fetchall():
        obj = scrapeList[s](row)
        events.append(obj)
        if "account" in obj.accountId:
            if obj.accountId not in players:
                players[obj.accountId] = playerManager(obj.accountId)
            players[obj.accountId].add(obj)

absMin = 9999999999999999
#for p in players:
#    players[p].getMainProperties()


for p in players:
    players[p].buildTimeline()
    absMin = min(absMin, players[p].gameStart)

for p in players:
    players[p].gameStart = absMin
    players[p].postProcessing()

