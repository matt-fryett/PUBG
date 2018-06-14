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