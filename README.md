Algorithm:
1. First we get a Call csv.
2. We loop through the call, and run by each call.
3. Check if the call is UP or DOWN. Deppending on which state we run through the csv and check which calls are relevant according
   to the timeStamp and state. (Id the elevator is now in the same direction as the call or the call timestamp is greater than
   the elevator floor timestamp - the call is irelevant.)
4. When finishing the loop, every call's elevator index that is different from -1, gets moved to an outputfile.
5. When finishing all the calls, we will sort the output file according to the timestamp.

Classes:
1) Building:
   - Class Building receives a JSON file and extracts the key values given:
   1.1) __init__() :
        - Minimum Floor.
        - Maximum Floor.
        - elevator list.
            - Each index contains an elevator(imported from class - elevator).
        - Number of elevators.
   1.2) __str__():
        - Prints the Building information.
        
2) elevator():
    - The elevator class receives information from the building and creates an elevator object.
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
   2.6) adjust_not_empty_dict(self, add_call):
            - This function adjust the elevator dictionary timestamp that is not empty. Meaning it has been previously given calls. 
   2.7) get_floorTimestamp(self, floor):
            - This function returns the given floor time-stamp.
   2.8) is_elevator_UP(self):
            - This function returns the direction of a current elevator.
   2.7)  __str__(self):
            - Prints the information of the elevator.

3) Call:  
    - The Call class receives a row from the call.csv and transforms it into an object called Call.
   3.1) __init__() :
        - stam_str - A string containing the syntax 'Elevator Call'.
        - Timestamp - The call timestamp.
        - Origin Floor - The floor the call was made.
        - Destination Floor - The destination of the floor.
        - Status - The direction of the call. (UP of DOWN)
        - Elevator Index - The index of the elevator taking the call (initialized as 0)
    3.2) __str__() :
        - Prints the information of the Call.

4) Ex1:
    - This is the main class. The Class holds functions that help create the final DataFrame.
   Functions:
   4.1) Ex1(Building_json, call_csv):
        - This function receives a building json file and call csv file.
        - It returns an output csv file with the determined elevator index for each call.
    4.2) allocate_elev(elevator_list, output, call_file): 
        - This function receives an elevator list, an output file, and the original call csv file.
        - It calculates the best elevator for the current call and updates the output file.
    4.3) calc_time(elev):
        - This function receives an elevator and calculates the average waiting time for the calls in the elevator call list.
    4.4) wipe(elev, str):
        - This function receives and elevator and a string. 
        - If the given string is "best" then the function clears the elevator call list and updates the timestamp dictionary.
        - If the given string is not "best", the function just clears the call list and resets the call amount to zero.
    4.5) update_call_file(call_file, call):
        - This function receives the original call file and a call and drops the call from the call file. It is done 
           after the call has been taken care of.
    4.6) send_to_output(curr_elev, output):
        - This function receives an elevator and the output csv file and adds the call to the output file.
    4.7) addIndex(curr_elev):
        - This function changes the elevator index of the current call to the best elevator given.
    4.8) elev_df(curr_elev):
        - This function receives the current best elevator and creates a dataframe from its call list. 
    4.9) make_df(file):
        - This function receives the call csv file and transforms it to a dataframe.
    4.10)  make_up(dataframe):
        - This function receives a dataframe and returns a new dataframe with only UP calls.
    4.11) make_down(dataframe):
        - This function receives a dataframe and returns a new dataframe with only DOWN calls.
    4.12) make_output(dataframe, df_name: str = None):
        - This function receives a dataframe and a string name and returns an output csv file in the name of the given string.
    4.13) main():
        - This is the main function.
        - Here the program runs Ex1 and returns the final output csv file.
