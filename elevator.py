from Call import *

'''
This is the Elevator class:
    1. The _init_ receives information from the Building class and initializes an elevator:
        - Elevator ID (index in the elevator-list)
        - Elevator Speed
        - Minimum floor of the elevator.
        - Maximum floor of the elevator.
        - Door closing time.
        - Door opening time.
        - Start time (time until the elevator reaches full speed).
        - Stop time (time until elevator reaches a complete stop)
    2. The _init_ also contains a Call-List. 
        - The call list will hold the upcoming calls the elevator need to attend to.
        - Every index represents a call.
        - Each calls will be in ascending order, according to their timestamps. *******
    3. The _init_ also contains a Finish-Time.
        - The Finish-time will update itself according to the last call in the call-list.
        - The algorithm will know to choose an elevator according the their Finish-timestamp.
    4. The _init_ also contains a Floor Timestamp dictionary (key='floor number'(int) : value='timestamp(float)).
        - This dictionary allows us to see what the timestamp of the elevator at each floor.
        - This will help us determine if to add a call to the elevator call list.
'''


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
        self.callList = []  # {2}Here we can add the calls appointed to the elevator
        self.callAmount = 0
        self.labor_time = self.closetime + self.opentime + self.starttime + self.stoptime  # initialize the labor time
        self.finish_timestamp = 0.0  # {3} The end-time will be initialized to 0.
        self.total_floors = (abs(self.minFloor) + abs(self.maxFloor) + 1)
        self.floor_timestamp_dict = {index: x for index, x in enumerate([0.0] * self.total_floors, start=self.minFloor)}

    '''This function adds a call to the elevator call list. It also updates the "Call amount" and "time-Adjuster.'''

    def is_in_Range(self, call):
        if self.callList[len(self.callList) - 1].originFloor == call.originFloor:
            stop_time = self.opentime + self.closetime
            return call.timeStamp <= self.floor_timestamp_dict[call.originFloor] + stop_time
        else:
            stop_time = self.stoptime + self.opentime + self.closetime
            return call.timeStamp <= self.floor_timestamp_dict[call.originFloor] + stop_time


    def addCall(self, call):
        if len(self.callList) == 0: # If the list is empty
            empty = True
            for i in range(self.minFloor, self.maxFloor + 1):
                if self.floor_timestamp_dict[i] != 0.0:
                    empty = False
            if empty:  # call is a FIRST call and dict is empty
                self.added_call_time_Adjuster(call, call.timeStamp)
                self.callList.append(call)
                self.callAmount += 1
            else: # dict isn't empty
                self.adjust_not_empty_dict(call)
        else:
            if self.is_in_Range(call):  # The call is in sup range
                self.callList.append(call)
                self.callAmount += 1
                timeStamp = call.timeStamp + self.closetime
                self.added_call_time_Adjuster(call, timeStamp)


    ''' function that adjust the dict after it got a future dict from allocate in Ex1'''

    def adjust_not_empty_dict(self, add_call):
        call_timeStamp = add_call.timeStamp
        dict_timeStamp = self.floor_timestamp_dict[add_call.originFloor]
        if call_timeStamp <= dict_timeStamp:
            self.callList.append(add_call)
            self.callAmount += 1
            #add_call.timeStamp = dict_timeStamp #FUCK YOU ARYEH, If you change the add call, it changes the original abject. NEED to make a COPY
            self.added_call_time_Adjuster(add_call, dict_timeStamp)
        else:
            self.added_call_time_Adjuster(add_call, add_call.timeStamp)
            self.callList.append(add_call)
            self.callAmount += 1


    '''This function adjusts the time-stamp dictionary according to the call.'''

    def added_call_time_Adjuster(self, added_call, timeStamp): # Added the timeStamp to adjust by
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
                self.floor_timestamp_dict[call_dest-1] = self.floor_timestamp_dict[call_dest-2] + self.speed
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

    '''This function adjust the elevator time after the call reached its destination, until it reaches the maximum or
     minimum floor. '''

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

    '''This function adjust the elevator time after the call reached its destination, until it reaches the maximum 
    floor. '''

    '''This function returns the given floor time-stamp.'''

    def get_floorTimestamp(self, floor):
        try:
            return self.floor_timestamp_dict[floor]
        except KeyError:
            print("The floor_timestamp_dict['index'] is OUT-OF-BOUNDS ")

    '''This function checks if a given call is relevant.'''

    def is_elevator_UP(self):
        return self.floor_timestamp_dict[self.maxFloor] > self.floor_timestamp_dict[self.maxFloor - 1]

    def is_call_relevant(self, call):
        if self.floor_timestamp_dict[self.maxFloor] == 0.0:  # This is the first call
            return True
        if (call.is_Up_call() and self.is_elevator_UP()) or (
                not call.is_Up_call() and not self.is_elevator_UP()):  # If same direction
            print(self.floor_timestamp_dict)
            return call.timeStamp <= self.floor_timestamp_dict[call.originFloor]
        else:  # The call and elevator are different directions:
            self.adjust_time_for_new_direction(call)
            print(self.floor_timestamp_dict)
            return call.timeStamp <= self.floor_timestamp_dict[call.originFloor]

    '''This function check is to change the elevator timestamp to DOWN'''

    def adjust_time_for_new_direction(self, call):  ###########Fix#############################################
        curr_max_floor_timestamp = self.floor_timestamp_dict[self.maxFloor]
        curr_min_floor_timestamp = self.floor_timestamp_dict[self.minFloor]
        floors = (self.maxFloor - self.minFloor) + 1
        time_to_add = ((floors * self.speed) + self.labor_time) / floors
        counter = 1
        if call.timeStamp >= curr_max_floor_timestamp:  # Adjust going Down
            for i in range(self.maxFloor - 1, self.minFloor - 1, -1):
                self.floor_timestamp_dict[i] = self.floor_timestamp_dict[self.maxFloor] + (time_to_add * counter)
                counter += 1
        if (call.timeStamp >= curr_min_floor_timestamp) and counter == 1:  # Adjust going UP
            for i in range(self.minFloor + 1, self.maxFloor + 1):
                self.floor_timestamp_dict[i] = self.floor_timestamp_dict[self.minFloor] + (time_to_add * counter)
                counter += 1

    '''This function prints the elevator information.'''

    def __str__(self):
        return "Elevator Id: {}\nSpeed Time: {}\nMinimum Floor: {}\nMaximum Floor: {}\nClose Time: {}\n" \
               "Open Time: {}\nStart Time: {}\nStop Time: {}\nCall List: {}\nNumber of Calls: {}\n" \
               "Current Finish Time: {}".format(self.id, self.speed, self.minFloor, self.maxFloor, self.closetime,
                                                self.opentime, self.starttime, self.stoptime,
                                                [c._str_() for c in self.callList], self.callAmount,
                                                self.finish_timestamp)

# //////////////////////////////////////////////////////////////////////////