'''
The elevator class receives information from the building and creates an elevator object.
   2.1) __init__() :  receives information from the Building class and initializes an elevator:
            - Elevator ID (index in the elevator-list)
            - Elevator Speed
            - Minimum floor of the elevator.
            - Maximum floor of the elevator.
            - Door closing time.
            - Door opening time.
            - Start time (time until the elevator reaches full speed).
            - Stop time (time until elevator reaches a complete stop)
                        Added parameters to the init:
            - CallList - each elevator contains a list of calls that it will take.
            - Call Amount - the amount of calls currently in the call list.
            - Labor Time - the elevators of maintenance time (close,open,start,and stop times).
            - Finish Timestamp - The time the elevator will reach the minimum or maximum floor according to the direction.
            - Total Floors - total floors the elevator can reach.
            - TIMESTAMP DICTIONARY - This is a dictionary. Each key is a floor of the building and each key value holds the time
                                     the elevator will reach the floor. This is the most important parameter of the elevator.
                                     It allows the algorithm determine which elevator to call.
            Functions:
   2.2) addCall(self, call):
            - This function adds a call to the elevator call list. It also updates the "Call amount" and "time-Adjuster.
   2.3) added_call_time_Adjuster(self, added_call):
            - This function adjusts the time-stamp dictionary according to the call.
   2.4) is_in_Range(self, call):
            - This function, given a call, checks if the call is relevant to the elevator at the src floor.
   2.5) add_default_time(self, call_dest, call_src):
            - This function adjust the elevator time from the floor above the call destination until the maximum floor of the building,
              or from the floor under the call until the minimum of the building, according to the direction of the call.
   2.6)  __str__(self):
            - Prints the information of the elevator.
'''
from Call import*

class elevator:
    def __init__(self, id, speed, minFloor, maxFloor, closetime, opentime, starttime, stoptime):
        self.id = int(id)
        self.speed = 1 / float(speed)
        self.minFloor = int(minFloor)
        self.maxFloor = int(maxFloor)
        self.closetime = float(closetime)
        self.opentime = float(opentime)
        self.starttime = float(starttime)
        self.stoptime = float(stoptime)
        #########################################################################
        self.callList = []
        self.callAmount = 0
        self.labor_time = self.closetime + self.opentime + self.starttime + self.stoptime
        self.finish_timestamp = 0.0
        self.total_floors = (abs(self.minFloor) + abs(self.maxFloor) + 1)
        self.floor_timestamp_dict = {index: x for index, x in enumerate([0.0] * self.total_floors, start=self.minFloor)}

    '''This function adds a call to the elevator call list. It also updates the "Call amount" and "time-Adjuster.'''

    def addCall(self, call):
        if len(self.callList) == 0:  # If the list is empty
            empty = True
            for i in range(self.minFloor, self.maxFloor + 1):
                if self.floor_timestamp_dict[i] != 0.0:
                    empty = False
            if empty:  # call is a FIRST call and dict is empty
                self.added_call_time_Adjuster(call, call.timeStamp)
                self.callList.append(call)
                self.callAmount += 1
            else:  # dict isn't empty
                self.adjust_not_empty_dict(call)
        else:
            if self.is_in_Range(call):  # The call is in sup range
                self.callList.append(call)
                self.callAmount += 1
                timeStamp = call.timeStamp + self.closetime
                self.added_call_time_Adjuster(call, timeStamp)

    """This function, given a call, checks if the call is relevant to the elevator at the src floor."""

    def is_in_Range(self, call):
        if self.callList[len(self.callList) - 1].originFloor == call.originFloor:
            stop_time = self.opentime + self.closetime
            return call.timeStamp <= self.floor_timestamp_dict[call.originFloor] + stop_time
        else:
            stop_time = self.stoptime + self.opentime + self.closetime
            return call.timeStamp <= self.floor_timestamp_dict[call.originFloor] + stop_time

    '''This function adjust the elevator dictionary timestamp that is not empty. Meaning it has been previously given calls.'''

    def adjust_not_empty_dict(self, add_call):
        call_timeStamp = add_call.timeStamp
        dict_timeStamp = self.floor_timestamp_dict[add_call.originFloor]
        if call_timeStamp <= dict_timeStamp:
            self.callList.append(add_call)
            self.callAmount += 1
            # add_call.timeStamp = dict_timeStamp #FUCK YOU ARYEH, If you change the add call, it changes the original abject. NEED to make a COPY
            self.added_call_time_Adjuster(add_call, dict_timeStamp)
        else:
            self.added_call_time_Adjuster(add_call, add_call.timeStamp)
            self.callList.append(add_call)
            self.callAmount += 1

    '''This function adjusts the time-stamp dictionary according to the call.'''

    def added_call_time_Adjuster(self, added_call, timeStamp):  # Added the timeStamp to adjust by
        call_src = added_call.originFloor
        call_dest = added_call.destFloor
        stop_time = self.stoptime + self.opentime + self.speed
        start_time = self.starttime + self.closetime + self.speed
        floors = abs(call_dest - call_src)
        self.floor_timestamp_dict[call_src] = timeStamp
        if added_call.status == 1:  # UP call
            self.floor_timestamp_dict[call_src + 1] = self.floor_timestamp_dict[call_src] + start_time
            if floors == 1:
                self.floor_timestamp_dict[call_src + 1] += (stop_time - self.speed)
            if floors == 2:
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest - 1] + stop_time
            if floors == 3:
                self.floor_timestamp_dict[call_dest - 1] = self.floor_timestamp_dict[call_dest - 2] + self.speed
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest - 1] + stop_time
            else:
                for i in range(call_src + 2, call_dest):
                    self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i - 1] + self.speed
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest - 1] + stop_time
            # update default
            if call_dest != self.maxFloor:
                self.add_default_time(added_call)
            self.finish_timestamp = self.floor_timestamp_dict[self.maxFloor]
        else:  # DOWN call
            self.floor_timestamp_dict[call_src - 1] = self.floor_timestamp_dict[call_src] + start_time
            if floors == 1:
                self.floor_timestamp_dict[call_src - 1] += (stop_time - self.speed)
            if floors == 2:
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest + 1] + stop_time
            if floors == 3:
                self.floor_timestamp_dict[call_dest + 1] = self.floor_timestamp_dict[call_dest + 2] + self.speed
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest - 1] + stop_time
            else:
                for i in range(call_src - 2, call_dest, -1):
                    self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i + 1] + self.speed
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest + 1] + stop_time
            # update default time
            if call_dest != self.minFloor:
                self.add_default_time(added_call)
            self.finish_timestamp = self.floor_timestamp_dict[self.minFloor]

    '''This function adjust the elevator time from the floor above the call destination until the maximum floor of the building,
              or from the floor under the call until the minimum of the building, according to the direction of the call. '''

    def add_default_time(self, added_call):
        stop_time = self.stoptime + self.opentime + self.speed
        start_time = self.starttime + self.closetime + self.speed
        if added_call.status == 1:  # elevator going UP
            self.floor_timestamp_dict[added_call.destFloor + 1] = self.floor_timestamp_dict[added_call.destFloor] + \
                                                                  start_time
            for i in range(added_call.destFloor + 2, self.maxFloor):
                self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i - 1] + self.speed
            self.floor_timestamp_dict[self.maxFloor] = self.floor_timestamp_dict[self.maxFloor - 1] + stop_time - \
                                                       self.opentime
        else:  # elevator going DOWN
            self.floor_timestamp_dict[added_call.destFloor - 1] = self.floor_timestamp_dict[added_call.destFloor] + \
                                                                  start_time
            for i in range(added_call.destFloor - 2, self.minFloor, -1):
                self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i + 1] + self.speed
            self.floor_timestamp_dict[self.minFloor] = self.floor_timestamp_dict[self.minFloor + 1] + stop_time - \
                                                       self.opentime

    '''This function returns the given floor time-stamp.'''

    def get_floorTimestamp(self, floor):
        try:
            return self.floor_timestamp_dict[floor]
        except KeyError:
            print("The floor_timestamp_dict['index'] is OUT-OF-BOUNDS ")

    '''This function returns the direction of a current elevator.'''

    def is_elevator_UP(self):
        return self.floor_timestamp_dict[self.maxFloor] > self.floor_timestamp_dict[self.maxFloor - 1]

    '''This function prints the elevator information.'''

    def __str__(self):
        return "Elevator Id: {}\nSpeed Time: {}\nMinimum Floor: {}\nMaximum Floor: {}\nClose Time: {}\n" \
               "Open Time: {}\nStart Time: {}\nStop Time: {}\nCall List: {}\nNumber of Calls: {}\n" \
               "Current Finish Time: {}".format(self.id, self.speed, self.minFloor, self.maxFloor, self.closetime,
                                                self.opentime, self.starttime, self.stoptime,
                                                [c._str_() for c in self.callList], self.callAmount,
                                                self.finish_timestamp)

# //////////////////////////////////////////////////////////////////////////
