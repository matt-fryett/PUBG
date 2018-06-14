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



if convertMatchesToSql:
    for file in random.sample(files,len(files)):
        telePro = telemetryParser(path,matchPath,file)


#conn = sqlite3.connect("./matches.db")
#cursor = conn.cursor()
#cursor.execute("SELECT matchId FROM matchInfo WHERE gameMode = 'solo-fpp' AND mapName = 'Erangel_Main'")

match = "61340f80-c08a-46f1-b82e-56727d4bc3c6"


from carePackageLand import *
from carePackageSpawn import *
from gameStateManager import *
from playerManager import *

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

#exit()

for s in scrapeList:
    teleCursor.execute("SELECT * FROM "+s)
    for row in teleCursor.fetchall():
        obj = scrapeList[s](row)
        events.append(obj)
        if "account" in obj.accountId:
            if obj.accountId not in players:
                players[obj.accountId] = playerManager(obj.accountId)
            players[obj.accountId].add(obj)

from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data

fig = plt.figure()
ax = fig.add_subplot(111)#, projection='3d')
#fn = get_sample_data("C:/Users/matth/Documents/Projects/git/PUBG/map2.png", asfileobj=False)

#print(fn)
#arr = read_png(fn)
#plt.imshow(img, zorder=0, extent=[0, 800000.0, 0, 800000.0])
#ax.set_zscale("log",nonposz="clip")
#ax.set_zlim([-1000,5000])

minT = 999999999999999999
maxT = 0

#for angle in range(0,360):
#print(len(events))
for p in players:
    players[p].buildTimeline()
    minT = min(minT,players[p].minTime)
    maxT = max(maxT,players[p].maxTime)

exit()

ts = np.linspace(minT,maxT,1000)
angle = 0
c =0

lastXmin = 0
lastXmax = 816000
lastYmin = 0
lastYmax = 816000

for t in ts:
    #print(c)
    angle+=1
    c+=1
    angle=angle%360

    x = gameStateManager.safe(t)
    xmin = x[0]-x[3]
    xmax = x[0]+x[3]
    ymin = x[1]-x[3]
    ymax = x[1]+x[3]

    if np.isnan(xmin) or xmin < 0:
        xmin = 0
    if np.isnan(xmax) or xmax > 816000:
        xmax = 816000
    if np.isnan(ymin) or ymin < 0:
        ymin = 0
    if np.isnan(ymax) or ymax > 816000:
        ymax = 816000

    print(c,xmin,xmax,ymin,ymax)
    if xmin > lastXmin: lastXmin = xmin
    if xmax < lastXmax: lastXmax = xmax
    if ymin > lastYmin: lastYmin = ymin
    if ymax < lastYmax: lastYmax = ymax
    print(c,lastXmin,lastXmax,lastYmin,lastYmax)
    ax.set_xlim([lastXmin, lastXmax])
    ax.set_ylim([lastYmax, lastYmin])
    #ax.set_xlim([0, 800000])
    #ax.set_ylim([800000, 0])
    #ax.set_zlim([-1000, 200000])
    #print(gameStateManager.safe(t))
    safe = plt.Circle((gameStateManager.safe(t)[0], gameStateManager.safe(t)[1]), gameStateManager.safe(t)[3], color='b', alpha=0.2)
    poison = plt.Circle((gameStateManager.poison(t)[0], gameStateManager.poison(t)[1]), gameStateManager.poison(t)[3], color='k', alpha=0.2)
    red = plt.Circle((gameStateManager.red(t)[0], gameStateManager.red(t)[1]), gameStateManager.red(t)[3],color='r', alpha=0.2)

    #print(circle)
    ax.add_artist(safe)
    ax.add_artist(poison)
    ax.add_artist(red)
    for p in players:
        w = players[p].loc(t)
        ax.scatter(w[0], w[1])
    #ax.view_init(90*(t-minT)/(maxT-minT), angle)
    plt.savefig("./3dplot2/" + str(c) + ".png")
    plt.cla()

#print(ts)

    #
    #     t,h,x,y,z,= players[p].getDiscreteCoords()
    #     ax.plot(x,y,z)
    # ax.view_init(30,angle)
    # plt.savefig("./3dplot/"+str(angle)+".png")
    # plt.cla()
    # #print(p,players[p])
    #
