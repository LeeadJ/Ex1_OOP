'''
This is the Algorithm file.
- In the Algo method:
1) Get a building json file and create the building.
2) Get a Call csv.
    - Run through the csv.
    - Convert the csv int a list of call objects.
    - Run though the Call-object list, match the call to the best elevator(algorithm).
        - Maybe first sort the list according to what we want.
        - Creat a new list. Each index represents an elevator according to the building.
        - Each index will contain a list which we can add on calls.
        - Insert the index (which contains a list of calls) into the elevator Call-List.
    - Once best elevator is discovered, insert the call to the elevator Call-List.

'''
from Call import *
import json
import numpy as np
import csv



class Ex1:

    def __init__(self, building_jFile, call_csv, out_csv):
        self.building = building_jFile
        self.calls = call_csv
        self.out = out_csv


    def allocateCall(self, call_csv):
        pass

def openCalls( call_csv):
    callList = []
    with open(call_csv) as cs:
        df = csv.reader(cs)
        for row in df:
            callList.append(Call(row))
    return callList

def fromArrayToCsv(self, callsList):
    filename = 'output.csv'
    all = []
    for i in callsList:
        all.append(i._dict_.values())
    with open(filename, 'w', newline="") as file:
        csvWriter = csv.writer(file)
        csvWriter.writerows(all)

file = r"C:\Users\Leead\Desktop\calls\Calls_a.csv"
e = openCalls(file)
print(e[0].__str__())
fromArrayToCsv(e)


