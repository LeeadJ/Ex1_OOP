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
        self.labor_time = self.closetime + self.opentime + self.starttime + self.stoptime  # initialize the labor time
        self.finish_timestamp = 0.0  # {3} The end-time will be initialized to 0.
        self.total_floors = (abs(self.minFloor) + abs(self.maxFloor) + 1)
        self.floor_timestamp_dict = {index: x for index, x in enumerate([0.0] * self.total_floors, start=self.minFloor)}

    '''This function adds a call to the elevator call list. It also updates the "Call amount" and "time-Adjuster.'''

    def addCall(self, call):
        self.callList.append(call)
        self.callAmount = len(self.callList)
        self.added_call_time_Adjuster(call)

    '''This function calculates the absolute time to finish a call(given an elevator and call).'''

    def src2dest_time(self, curr_call):
        # start_time = curr_call.timeStamp
        total_floors = abs(curr_call.destFloor - curr_call.originFloor)
        total_time = (total_floors * self.speed) + self.labor_time
        return total_time

    '''This function calculates the absolute time from the created call until the destination.'''

    def call2dest_time(self, curr_call):
        pass

    '''This function adjusts the time-stamp dictionary according to the call.'''

    def added_call_time_Adjuster(self, added_call):
        call_src = added_call.originFloor
        call_dest = added_call.destFloor
        stop_time = self.stoptime + self.opentime + self.speed
        floors = abs(call_dest - call_src)
        start_time = self.starttime + self.closetime + self.speed
        self.floor_timestamp_dict[call_src] = added_call.timeStamp
        if added_call.is_Up_call:  # UP call
            self.floor_timestamp_dict[call_src + 1] = self.floor_timestamp_dict[call_src] + start_time
            if floors == 1:
                self.floor_timestamp_dict[call_src + 1] += (stop_time - self.speed)
            elif floors > 3:
                for i in range(call_src + 2, call_dest):
                    self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i - 1] + self.speed
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest - 1] + stop_time
            else:
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest - 1] + stop_time
            if call_dest != self.maxFloor:
                self.add_default_time(call_dest, call_src)
        else:  # DOWN call
            self.floor_timestamp_dict[call_src - 1] = self.floor_timestamp_dict[call_src] + start_time
            if floors == 1:
                self.floor_timestamp_dict[call_src - 1] += (stop_time - self.speed)
            elif floors > 3:
                for i in range(call_src - 2, call_dest, -1):
                    self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i + 1] + self.speed
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest + 1] + stop_time
            else:
                self.floor_timestamp_dict[call_dest] = self.floor_timestamp_dict[call_dest + 1] + stop_time
            if call_dest != self.minFloor:
                self.add_default_time(call_dest, call_src)

    '''This function adjust the elevator time after the call reached its destination, until it reaches the maximum or
     minimum floor. '''

    def add_default_time(self, call_dest, call_src):
        stop_time = self.stoptime + self.opentime + self.speed
        start_time = self.starttime + self.closetime + self.speed
        if call_dest >= call_src:  # elevator going UP
            self.floor_timestamp_dict[call_dest + 1] = self.floor_timestamp_dict[call_dest] + start_time
            for i in range(call_dest + 2, self.maxFloor):
                self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i - 1] + self.speed
            self.floor_timestamp_dict[self.maxFloor] = self.floor_timestamp_dict[self.maxFloor - 1] + stop_time
        else:  # elevator going DOWN
            self.floor_timestamp_dict[call_dest - 1] = self.floor_timestamp_dict[call_dest] + start_time
            for i in range(call_dest - 2, self.minFloor):
                self.floor_timestamp_dict[i] = self.floor_timestamp_dict[i + 1] + self.speed
            self.floor_timestamp_dict[self.minFloor] = self.floor_timestamp_dict[self.minFloor + 1] + stop_time

    def addCall2(self, call):
        stop_time = self.stoptime + self.opentime
        if not self.callList:  # call is a FIRST call
            self.added_call_time_Adjuster(call)
            self.callList.append(call)
            self.callAmount += 1
        else:
            if self.is_in_Range(call):  # The call is in sup range
                self.callList.append(call)
                self.callAmount += 1
                self.floor_timestamp_dict[call.originFloor] += stop_time
                call.timeStamp = self.floor_timestamp_dict[call.originFloor] + stop_time
                self.added_call_time_Adjuster(call)

    def is_in_Range(self, call):
        stop_time = self.stoptime + self.opentime
        return call.timeStamp <= self.floor_timestamp_dict[call.originFloor] + stop_time + self.closetime

        # def is_in_range(self, call_list, call_src, status):

    #     if status == 1:
    #         call_up = df_up(call_list)
    #         for(i in range(1, len(call_up))):

    # Need to adjust the call timestamp as the starting point.
    # total_time = self.src2dest_time(added_call)
    # total_floors = abs(added_call.destFloor - added_call.originFloor)
    # time_to_add = total_time / total_floors
    # counter = 1
    # if added_call.is_Up_call():  # call going UP
    #     self.floor_timestamp_dict[added_call.originFloor] = added_call.timeStamp
    #     for i in range(added_call.originFloor + 1, added_call.destFloor + 1):
    #         self.floor_timestamp_dict[i] = added_call.timeStamp + (time_to_add * counter)
    #         counter += 1
    #     self.default_time_adjuster(added_call)
    #     self.finish_timestamp = self.floor_timestamp_dict[self.maxFloor]
    # else:  # call going DOWN
    #     self.floor_timestamp_dict[added_call.originFloor] = added_call.timeStamp
    #     for i in range(added_call.originFloor - 1, added_call.destFloor - 1, -1):
    #         self.floor_timestamp_dict[i] = (time_to_add * counter) + added_call.timeStamp
    #         counter += 1
    #     self.default_time_adjuster(added_call)
    #     self.finish_timestamp = self.floor_timestamp_dict[self.minFloor]

    '''This function adjust the elevator time after the call reached its destination, until it reaches the maximum 
    floor. '''

    # def default_time_adjuster(self, added_call):
    #     counter = 1
    #     if added_call.is_Up_call():  # going UP
    #         floors = self.maxFloor - added_call.destFloor
    #         if floors == 0:
    #             time_to_add = 0
    #         else:
    #             time_to_add = ((floors * self.speed) + self.labor_time) / floors
    #         for i in range(added_call.destFloor + 1, self.maxFloor + 1):
    #             self.floor_timestamp_dict[i] = self.floor_timestamp_dict[added_call.destFloor] + (time_to_add * counter)
    #             counter += 1
    #     else:  # going DOWN
    #         floors = self.maxFloor - self.minFloor
    #         if floors == 0:
    #             time_to_add = 0
    #         else:
    #             time_to_add = ((floors * self.speed) + self.labor_time) / floors
    #         for i in range(added_call.destFloor - 1, self.minFloor - 1, -1):
    #             self.floor_timestamp_dict[i] = self.floor_timestamp_dict[added_call.destFloor] + (time_to_add * counter)
    #             counter += 1

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
                                                [c.__str__() for c in self.callList], self.callAmount,
                                                self.finish_timestamp)

# //////////////////////////////////////////////////////////////////////////
