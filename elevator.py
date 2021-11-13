from Call import *

'''
This is the Elevator class:
    1. The __init__ receives information from the Building class and initializes an elevator:
        - Elevator ID (index in the elevator-list)
        - Elevator Speed
        - Minimum floor of the elevator.
        - Maximum floor of the elevator.
        - Door closing time.
        - Door opening time.
        - Start time (time until the elevator reaches full speed).
        - Stop time (time until elevator reaches a complete stop)
    2. The __init__ also contains a Call-List. 
        - The call list will hold the upcoming calls the elevator need to attend to.
        - Every index represents a call.
        - Each calls will be in ascending order, according to their timestamps. *****************
    3. The __init__ also contains an Finish-Time.
        - The Finish-time will update itself according to the last call in the call-list.
        - The algorithm will know to choose an elevator according the their Finish-timestamp.
'''


class elevator:
    def __init__(self, id, speed, minFloor, maxFloor, closetime, opentime, starttime, stoptime):
        self.id = int(id)
        self.speed = float(speed)
        self.minFloor = int(minFloor)
        self.maxFloor = int(maxFloor)
        self.closetime = float(closetime)
        self.opentime = float(opentime)
        self.starttime = float(starttime)
        self.stoptime = float(stoptime)
        #########################################################################
        self.callList = []  # {2}Here we can add the calls appointed to the elevator
        self.callAmount = 0
        self.finish_timestamp = 0.0  # {3} The end-time will be initialized to 0.

    # {2}Function for adding calls (type=Call) to the call-list.
    def addCall(self, call, call_time):
        self.callList.append(call)
        self.callAmount = len(self.callList)
        self.finish_timestamp += call_time

    # This function will print all the information needed of the elevator:
    def __str__(self):
        return "Elevator Id: {}\nSpeed Time: {}\nMinimum Floor: {}\nMaximum Floor: {}\nClose Time: {}\n" \
               "Open Time: {}\nStart Time: {}\nStop Time: {}\nCall List: {}\nNumber of Calls: {}\n" \
               "Current Finish Time: {}".format(self.id, self.speed, self.minFloor, self.maxFloor, self.closetime,
                                                self.opentime, self.starttime, self.stoptime,
                                                [c.__str__() for c in self.callList], self.callAmount,
                                                self.finish_timestamp)

# //////////////////////////////////////////////////////////////////////////
