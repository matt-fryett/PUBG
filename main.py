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

class player():
    def __init__(self,character):
        self.name = character["name"]
        self.id = character["accountId"]
        self.team = character["teamId"]
        self.health = character["health"]
        self.t = [character["time"]]
        self.x = [(character["location"]["x"])]
        self.y = [(816000.0-character["location"]["y"])]
        self.z = [(character["location"]["z"])]
        self.timeline = interp1d(np.array([-2,-1]),np.array([np.array([0,1]),np.array([0,1])]), bounds_error=False, fill_value=np.nan)

    def add(self,character):
        self.t.append(character["time"])
        self.x.append(character["location"]["x"])
        self.y.append(816000.0 - character["location"]["y"])
        self.z.append(character["location"]["z"])

    def setTimeline(self):
        if len(self.t)>1:
            self.timeline = interp1d(np.array(self.t), np.array([np.array(self.x),np.array(self.y)]), bounds_error=False, fill_value=np.nan)

class telemetryProcessor():
    def __init__(self,teleInfo):
        self.players = {}
        self.matchTime = None
        for k in teleInfo:
            if {"MatchId", "PingQuality","_V","_D","_T"} == set(t.keys()):
                self.matchTime = k["_D"]
            if {"character", "common", "_V", "_D", "_T"} == set(t.keys()):
                None
            if {"character", "elapsedTime","numAlivePlayers","common","_V","_D","_T"} == set(k.keys()):
                print(k)
                char = k["character"]
                char["time"] = k["elapsedTime"]
                if char["time"] > 0:
                    if char["name"] not in self.players:
                        # print(char["name"])
                        self.players[char["name"]] = player(char)
                    else:
                        self.players[char["name"]].add(char)

        for p in self.players.values():
            p.setTimeline()
        self.planePath = []
        #self.matchTime = teleInfo["MatchId"]["PingQuality"]["_D"]

    def getPlaneTrajectory(self,plot=False):
        xs = []
        ys = []
        for p in self.players.values():
            xs.append(p.x[0])
            ys.append(p.y[0])

        grads = (np.roll(np.array(ys),1)-np.array(ys))/(np.roll(np.array(xs),1)-np.array(xs))
        inters = -grads*xs+ys
        mask = ~np.isnan(grads)
        m = np.median(grads[mask])
        c = np.median(inters[mask])

        if m>1:
            y = np.linspace(0, 816000, 10000)
            x = (y-c)/m
        else:
            x = np.linspace(0, 816000, 10000)
            y = m * x + c
        return x,y


    def plotTimeLine(self,totalFrames):
        maxTime = 0
        funcs = []
        for p in self.players:
            coords = np.array([self.players[p].x, self.players[p].y])
            time = np.array(self.players[p].t)
            if max(time) > maxTime:
                maxTime = max(time)
            funcs.append(interp1d(time, coords, bounds_error=False, fill_value=np.nan))

        # exit()
        timeSeries = list(np.linspace(0, maxTime, 10))
        for t in timeSeries:
            fig, ax = plt.subplots()
            ax.set_xlim(0, 816000)
            ax.set_ylim(0, 816000)
            for f in funcs:
                x = f(t)[0]
                y = f(t)[1]
                ax.plot(x, y, "o", linewidth=0.5, markersize=1)

            img = imread(cbook.get_sample_data("C:/Users/matth/Documents/Projects/git/PUBG/map2.jpg"))
            plt.imshow(img, zorder=0, extent=[0, 816000.0, 0, 816000.0])
            plt.savefig("./plots/" + str(timeSeries.index(t)) + ".png", dpi=200)
            plt.clf()
            plt.close()



#816000.0


        #self.loc[character["time"]] = [character["location"]["x"],816000.0-character["location"]["y"],character["location"]["z"]]

#path = "../PUBG/telemetry/"
#files = [f for f in listdir(path) if isfile(join(path, f))]

# fig, ax = plt.subplots()
# ax.set_xlim(0, 816000)
# ax.set_ylim(0, 816000)

traj_x = np.array([])
traj_y = np.array([])
hist = np.histogram2d(traj_x, traj_y, bins=(100, 100))[0]
c=0

def getPlanePath(tele):
    x,y = tele.getPlaneTrajectory()
    return np.histogram2d(x, y, bins=(100, 100),range=[[0,816000],[0,816000]])[0]

def plotPlanePath(hist):
    fig, ax = plt.subplots()
    ax.set_xlim(0, 816000)
    ax.set_ylim(0, 816000)
    plt.imshow(hist, extent=[0, 816000, 0, 816000])
    plt.savefig("./plane_heat.png", dpi=200)
    with open("plane_heat.csv","w") as f:
        for row in hist:
            f.write(",".join([str(x) for x in list(row)])+"\n")
    #hist.tofile("plane_heat.csv")


doPlanePaths = False

convertMatchesToSql = False

matchPath = "../PUBG/matches/"

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
