from gameState import *
import numpy as np
from scipy.interpolate import interp1d

class gameStateManager:
    def __init__(self,row):
        self.gameStates = []
        self.safe = None
        for r in row:
            self.gameStates.append(gameState(r))

    def buildTimeline(self):
        self.gameStates.sort(key=lambda x: x.time)
        self.minTime = self.gameStates[0].tidx
        self.maxTime = self.gameStates[-1].tidx

        self.safeX = np.array([x.safeX for x in self.gameStates])
        self.safeY = np.array([x.safeY for x in self.gameStates])
        self.safeZ = np.array([x.safeZ for x in self.gameStates])
        self.safeR = np.array([x.safeR for x in self.gameStates])
        self.safeX[self.safeX < 1] = np.nan
        self.safeY[self.safeY < 1] = np.nan
        self.safeZ[self.safeZ < 1] = np.nan
        self.safeR[self.safeR < 1] = np.nan
        self.t = np.array([x.tidx for x in self.gameStates])
        self.safe = interp1d(self.t, np.array([self.safeX, self.safeY, self.safeZ, self.safeR]), bounds_error=False, fill_value=np.nan)

        self.poisonX = np.array([x.poisonX for x in self.gameStates])
        self.poisonY = np.array([x.poisonY for x in self.gameStates])
        self.poisonZ = np.array([x.poisonZ for x in self.gameStates])
        self.poisonR = np.array([x.poisonR for x in self.gameStates])
        self.poisonX[self.poisonX < 1] = np.nan
        self.poisonY[self.poisonY < 1] = np.nan
        self.poisonZ[self.poisonZ < 1] = np.nan
        self.poisonR[self.poisonR < 1] = np.nan
        self.t = np.array([x.tidx for x in self.gameStates])
        self.poison = interp1d(self.t, np.array([self.poisonX, self.poisonY, self.poisonZ, self.poisonR]), bounds_error=False, fill_value=np.nan)

        self.redX = np.array([x.redX for x in self.gameStates])
        self.redY = np.array([x.redY for x in self.gameStates])
        self.redZ = np.array([x.redZ for x in self.gameStates])
        self.redR = np.array([x.redR for x in self.gameStates])
        self.redX[self.redX < 1] = np.nan
        self.redY[self.redY < 1] = np.nan
        self.redZ[self.redZ < 1] = np.nan
        self.redR[self.redR < 1] = np.nan
        self.t = np.array([x.tidx for x in self.gameStates])
        self.red = interp1d(self.t, np.array([self.redX, self.redY, self.redZ, self.redR]), bounds_error=False, fill_value=np.nan)



