import pandas as pd
from Building import *

'''This function receives a building json file and call csv file. It returns an output csv file with the determined 
elevator index for each call. '''


def Ex1(Building_json, call_csv):
    building_b = Building(Building_json)  # WORKS
    elev_list = building_b.ElevatorList  # WORKS
    call_file = make_df(call_csv)  # WORKS
    # call_file.to_csv("call_file", index=False)///////////////////////////////
    size = len(call_file)  # size = 100 # WORKS
    data = {'stam_str': [], 'timeStamp': [], 'src': [], 'dest': [], 'status': [], 'elevatorIndex': []}  # WORKS
    output = pd.DataFrame(data)  # print empty output with the correct columns # WORKS
    # output.to_csv("call_file", index=False)///////////////////////////
    count = 0
    while size != 0:  # ENDLESS LOOP NEED TO FIX
        # print("\t\tThe current DataFrame size is:",size)
        count += 1
        # print("\t\t\tIteration Number:",count)
        if building_b.elevatorAmount == 1:  # WORKS
            # print("\t\tElevator Amount = 1")
            # print("Create output with Elevator Index = 0")
            output = pd.concat([call_file, output], ignore_index=True)  # WORKS
            output = output.assign(elevatorIndex=0)  # WORKS
            # print(output)
            size = 0
        else:
            first_call = Call(call_file.iloc[[0]].values[0])  # WORKS
            # print("\nThe First Call:",first_call.__str__())
            # print("\n\t\tAdding the First Call to each Elevator\n")
            for i in elev_list:
                dict_before_first_call = i.floor_timestamp_dict.copy()
                i.addCall(first_call)
                # print("Adding First Call to elevator:", i.id)
                # print("Elevator call list:",[call.__str__() for call in i.callList])
            if first_call.status == 1:  # call is UP
                # print("\nThe First Call is an UP call from:",first_call.originFloor,"--->",first_call.destFloor,"\n")
                temp_df = make_up(call_file.loc[1:])
                # print("\nThis is the Make_UP_df:", "First Call origin floor=", first_call.originFloor, "MaxFloor=", building_b.maxFloor)
                # print(temp_df)
                for src in range(first_call.originFloor, building_b.maxFloor):
                    src_df = temp_df[temp_df['src'] == src]
                    # print("\nThis is the src_df:", "src=", src)
                    # print(src_df)
                    for e in elev_list:
                        # print("\n\t\tLooping through the Building Elevator LIST\n")
                        # print("Elevator ID:", e.id)
                        # print("First Call:",first_call.__str__())
                        # print("Dictionary Before FIRST Call:", dict_before_first_call)
                        # print("Dictionary After FIRST Call:", e.floor_timestamp_dict,"\n")
                        dict_Before_added_calls = e.floor_timestamp_dict.copy()
                        for j in range(1, len(src_df)):  # ///////////////////////////////////////
                            curr_call = Call(src_df.iloc[[j]].values[0])
                            if curr_call.timeStamp > e.floor_timestamp_dict[e.maxFloor]:
                                # print("\nTHE NEXT CALLS TIMESTAMPS ARE GREATER THAN THE MAX-FLOOR TIMESTAMP. THEY ARE IRELEVANT\n")
                                break
                            e.addCall(curr_call)
                            # print("Checking Call:", curr_call.__str__(), "to Elevator:", e.id)
                        # print("Current number of calls in Elevator",e.id,": ",e.callAmount)
                        # print("Added Calls:", [call.__str__() for call in e.callList])
                        # print("Dictionary BEFORE Added Calls:", dict_Before_added_calls)
                        # print("Dictionary AFTER Added Calls:", e.floor_timestamp_dict,"\n")
                output = allocate_elev(elev_list, output, call_file)
                # print("\t\t\nThe OUTPUT is:\n")
                # print(output, "\n")
                # print("\nThe Chosen Elevator is:", output.iloc[[0]].values[0][5])
                # print("Current Dict:", elev_list[int(output.iloc[[0]].values[0][5])].floor_timestamp_dict, "\n\n")
                size = len(call_file)
            else:  # call is DOWN
                # print("\nThe First Call is a DOWN call from:",first_call.originFloor,"--->",first_call.destFloor,"\n")
                temp_df = make_down(call_file.loc[1:])  # WORKS
                # print("\nThis is the Make_DOWN_df:", "First Call origin floor=", first_call.originFloor, "MinFloor=", building_b.minFloor)
                # print(temp_df)
                for src in range(first_call.originFloor, building_b.minFloor, -1):  # WORKS
                    src_df = temp_df[temp_df['src'] == src]  # WORKS
                    # print("\nThis is the src_df:", "src=", src)
                    # print(src_df)
                    for e in elev_list:
                        # print("\n\t\tLooping through the Building Elevator LIST\n")
                        # print("Elevator ID:", e.id)
                        # print("First Call:", first_call.__str__())
                        # print("Dictionary Before FIRST Call:", dict_before_first_call)
                        # print("Dictionary After FIRST Call:", e.floor_timestamp_dict,"\n")
                        dict_Before_added_calls = e.floor_timestamp_dict.copy()
                        for i in range(1, len(src_df)):
                            curr_call = Call(src_df.iloc[[i]].values[0])
                            if curr_call.timeStamp > e.floor_timestamp_dict[e.minFloor]:
                                # print("\nTHE NEXT CALLS TIMESTAMPS ARE GREATER THAN THE MIN-FLOOR TIMESTAMP. THEY ARE IRELEVANT\n")
                                break
                            e.addCall(curr_call)
                            # print("Checking Call:", curr_call.__str__(), "to Elevator:", e.id)
                        # print("Current number of calls in Elevator",e.id,": ",e.callAmount)
                        # print("Added Calls:", [call.__str__() for call in e.callList])
                        # print("Dictionary BEFORE Added Calls:", dict_Before_added_calls)
                        # print("Dictionary AFTER Added Calls:",e.floor_timestamp_dict,"\n")
                output = allocate_elev(elev_list, output, call_file)
                # print("\t\t\nThe OUTPUT is:\n")
                # print(output,"\n")
                # print("\nThe Chosen Elevator is:",output.iloc[[0]].values[0][5])
                # print("Current Dict:",elev_list[int(output.iloc[[0]].values[0][5])].floor_timestamp_dict,"\n\n")
                size = len(call_file)
    output["elevatorIndex"] = output['elevatorIndex'].astype(str).astype(float).astype(int)
    output["timeStamp"] = output['timeStamp'].astype(str).astype(float)
    output["src"] = output['src'].astype(str).astype(float).astype(int)
    output["dest"] = output['dest'].astype(str).astype(float).astype(int)
    output["status"] = output['status'].astype(str).astype(float).astype(int)
    make_output(output, "output.csv")


'''This function receives the elevator list and chooses the best elevator fir the calls.'''


def allocate_elev(elevator_list, output, call_file):
    best = 0
    min_time = calc_time(elevator_list[best])
    try:
        for i in range(0, len(elevator_list)):
            if calc_time(elevator_list[i]) < min_time:
                min_time = calc_time(elevator_list[i])
                best = i
    except TypeError:
        print("empty list")
    for i in range(0, len(elevator_list)):
        if i != best:
            wipe(elevator_list[i], "not_best")  # clear the elevator list and dictionary
    addIndex(elevator_list[best])
    output = send_to_output(elevator_list[best], output)
    # update_call_file(call_file, elevator_list[best])
    for call in elevator_list[best].callList:
        update_call_file(call_file, call)
    wipe(elevator_list[best], "best")
    # print("Best: ", best, ". dict: ", elevator_list[best].floor_timestamp_dict)
    return output


'''This function receives an elevator and calculates the average waiting time for the calls in the elevator call list.'''


def calc_time(elev):
    if len(elev.callList) != 0:
        call_list = elev.callList
        total_time = 0
        people = len(elev.callList)
        for call in call_list:
            total_time += (elev.floor_timestamp_dict[call.destFloor] - call.timeStamp)
        return float(total_time / people)


'''This function clears the elevator list and resets the elevator timestamp dictionary.'''


def wipe(elev, str):
    if str == "best":
        if len(elev.callList) != 0:
            start = elev.callList[len(elev.callList) - 1].destFloor
            for i in range(start + 1, elev.maxFloor + 1):
                elev.floor_timestamp_dict[i] = elev.floor_timestamp_dict[i - 1] + elev.speed
            for i in range(start - 1, elev.minFloor - 1, -1):
                elev.floor_timestamp_dict[i] = elev.floor_timestamp_dict[i + 1] + elev.speed
            elev.callList = []
            elev.callAmount = 0
    else:
        elev.callList = []
        elev.callAmount = 0
        # elev.floor_timestamp_dict = {index: x for index, x in enumerate([0.0] * elev.total_floors, start=elev.minFloor)}


'''This function receives the original call file and a call and drops the call from the call file. It is done 
           after the call has been taken care of.'''


def update_call_file(call_file, call):
    # for i in range(len(curr_elev.callList)):
    #     ts = curr_elev.callList[i].timeStamp
    #     call_file = call_file.drop(call_file[call_file.timeStamp == ts].index, inplace=True)
    call_file = call_file.drop(call_file[call_file.timeStamp == call.timeStamp].index, inplace=True)
    # print("\n\n\t\tDropped From Main File Call:",call.__str__(),"\n\n")


'''This function receives an elevator and the output csv file and adds the call to the output file.'''


def send_to_output(curr_elev, output):
    df = elev_df(curr_elev)
    return pd.concat([df, output], ignore_index=True)


'''This function changes the elevator index of the current call to the best elevator given.'''


def addIndex(curr_elev):
    for call in curr_elev.callList:
        call.elevatorIndex = int(float(curr_elev.id))


'''This function receives the current best elevator and creates a dataframe from its call list. '''


def elev_df(curr_elev):
    data = {'stam_str': [], 'timeStamp': [], 'src': [], 'dest': [], 'status': [], 'elevatorIndex': []}
    for call in curr_elev.callList:
        data['stam_str'].append(call.stam_str)
        data['timeStamp'].append(call.timeStamp)
        data['src'].append(call.originFloor)
        data['dest'].append(call.destFloor)
        data['status'].append(call.status)
        data['elevatorIndex'].append(int(float(call.elevatorIndex)))
    return pd.DataFrame(data)


'''This function receives the call csv file and transforms it to a dataframe.'''


def make_df(file):
    # creating the csv file
    dataframe = pd.read_csv(file)
    # now we are going to sort out the columns
    # making header columns so we can work with the csv
    col = dataframe.columns  # saving all the columns names
    dataframe.loc[-1] = [col[0], float(col[1]), int(col[2]), int(col[3]), 0, -1]  # adding a row
    dataframe.index = dataframe.index + 1  # shifting index
    dataframe = dataframe.sort_index()  # sorting by index
    # renaming the columns to what we decide its only for our use when we allocate
    dataframe.rename(
        columns={col[0]: 'stam_str', col[1]: 'timeStamp', col[2]: 'src', col[3]: 'dest', col[4]: 'status',
                 col[5]: 'elevatorIndex'}, inplace=True)
    # now we will generate the status for each call
    for i in range(len(dataframe)):
        if int(dataframe.src[i]) < int(dataframe.dest[i]):
            dataframe.status[i] = 1
        else:
            dataframe.status[i] = -1
    return dataframe


'''This function receives a dataframe and returns a new dataframe with only UP calls.'''


def make_up(dataframe):
    df_up = dataframe[dataframe['status'] == 1]
    df_up = df_up.sort_values(['src', 'timeStamp'], ascending=True)
    df_up = df_up.reset_index()
    df_up.drop(['index'], axis=1, inplace=True)
    return df_up


'''This function receives a dataframe and returns a new dataframe with only DOWN calls.'''


def make_down(dataframe):
    df_down = dataframe[dataframe['status'] == -1]
    df_down = df_down.sort_values(['src', 'timeStamp'], ascending=True)
    df_down = df_down.reset_index()
    df_down.drop(['index'], axis=1, inplace=True)
    return df_down


'''This function receives a dataframe and a string name and returns an output csv file in the name of the given string.'''


def make_output(dataframe, df_name: str = None):
    dataframe = dataframe.drop_duplicates()
    dataframe = dataframe.sort_values(['timeStamp'], ascending=True)
    new_header = dataframe.iloc[0]  # grab the first row for the header
    dataframe = dataframe[1:]  # take the data less the header row
    dataframe.columns = new_header  # set the header row as the df header
    dataframe.to_csv(df_name, index=False)


'''This is the MAIN function.'''


def main():
    b1 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B1.json"  # (-2,10)
    b2 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B2.json"  # (-2,10)
    b3 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B3.json"  # (-10,100)
    b4 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B4.json"  # (-10,100)
    b5 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B5.json"  # (-10,100)

    c_a = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_a.csv"  # (b1, b2)
    c_b = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_b.csv"  # (b3, b4, b5)
    c_c = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_c.csv"  # (b3, b4, b5)
    c_d = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_d.csv"  # (b3, b4, b5)
    Ex1(b3, c_d)


if __name__ == "__main__":
    main()

'''When removing the set dict to 0.0 in the Wipe function there are musch more distributed results.'''
