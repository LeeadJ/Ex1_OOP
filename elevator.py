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
    3. The __init__ also contains a Finish-Time.
        - The Finish-time will update itself according to the last call in the call-list.
        - The algorithm will know to choose an elevator according the their Finish-timestamp.
    4. The __init__ also contains a Floor Timestamp dictionary (key='floor number'(int) : value='timestamp(float)).
        - This dictionary allows us to see what the timestamp of the elevator at each floor.
        - This will help us determine if to add a call to the elevator call list.
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
        total_floors = (abs(self.minFloor) + abs(self.maxFloor) + 1)
        self.floor_timestamp_dict = {index: x for index, x in enumerate([0.0] * total_floors, start=self.minFloor)}

    # {2}Function for adding calls (type=Call) to the call-list.
    def addCall(self, call):
        self.callList.append(call)
        self.callAmount = len(self.callList)
        self.adjustTime(call)

    '''This function calculates the absolute time to finish a call(given an elevator and call).'''
    def call_time(self, curr_call):
        start_time = curr_call.timeStamp
        labor_time = self.closetime + self.opentime + self.starttime + self.stoptime
        total_floors = abs(curr_call.destFloor - curr_call.originFloor)
        total_time = (total_floors * self.speed) + labor_time
        return total_time

    '''This function adjusts the time-stamp dictionary according to the call.'''
    def adjustTime(self, added_call):
        # Need to adjust the call timestamp as the starting point.
        total_time = self.call_time(added_call)
        total_floors = abs(added_call.destFloor - added_call.originFloor)
        time_to_add = total_time/total_floors
        counter = 1
        if added_call.originFloor < added_call.destFloor:  # going UP
            self.floor_timestamp_dict[added_call.originFloor] = added_call.timeStamp
            for i in range(added_call.originFloor+1, added_call.destFloor+1):
                self.floor_timestamp_dict[i] = added_call.timeStamp + (time_to_add * counter)
                counter += 1
            for j in range(added_call.destFloor+1, self.maxFloor+1):
                self.floor_timestamp_dict[j] = self.floor_timestamp_dict[added_call.destFloor]
            self.finish_timestamp = self.floor_timestamp_dict[self.maxFloor]
        else:  # going DOWN
            self.floor_timestamp_dict[added_call.originFloor] = added_call.timeStamp
            for i in range(added_call.originFloor-1, added_call.destFloor-1, -1):
                self.floor_timestamp_dict[i] = (time_to_add*counter) + added_call.timeStamp
                counter += 1
            for j in range(added_call.destFloor-1, self.minFloor-1, -1):
                self.floor_timestamp_dict[j] = self.floor_timestamp_dict[added_call.destFloor]
            self.finish_timestamp = self.floor_timestamp_dict[self.minFloor]

    '''This function returns the given floor time-stamp.'''
    def get_floorTimestamp(self, floor):
        try:
            return self.floor_timestamp_dict[floor]
        except KeyError:
            print("The floor_timestamp_dict['index'] is OUT-OF-BOUNDS ")

    '''This function checks if a given call is relevant.'''
    def is_call_relevant(self, call):
        origin_timeStamp = call.timeStamp
        floor_elevator_timestamp = self.get_floorTimestamp(call.originFloor)
        return origin_timeStamp <= floor_elevator_timestamp
    '''This function prints the elevator information.'''
    def __str__(self):
        return "Elevator Id: {}\nSpeed Time: {}\nMinimum Floor: {}\nMaximum Floor: {}\nClose Time: {}\n" \
               "Open Time: {}\nStart Time: {}\nStop Time: {}\nCall List: {}\nNumber of Calls: {}\n" \
               "Current Finish Time: {}".format(self.id, self.speed, self.minFloor, self.maxFloor, self.closetime,
                                                self.opentime, self.starttime, self.stoptime,
                                                [c.__str__() for c in self.callList], self.callAmount,
                                                self.finish_timestamp)

# //////////////////////////////////////////////////////////////////////////
