import numpy as np
import matplotlib.pyplot as plt

class plotters:
    def __init__(self):
        None

    def plotWholeMatch(self,players,gameStateManager):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        minT = 999999999999999999
        maxT = 0
        for p in players:
            minT = min(minT,players[p].minTime)
            maxT = max(maxT,players[p].maxTime)

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
