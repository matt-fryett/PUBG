import sqlite3
import json

class telemetryParser:
    def __init__(self,path,matchPath,file):
        print("Processing", file)
        self.path = path
        self.matchPath = matchPath
        self.file = file
        self.conn = sqlite3.connect("matches.db")
        self.cursor = self.conn.cursor()
        self.hasMatchFile = True
        self.matchInfo = None

        self.pFuncs = {}
        self.pFuncs2 = {}
        self.pFuncs2["LogPlayerLogin"] = self.parseLogPlayerLogin
        self.pFuncs["LogPlayerCreate"] = self.parseLogPlayerCreate
        self.pFuncs["LogPlayerPosition"] = self.parseLogPlayerPosition
        self.pFuncs["LogPlayerAttack"] = self.parseLogPlayerAttack
        self.pFuncs2["LogPlayerLogout"] = self.parseLogPlayerLogout
        self.pFuncs["LogVehicleRide"] = self.parseLogVehicleRide
        self.pFuncs["LogItemEquip"] = self.parseLogItemEquip
        self.pFuncs["LogItemUnequip"] = self.parseLogItemUnequip
        self.pFuncs["LogItemPickup"] = self.parseLogItemPickup
        self.pFuncs["LogItemDrop"] = self.parseLogItemDrop
        self.pFuncs["LogMatchStart"] = self.parseLogMatchStart
        self.pFuncs["LogGameStatePeriodic"] = self.parseLogGameStatePeriodic
        self.pFuncs["LogItemAttach"] = self.parseLogItemAttach
        self.pFuncs["LogItemDetach"] = self.parseLogItemDetach
        self.pFuncs["LogItemUse"] = self.parseLogItemUse
        self.pFuncs["LogPlayerTakeDamage"] = self.parseLogPlayerTakeDamage
        self.pFuncs["LogPlayerKill"] = self.parseLogPlayerKill
        self.pFuncs["LogCarePackageSpawn"] = self.parseLogCarePackageSpawn
        self.pFuncs["LogVehicleDestroy"] = self.parseLogVehicleDestroy
        self.pFuncs["LogVehicleLeave"] = self.parseLogVehicleLeave
        self.pFuncs["LogSwimStart"] = self.parseLogSwimStart
        self.pFuncs["LogSwimEnd"] = self.parseLogSwimEnd
        self.pFuncs["LogMatchEnd"] = self.parseLogMatchEnd
        self.pFuncs["LogMatchDefinition"] = self.nullFunc
        self.pFuncs["LogArmorDestroy"] = self.parseLogArmorDestroy
        self.pFuncs["LogCarePackageLand"] = self.parseLogCarePackageLand

        self.dbPath = "./telemetry/"
        with open(self.path + self.file) as json_data:
            self.teleInfo = json.load(json_data)
        try:
            with open(matchPath + "-".join(file.split("-")[:5])+".json") as match_data:
                self.matchInfo = json.load(match_data)
                self.addMatch()
        except Exception as ex:
            self.hasMatchFile = False
        try:
            self.teleConn = sqlite3.connect(self.dbPath + self.matchInfo["data"]["id"] + ".db")
            self.teleCursor = self.teleConn.cursor()
            self.createTables()
            self.parseToSql()


            self.teleConn.commit()
            self.teleConn.close()
        except:
            pass
        self.conn.commit()

    def nullFunc(self,t,_t):
        pass

    def parseLogPlayerLogin(self,t,_t):
        #print("UPDATE players SET loginTime = '" + t["_D"] + "' WHERE accountId = '" + t["accountId"] + "'")
        self.teleCursor.execute("UPDATE players SET loginTime = '" + t["_D"] + "' WHERE accountId = '" + t["accountId"] + "'")
        if self.hasMatchFile:
            self.cursor.execute("UPDATE playerInfo SET loginTime = '" + t["_D"] + "' WHERE matchId = '" + self.matchInfo["data"]["id"] + "' AND playerId = '" + t["accountId"] + "'")

    def parseLogPlayerCreate(self,t,_t):
        self.sqlInsert(self.cursor, "teamInfo", {"accountId": t["character"]["accountId"], "teamId": t["character"]["teamId"]})
        self.sqlInsert(self.teleCursor, "players", {"accountId": t["character"]["accountId"], "teamId": t["character"]["teamId"]})
        queryString = "UPDATE players SET " + \
                      "initX = '" + str(t["character"]["location"]["x"]) + "', " + \
                      "initY = '" + str(t["character"]["location"]["y"]) + "', " + \
                      "initZ = '" + str(t["character"]["location"]["z"]) + "', " + \
                      "ranking = '" + str(t["character"]["ranking"]) + "' " + \
                      "WHERE accountId = '" + t["character"]["accountId"] + "'"
        self.teleCursor.execute(queryString)
        if self.hasMatchFile:
            queryString = "UPDATE playerInfo SET " + \
                          "initX = '" + str(t["character"]["location"]["x"]) + "', " + \
                          "initY = '" + str(t["character"]["location"]["y"]) + "', " + \
                          "initZ = '" + str(t["character"]["location"]["z"]) + "', " + \
                          "ranking = '" + str(t["character"]["ranking"]) + "' " + \
                          "WHERE matchId = '" + self.matchInfo["data"]["id"] + "' AND playerId = '" + t["character"][
                              "accountId"] + "'"
            self.cursor.execute(queryString)

    def parseLogPlayerPosition(self,t,_t):
        positionInfo = {}
        positionInfo["accountId"] = t["character"]["accountId"]
        positionInfo["time"] = t["_D"]
        positionInfo["elapsedTime"] = t["elapsedTime"]
        positionInfo["health"] = t["character"]["health"]
        positionInfo["x"] = t["character"]["location"]["x"]
        positionInfo["y"] = t["character"]["location"]["y"]
        positionInfo["z"] = t["character"]["location"]["z"]
        self.sqlInsert(self.teleCursor, _t, positionInfo)

    def parseLogPlayerAttack(self,t,_t):
        attackInfo = {}
        attackInfo["attackId"] = t["attackId"]
        attackInfo["time"] = t["_D"]
        attackInfo["accountId"] = t["attacker"]["accountId"]
        attackInfo["health"] = t["attacker"]["health"]
        attackInfo["x"] = t["attacker"]["location"]["x"]
        attackInfo["y"] = t["attacker"]["location"]["y"]
        attackInfo["z"] = t["attacker"]["location"]["z"]
        attackInfo["attackType"] = t["attackType"]
        attackInfo["itemId"] = t["weapon"]["itemId"]
        attackInfo["stackCount"] = t["weapon"]["stackCount"]
        attackInfo["category"] = t["weapon"]["category"]
        attackInfo["subCategory"] = t["weapon"]["subCategory"]
        attackInfo["attachedItems"] = t["weapon"]["attachedItems"]
        attackInfo["vehicleType"] = t["vehicle"]["vehicleType"]
        attackInfo["vehicleId"] = t["vehicle"]["vehicleId"]
        attackInfo["healthPercent"] = t["vehicle"]["healthPercent"]
        attackInfo["fuelPercent"] = t["vehicle"]["feulPercent"]
        self.sqlInsert(self.teleCursor, _t, attackInfo)

    def parseLogArmorDestroy(self,t,_t):
        armorDestoryInfo = {}
        armorDestoryInfo["attackId"] = t["attackId"]
        armorDestoryInfo["time"] = t["_D"]
        armorDestoryInfo["attackerAccountId"] = t["attacker"]["accountId"]
        armorDestoryInfo["attackerHealth"] = t["attacker"]["health"]
        armorDestoryInfo["attackerX"] = t["attacker"]["location"]["x"]
        armorDestoryInfo["attackerY"] = t["attacker"]["location"]["y"]
        armorDestoryInfo["attackerZ"] = t["attacker"]["location"]["z"]
        armorDestoryInfo["victimAccountId"] = t["victim"]["accountId"]
        armorDestoryInfo["victimHealth"] = t["victim"]["health"]
        armorDestoryInfo["victimX"] = t["victim"]["location"]["x"]
        armorDestoryInfo["victimY"] = t["victim"]["location"]["y"]
        armorDestoryInfo["victimZ"] = t["victim"]["location"]["z"]
        armorDestoryInfo["damageTypeCategory"] = t["damageTypeCategory"]
        armorDestoryInfo["damageReason"] = t["damageReason"]
        armorDestoryInfo["damageCauserName"] = t["damageCauserName"]
        armorDestoryInfo["itemId"] = t["item"]["itemId"]
        armorDestoryInfo["stackCount"] = t["item"]["stackCount"]
        armorDestoryInfo["category"] = t["item"]["category"]
        armorDestoryInfo["subCategory"] = t["item"]["subCategory"]
        armorDestoryInfo["attachedItems"] = t["item"]["attachedItems"]
        armorDestoryInfo["distance"] = t["distance"]
        self.sqlInsert(self.teleCursor, _t, armorDestoryInfo)

    def parseLogPlayerLogout(self,t,_t):
        self.teleCursor.execute("UPDATE players SET logoutTime = '" + t["_D"] + "' WHERE accountId = '" + t["accountId"] + "'")
        if self.hasMatchFile:
            self.cursor.execute("UPDATE playerInfo SET logoutTime = '" + t["_D"] + "' WHERE matchId = '" + self.matchInfo["data"][
                "id"] + "' AND playerId = '" + t["accountId"] + "'")

    def parseLogVehicleRide(self,t,_t):
        vehicleRideInfo = {}
        vehicleRideInfo["accountId"] = t["character"]["accountId"]
        vehicleRideInfo["time"] = t["_D"]
        vehicleRideInfo["health"] = t["character"]["health"]
        vehicleRideInfo["x"] = t["character"]["location"]["x"]
        vehicleRideInfo["y"] = t["character"]["location"]["y"]
        vehicleRideInfo["z"] = t["character"]["location"]["z"]
        vehicleRideInfo["vehicleType"] = t["vehicle"]["vehicleType"]
        vehicleRideInfo["vehicleId"] = t["vehicle"]["vehicleId"]
        vehicleRideInfo["healthPercent"] = t["vehicle"]["healthPercent"]
        vehicleRideInfo["fuelPercent"] = t["vehicle"]["feulPercent"]
        self.sqlInsert(self.teleCursor, _t, vehicleRideInfo)

    def parseLogVehicleLeave(self,t,_t):
        vehicleLeaveInfo = {}
        vehicleLeaveInfo["accountId"] = t["character"]["accountId"]
        vehicleLeaveInfo["time"] = t["_D"]
        vehicleLeaveInfo["health"] = t["character"]["health"]
        vehicleLeaveInfo["x"] = t["character"]["location"]["x"]
        vehicleLeaveInfo["y"] = t["character"]["location"]["y"]
        vehicleLeaveInfo["z"] = t["character"]["location"]["z"]
        vehicleLeaveInfo["vehicleType"] = t["vehicle"]["vehicleType"]
        vehicleLeaveInfo["vehicleId"] = t["vehicle"]["vehicleId"]
        vehicleLeaveInfo["healthPercent"] = t["vehicle"]["healthPercent"]
        vehicleLeaveInfo["fuelPercent"] = t["vehicle"]["feulPercent"]
        self.sqlInsert(self.teleCursor, _t, vehicleLeaveInfo)

    def parseLogItemEquip(self,t,_t):
        itemEquip = {}
        itemEquip["accountId"] = t["character"]["accountId"]
        itemEquip["time"] = t["_D"]
        itemEquip["health"] = t["character"]["health"]
        itemEquip["x"] = t["character"]["location"]["x"]
        itemEquip["y"] = t["character"]["location"]["y"]
        itemEquip["z"] = t["character"]["location"]["z"]
        itemEquip["itemId"] = t["item"]["itemId"]
        itemEquip["stackCount"] = t["item"]["stackCount"]
        itemEquip["category"] = t["item"]["category"]
        itemEquip["subCategory"] = t["item"]["subCategory"]
        itemEquip["attachedItems"] = t["item"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemEquip)

    def parseLogItemUnequip(self, t,_t):
        itemUnequip = {}
        itemUnequip["accountId"] = t["character"]["accountId"]
        itemUnequip["time"] = t["_D"]
        itemUnequip["health"] = t["character"]["health"]
        itemUnequip["x"] = t["character"]["location"]["x"]
        itemUnequip["y"] = t["character"]["location"]["y"]
        itemUnequip["z"] = t["character"]["location"]["z"]
        itemUnequip["itemId"] = t["item"]["itemId"]
        itemUnequip["stackCount"] = t["item"]["stackCount"]
        itemUnequip["category"] = t["item"]["category"]
        itemUnequip["subCategory"] = t["item"]["subCategory"]
        itemUnequip["attachedItems"] = t["item"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemUnequip)

    def parseLogItemPickup(self,t,_t):
        itemPickup = {}
        itemPickup["accountId"] = t["character"]["accountId"]
        itemPickup["time"] = t["_D"]
        itemPickup["health"] = t["character"]["health"]
        itemPickup["x"] = t["character"]["location"]["x"]
        itemPickup["y"] = t["character"]["location"]["y"]
        itemPickup["z"] = t["character"]["location"]["z"]
        itemPickup["itemId"] = t["item"]["itemId"]
        itemPickup["stackCount"] = t["item"]["stackCount"]
        itemPickup["category"] = t["item"]["category"]
        itemPickup["subCategory"] = t["item"]["subCategory"]
        itemPickup["attachedItems"] = t["item"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemPickup)

    def parseLogItemDrop(self,t,_t):
        itemDrop = {}
        itemDrop["accountId"] = t["character"]["accountId"]
        itemDrop["time"] = t["_D"]
        itemDrop["health"] = t["character"]["health"]
        itemDrop["x"] = t["character"]["location"]["x"]
        itemDrop["y"] = t["character"]["location"]["y"]
        itemDrop["z"] = t["character"]["location"]["z"]
        itemDrop["itemId"] = t["item"]["itemId"]
        itemDrop["stackCount"] = t["item"]["stackCount"]
        itemDrop["category"] = t["item"]["category"]
        itemDrop["subCategory"] = t["item"]["subCategory"]
        itemDrop["attachedItems"] = t["item"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemDrop)

    def parseLogMatchStart(self,t,_t):
        if self.hasMatchFile:
            self.cursor.execute("UPDATE matchInfo SET startedAt = '" + t["_D"] + "' WHERE matchId = '" + self.matchInfo["data"]["id"] + "'")

    def parseLogGameStatePeriodic(self,t,_t):
        gameInfo = {}
        gameInfo["time"] = t["_D"]
        gameInfo["elapsedTime"] = t["gameState"]["elapsedTime"]
        gameInfo["safeX"] = t["gameState"]["safetyZonePosition"]["x"]
        gameInfo["safeY"] = t["gameState"]["safetyZonePosition"]["y"]
        gameInfo["safeZ"] = t["gameState"]["safetyZonePosition"]["z"]
        gameInfo["safeRadius"] = t["gameState"]["safetyZoneRadius"]
        gameInfo["poisonX"] = t["gameState"]["poisonGasWarningPosition"]["x"]
        gameInfo["poisonY"] = t["gameState"]["poisonGasWarningPosition"]["y"]
        gameInfo["poisonZ"] = t["gameState"]["poisonGasWarningPosition"]["z"]
        gameInfo["poisonRadius"] = t["gameState"]["poisonGasWarningRadius"]
        gameInfo["redX"] = t["gameState"]["redZonePosition"]["x"]
        gameInfo["redY"] = t["gameState"]["redZonePosition"]["y"]
        gameInfo["redZ"] = t["gameState"]["redZonePosition"]["z"]
        gameInfo["redRadius"] = t["gameState"]["redZoneRadius"]
        self.sqlInsert(self.teleCursor, _t, gameInfo)

    def parseLogItemAttach(self,t,_t):
        itemAttachInfo = {}
        itemAttachInfo["accountId"] = t["character"]["accountId"]
        itemAttachInfo["time"] = t["_D"]
        itemAttachInfo["health"] = t["character"]["health"]
        itemAttachInfo["x"] = t["character"]["location"]["x"]
        itemAttachInfo["y"] = t["character"]["location"]["y"]
        itemAttachInfo["z"] = t["character"]["location"]["z"]
        itemAttachInfo["parentItemId"] = t["parentItem"]["itemId"]
        itemAttachInfo["parentStackCount"] = t["parentItem"]["stackCount"]
        itemAttachInfo["parentCategory"] = t["parentItem"]["category"]
        itemAttachInfo["parentSubCategory"] = t["parentItem"]["subCategory"]
        itemAttachInfo["parentAttachedItems"] = t["parentItem"]["attachedItems"]
        itemAttachInfo["childItemId"] = t["childItem"]["itemId"]
        itemAttachInfo["childStackCount"] = t["childItem"]["stackCount"]
        itemAttachInfo["childCategory"] = t["childItem"]["category"]
        itemAttachInfo["childSubCategory"] = t["childItem"]["subCategory"]
        itemAttachInfo["childAttachedItems"] = t["childItem"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemAttachInfo)

    def parseLogItemDetach(self, t,_t):
        itemDetachInfo = {}
        itemDetachInfo["accountId"] = t["character"]["accountId"]
        itemDetachInfo["time"] = t["_D"]
        itemDetachInfo["health"] = t["character"]["health"]
        itemDetachInfo["x"] = t["character"]["location"]["x"]
        itemDetachInfo["y"] = t["character"]["location"]["y"]
        itemDetachInfo["z"] = t["character"]["location"]["z"]
        itemDetachInfo["parentItemId"] = t["parentItem"]["itemId"]
        itemDetachInfo["parentStackCount"] = t["parentItem"]["stackCount"]
        itemDetachInfo["parentCategory"] = t["parentItem"]["category"]
        itemDetachInfo["parentSubCategory"] = t["parentItem"]["subCategory"]
        itemDetachInfo["parentAttachedItems"] = t["parentItem"]["attachedItems"]
        itemDetachInfo["childItemId"] = t["childItem"]["itemId"]
        itemDetachInfo["childStackCount"] = t["childItem"]["stackCount"]
        itemDetachInfo["childCategory"] = t["childItem"]["category"]
        itemDetachInfo["childSubCategory"] = t["childItem"]["subCategory"]
        itemDetachInfo["childAttachedItems"] = t["childItem"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemDetachInfo)

    def parseLogItemUse(self,t,_t):
        itemUse = {}
        itemUse["accountId"] = t["character"]["accountId"]
        itemUse["time"] = t["_D"]
        itemUse["health"] = t["character"]["health"]
        itemUse["x"] = t["character"]["location"]["x"]
        itemUse["y"] = t["character"]["location"]["y"]
        itemUse["z"] = t["character"]["location"]["z"]
        itemUse["itemId"] = t["item"]["itemId"]
        itemUse["stackCount"] = t["item"]["stackCount"]
        itemUse["category"] = t["item"]["category"]
        itemUse["subCategory"] = t["item"]["subCategory"]
        itemUse["attachedItems"] = t["item"]["attachedItems"]
        self.sqlInsert(self.teleCursor, _t, itemUse)

    def parseLogPlayerTakeDamage(self,t,_t):
        damageInfo = {}
        damageInfo["attackId"] = t["attackId"]
        damageInfo["time"] = t["_D"]
        damageInfo["attackerAccountId"] = t["attacker"]["accountId"]
        damageInfo["attackerHealth"] = t["attacker"]["health"]
        damageInfo["attackerX"] = t["attacker"]["location"]["x"]
        damageInfo["attackerY"] = t["attacker"]["location"]["y"]
        damageInfo["attackerZ"] = t["attacker"]["location"]["z"]
        damageInfo["victimAccountId"] = t["victim"]["accountId"]
        damageInfo["victimHealth"] = t["victim"]["health"]
        damageInfo["victimX"] = t["victim"]["location"]["x"]
        damageInfo["victimY"] = t["victim"]["location"]["y"]
        damageInfo["victimZ"] = t["victim"]["location"]["z"]
        damageInfo["damageTypeCategory"] = t["damageTypeCategory"]
        damageInfo["damageReason"] = t["damageReason"]
        damageInfo["damage"] = t["damage"]
        damageInfo["damageCauserName"] = t["damageCauserName"]
        self.sqlInsert(self.teleCursor, _t, damageInfo)

    def parseLogPlayerKill(self,t,_t):
        killInfo = {}
        killInfo["attackId"] = t["attackId"]
        killInfo["time"] = t["_D"]
        killInfo["killerAccountId"] = t["killer"]["accountId"]
        killInfo["killerHealth"] = t["killer"]["health"]
        killInfo["killerX"] = t["killer"]["location"]["x"]
        killInfo["killerY"] = t["killer"]["location"]["y"]
        killInfo["killerZ"] = t["killer"]["location"]["z"]
        killInfo["victimAccountId"] = t["victim"]["accountId"]
        killInfo["victimHealth"] = t["victim"]["health"]
        killInfo["victimX"] = t["victim"]["location"]["x"]
        killInfo["victimY"] = t["victim"]["location"]["y"]
        killInfo["victimZ"] = t["victim"]["location"]["z"]
        killInfo["damageTypeCategory"] = t["damageTypeCategory"]
        killInfo["damageCauserName"] = t["damageCauserName"]
        killInfo["distance"] = t["distance"]
        self.sqlInsert(self.teleCursor, _t, killInfo)

    def parseLogCarePackageSpawn(self,t,_t):
        crateSpawnInfo = {}
        crateSpawnInfo["time"] = t["_D"]
        crateSpawnInfo["itemPackageId"] = t["itemPackage"]["itemPackageId"]
        crateSpawnInfo["x"] = t["itemPackage"]["location"]["x"]
        crateSpawnInfo["y"] = t["itemPackage"]["location"]["y"]
        crateSpawnInfo["z"] = t["itemPackage"]["location"]["z"]
        crateSpawnInfo["items"] = t["itemPackage"]["items"]
        self.sqlInsert(self.teleCursor, _t, crateSpawnInfo)

    def parseLogCarePackageLand(self,t,_t):
        crateLandInfo = {}
        crateLandInfo["time"] = t["_D"]
        crateLandInfo["itemPackageId"] = t["itemPackage"]["itemPackageId"]
        crateLandInfo["x"] = t["itemPackage"]["location"]["x"]
        crateLandInfo["y"] = t["itemPackage"]["location"]["y"]
        crateLandInfo["z"] = t["itemPackage"]["location"]["z"]
        crateLandInfo["items"] = t["itemPackage"]["items"]
        self.sqlInsert(self.teleCursor, _t, crateLandInfo)

    def parseLogVehicleDestroy(self,t,_t):
        vehicleDestroyInfo = {}
        vehicleDestroyInfo["attackId"] = t["attackId"]
        vehicleDestroyInfo["time"] = t["_D"]
        vehicleDestroyInfo["attackerAccountId"] = t["attacker"]["accountId"]
        vehicleDestroyInfo["attackerHealth"] = t["attacker"]["health"]
        vehicleDestroyInfo["attackerX"] = t["attacker"]["location"]["x"]
        vehicleDestroyInfo["attackerY"] = t["attacker"]["location"]["y"]
        vehicleDestroyInfo["attackerZ"] = t["attacker"]["location"]["z"]
        vehicleDestroyInfo["vehicleType"] = t["vehicle"]["vehicleType"]
        vehicleDestroyInfo["vehicleId"] = t["vehicle"]["vehicleId"]
        vehicleDestroyInfo["healthPercent"] = t["vehicle"]["healthPercent"]
        vehicleDestroyInfo["fuelPercent"] = t["vehicle"]["feulPercent"]
        vehicleDestroyInfo["damageTypeCategory"] = t["damageTypeCategory"]
        vehicleDestroyInfo["damageCauserName"] = t["damageCauserName"]
        vehicleDestroyInfo["distance"] = t["distance"]
        self.sqlInsert(self.teleCursor, _t, vehicleDestroyInfo)

    def parseLogSwimStart(self,t,_t):
        swimStart = {}
        swimStart["accountId"] = t["character"]["accountId"]
        swimStart["time"] = t["_D"]
        swimStart["health"] = t["character"]["health"]
        swimStart["x"] = t["character"]["location"]["x"]
        swimStart["y"] = t["character"]["location"]["y"]
        swimStart["z"] = t["character"]["location"]["z"]
        self.sqlInsert(self.teleCursor, _t, swimStart)

    def parseLogSwimEnd(self,t,_t):
        swimEnd = {}
        swimEnd["accountId"] = t["character"]["accountId"]
        swimEnd["time"] = t["_D"]
        swimEnd["health"] = t["character"]["health"]
        swimEnd["x"] = t["character"]["location"]["x"]
        swimEnd["y"] = t["character"]["location"]["y"]
        swimEnd["z"] = t["character"]["location"]["z"]
        self.sqlInsert(self.teleCursor, _t, swimEnd)

    def parseLogMatchEnd(self,t,_t):
        if self.hasMatchFile:
            self.cursor.execute("UPDATE matchInfo SET endedAt = '" + t["_D"] + "' WHERE matchId = '" + self.matchInfo["data"]["id"] + "'")

    def parseToSql(self):
        fMissing = open("missing.txt","w")
        for t in self.teleInfo:
            if t["_T"] in self.pFuncs:
                s = t["_T"][3:]
                self.pFuncs[t["_T"]](t,s[0].lower()+s[1:])
            else:
                fMissing.write(t["_T"][3:]+"\n")
        for t in self.teleInfo:
            if t["_T"] in self.pFuncs2:
                s = t["_T"][3:]
                self.pFuncs2[t["_T"]](t,s[0].lower()+s[1:])
        fMissing.close()



    def createTables(self):
        from os import listdir
        from os.path import isfile, join
        files = [f for f in listdir("./tables/") if isfile(join("./tables/", f))]
        for f in files:
            with open("./tables/" + f) as qFile:
                self.teleCursor.execute(qFile.read())

    def addMatch(self):
        self.matchToSql(self.matchInfo)
        for p in self.matchInfo["included"]:
            if p["type"] == "participant":
                p["attributes"]["stats"]["matchId"] = self.matchInfo["data"]["id"]
                self.sqlInsert(self.cursor, "playerInfo", p["attributes"]["stats"])
        self.conn.commit()

    def sqlInsert(self,cursor, table, dict):
        try:
            queryString = "INSERT INTO " + table + " (" + ",".join(
                [str(x).replace("'", "") for x in dict.keys()]) + ") VALUES (" + ",".join(
                ["'" + str(x).replace("'", "") + "'" for x in dict.values()]) + ")"
            cursor.execute(queryString)
        except Exception as ex:
            print(queryString)
            print(table, ex)
            pass

    def matchToSql(self,matchInfo):
        matchSummary = {}
        matchSummary["matchId"] = matchInfo["data"]["id"]
        matchSummary["type"] = matchInfo["data"]["type"]
        matchSummary["duration"] = matchInfo["data"]["attributes"]["duration"]
        matchSummary["gameMode"] = matchInfo["data"]["attributes"]["gameMode"]
        matchSummary["shardId"] = matchInfo["data"]["attributes"]["shardId"]
        matchSummary["mapName"] = matchInfo["data"]["attributes"]["mapName"]
        matchSummary["createdAt"] = matchInfo["data"]["attributes"]["createdAt"]
        self.sqlInsert(self.cursor, "matchInfo", matchSummary)

    def __del__(self):
        self.conn.close()