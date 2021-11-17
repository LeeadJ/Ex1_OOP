import pandas as pd
from Call import *
from Building import *


def Ex1(Building_json, call_csv):
    building_b = Building(Building_json)
    elev_list = building_b.ElevatorList
    call_file = make_df(call_csv)
    size = len(call_file)
    data = {'stam_str': [], 'timeStamp': [], 'src': [], 'dest': [], 'status': [], 'elevatorIndex': []}
    output = pd.DataFrame(data)
    while size != 0:
        if building_b.elevatorAmount == 1:
            output = pd.concat([call_file, output], ignore_index=True)
            output = output.assign(elevatorIndex=0)
            size = 0
        else:
            first_call = Call(call_file.iloc[[0]].values[0])
            for i in elev_list:
                i.addCall(first_call)
            if first_call.status == 1:  # call is UP
                temp_df = make_up(call_file.loc[1:])
                for src in range(first_call.originFloor, building_b.maxFloor):
                    src_df = temp_df[temp_df['src'] == src]
                    for e in elev_list:
                        for i in range(1,len(src_df)+1):
                            curr_call = Call(src_df.iloc[[i]].values[0])
                            e.addCall(curr_call)
                output = allocate_elev(elev_list, output, call_file)
            else:  # call is DOWN
                temp_df = make_down(call_file.loc[1:])
                for src in range(first_call.originFloor, building_b.minFloor, -1):
                    src_df = temp_df[temp_df['src'] == src]
                    for e in elev_list:
                        for i in range(1, len(src_df) + 1):
                            curr_call = Call(src_df.iloc[[i]].values[0])
                            e.addCall(curr_call)
                output = allocate_elev(elev_list, output, call_file)
    make_output(output, "output.txt")


'''This function receives the elevator list and chooses the best elevator fir the calls.'''


def allocate_elev(elevator_list, output, call_file):
    best = 0
    min_time = calc_time(elevator_list[0])
    for i in range(1, len(elevator_list)):
        if calc_time(elevator_list[i]) < min_time:
            min_time = calc_time(elevator_list[i])
            best = i
    for i in range(0, len(elevator_list)):
        if i != best:
            wipe(elevator_list[i])  # clear the elevator list and dictionary
    addIndex(elevator_list[best])
    output = send_to_output(elevator_list[best], output)
    update_call_file(call_file, elevator_list[best])
    wipe(elevator_list[best])
    return output

def update_call_file(call_file, curr_elev):
    for call in curr_elev.callList:
        ts = call.timeStamp
        call_file = call_file.drop
        call_file = call_file.drop(call_file[call_file.timeStamp==ts].index)


'''This function receives an elevator and creats the output DataFrame.'''

def send_to_output(curr_elev, output):
    df = elev_df(curr_elev)
    return pd.concat([df, output], ignore_index=True)


'''This functions updates the calls with the correct elevator index.'''


def addIndex(curr_elev):
    for call in curr_elev.callList:
        call.elevatorIndex = curr_elev.id


'''This function creates a DataFrame.'''


def elev_df(curr_elev):
    data = {'stam_str': [], 'timeStamp': [], 'src': [], 'dest': [], 'status': [], 'elevatorIndex': []}
    for call in curr_elev.callList:
        data['stam_str'].append(call.stam_str)
        data['timeStamp'].append(call.timeStamp)
        data['src'].append(call.originFloor)
        data['dest'].append(call.destFloor)
        data['status'].append(call.status)
        data['elevatorIndex'].append(call.elevatorIndex)
    return pd.DataFrame(data)


'''This function clears the elevator list and resets the elevator timestamp dictionary.'''


def wipe(curr_elev):
    curr_elev.callList = []
    curr_elev.floor_timestamp_dict = {index: x for index, x in
                                      enumerate([0.0] * curr_elev.total_floors, start=curr_elev.minFloor)}


'''This function calculates the average time of the passenger in the elevator (from src to dest)'''


def calc_time(elev):
    if len(elev.callList) != 0:
        call_list = elev.callList
        total_time = 0
        people = len(elev.callList)
        for call in call_list:
            total_time += (elev.floor_timestamp_dict[call.destFloor] - call.timeStamp)
        return total_time / people


'''This function creats a DataFrame from the call_csv.'''


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


'''This function creates a DataFrame of UP calls only. The DataFrame will be sorted 'src' and hen 'timeStamp'.'''


def make_up(dataframe):
    df_up = dataframe[dataframe['status'] == 1]
    df_up = df_up.sort_values(['src', 'timeStamp'], ascending=True)
    df_up = df_up.reset_index()
    df_up.drop(['index'], axis=1, inplace=True)
    return df_up


'''This function creates a DataFrame of DOWN calls only. The DataFrame will be sorted 'src' and hen 'timeStamp'.'''


def make_down(dataframe):
    df_down = dataframe[dataframe['status'] == -1]
    df_down = df_down.sort_values(['src', 'timeStamp'], ascending=True)
    df_down = df_down.reset_index()
    df_down.drop(['index'], axis=1, inplace=True)
    return df_down


'''This function creates the FINAL output file.'''


def make_output(dataframe, df_name: str = None):
    dataframe = dataframe.drop_duplicates()
    new_header = dataframe.iloc[0]  # grab the first row for the header
    dataframe = dataframe[1:]  # take the data less the header row
    dataframe.columns = new_header  # set the header row as the df header
    # returning without index

    dataframe.to_csv(df_name, index=False)


'''This is the MAIN function.'''


def main():
    b1 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B1.json"
    b2 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B2.json"
    c_a = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_a.csv"
    # c_a = make_df(c_a)
    # print(c_a)
    # print()
    # print(c_a.iloc[[0]])
    # print()
    # c_b = c_a.iloc[[0]]
    # print(c_b.values[0])
    # print("start here")
    # for i in range(1,len(c_a)+1):
    #     print(c_a.iloc[[i]].values[0])
    # c_c = c_b.values[0]
    # print(c_b.values[0][1])
    # building_b = Building(b2)
    Ex1(b2, c_a)
    # elev_list = building_b.ElevatorList
    # call_file = make_df(c_a)
    # # print(call_file)
    # first_call = Call(call_file.iloc[0])
    # temp_df = {}
    # for i in elev_list:
    #     i.addCall(first_call)
    # if first_call.status == 1:  # call is UP
    #     temp_df = make_up(call_file.loc[1:])
    #     for src in range(first_call.originFloor, building_b.maxFloor):
    #         src_df = temp_df[temp_df['src'] == src]
    #         # print(src_df)
    #         for e in elev_list:
    #             for row in src_df:
    #                 curr_call = Call(row)
    #                 e.addCall(curr_call)
    #             # print(e.__str__())
    #
    # else:
    #     temp_df = make_down(call_file.loc[1:])
    #     for src in range(first_call.originFloor, building_b.minFloor, -1):
    #         src_df = temp_df[temp_df['src'] == src]
    #         print(src_df)
    #         for e in elev_list:
    #             for i in range(len(src_df)):
    #                 curr_call = Call(src_df.iloc[i])
    #                 # print(curr_call.__str__())
    #                 e.addCall(curr_call)
    #             # print(e.__str__())
    #         print(calc_time(elev_list[0]))
    #         print(elev_list[0].floor_timestamp_dict)



if __name__ == "__main__":
    main()
# b = Building(r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B2.json")
# c_a = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_a.csv"
# empty_output = r"C:\Users\Leead\Desktop\Ex1_csv\testeroutput_empty.csv"
# df = make_df(c_a)
# df = make_down(df)
# # # print(df)
# call = Call(df.loc[58])
# # print(call.__str__())
# e = b.ElevatorList[0]
# e.addCall(call)
# # print(e.floor_timestamp_dict)
# call2 = Call(df.loc[59])
# # print(call2.__str__())
# e.addCall(call2)
# print(e.floor_timestamp_dict)
# # print(e.__str__())


# data = {'stam_str': [], 'timeStamp': [], 'src': [], 'dest': [], 'status': [], 'elevatorIndex': []}
# output = pd.DataFrame(data)
# print(output)
# print()
# e = b.ElevatorList[0]
# call = Call(df.loc[58])
# e.addCall(call)
# output = send_to_output(e, output)
# print(output)
# print()
# call2 = Call(df.loc[59])
# e.addCall(call2)
# output = send_to_output(e, output)
# print(output)
# make_output(output, "tester_output")
# print()
