from item import *

class carePackage:
    def __init__(self,row):
        items = []
        for i in row[5][2:-2].split("}, {"):
            id = {}
            for x in [x.strip().split(":") for x in i.split(",")]:
                id[x[0]] = x[1].strip()
            items.append(item(id["itemId"], id["stackCount"], id["category"], id["subCategory"], id["attachedItems"]))