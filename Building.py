import json
from elevator import *


class Building:
    def __init__(self, j_file):
        with open(j_file, 'r') as json_file:
            json_load = json.load(json_file)
            self.minFloor = json_load['_minFloor']
            self.maxFloor = json_load['_maxFloor']
            elevatorArr = []
            for e in json_load["_elevators"]:
                newE = elevator(e["_id"], e["_speed"], e["_minFloor"], e["_maxFloor"], e["_closeTime"], e["_openTime"],
                                e["_startTime"], e["_stopTime"])
                elevatorArr.append(newE)
            self.ElevatorArray = elevatorArr
        json_file.close()


file = r"C:\Users\Leead\Desktop\B5.json"
b = Building(file)

for e in b.ElevatorArray:
    print(e.__str__())

