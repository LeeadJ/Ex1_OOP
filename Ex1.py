import pandas as pd
from Call import *
from Building import *


def Ex1(Building_json, call_csv, output_csv):
    building_b = Building(Building_json)
    elev_list = building_b.ElevatorList
    call_file = make_df(call_csv)
    while call_file.size != 0:
        first_call = Call(call_file.iloc[0])
        temp_df = {}
        for i in elev_list:
            i.addCall(first_call)
        if first_call.status == 1:  # call is UP
            temp_df = make_up(call_file.loc[1:])
            for src in range(first_call.originFloor, building_b.maxFloor):
                src_df = temp_df[temp_df['src'] == src]

                for e in elev_list:
                    for row in src_df:
                        curr_call = Call(row)
                        e.addCall(curr_call)
            allocate_elev(elev_list)

        else:  # call is DOWN
            temp_df = make_down(call_file.loc[1:])
            for src in range(first_call.originFloor, building_b.minFloor - 1, -1):
                src_df = temp_df[temp_df['src'] == src]
                for e in elev_list:
                    for row in src_df:
                        curr_call = Call(row)
                        e.addCall(curr_call)
            allocate_elev(elev_list)


def allocate_elev(elevator_list):
    best = 0
    min_time = calc_time(elevator_list[0])


'''This function calculates the average time of the passenger in the elevator (from src to dest)'''
def calc_time(elev):
    if len(elev.callList) != 0:
        call_list = elev.callList
        total_time = 0
        people = len(elev.callList)
        for call in call_list:
            total_time += (elev.floor_timestamp_dict[call.destFloor] - call.timeStamp)
        return total_time / people


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


# function to make a data frame with only up calls
def make_up(dataframe):
    df_up = dataframe[dataframe['status'] == 1]
    df_up = df_up.sort_values(['src', 'timeStamp'], ascending=True)
    df_up = df_up.reset_index()
    df_up.drop(['index'], axis=1, inplace=True)
    return df_up


# function to make dataframe with only down calls
def make_down(dataframe):
    df_down = dataframe[dataframe['status'] == -1]
    df_down = df_down.sort_values(['src', 'timeStamp'], ascending=True)
    df_down = df_down.reset_index()
    df_down.drop(['index'], axis=1, inplace=True)
    return df_down


# creating function to return csv file correctly
def make_output(dataframe, df_name: str = None):
    new_header = dataframe.iloc[0]  # grab the first row for the header
    dataframe = dataframe[1:]  # take the data less the header row
    dataframe.columns = new_header  # set the header row as the df header
    # returning without index
    dataframe.to_csv(df_name, index=False)


def allocateCall():
    pass


def main():
    b2 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B2.json"
    c_a = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_a.csv"
    building_b = Building(b2)
    elev_list = building_b.ElevatorList
    call_file = make_df(c_a)
    # print(call_file)
    first_call = Call(call_file.iloc[0])
    temp_df = {}
    for i in elev_list:
        i.addCall(first_call)
    if first_call.status == 1:  # call is UP
        temp_df = make_up(call_file.loc[1:])
        for src in range(first_call.originFloor, building_b.maxFloor):
            src_df = temp_df[temp_df['src'] == src]
            # print(src_df)
            for e in elev_list:
                for row in src_df:
                    curr_call = Call(row)
                    e.addCall(curr_call)
                # print(e.__str__())

    else:
        temp_df = make_down(call_file.loc[1:])
        for src in range(first_call.originFloor, building_b.minFloor, -1):
            src_df = temp_df[temp_df['src'] == src]
            print(src_df)
            for e in elev_list:
                for i in range(len(src_df)):
                    curr_call = Call(src_df.iloc[i])
                    # print(curr_call.__str__())
                    e.addCall(curr_call)
                # print(e.__str__())
            print(calc_time(elev_list[0]))
            print(elev_list[0].floor_timestamp_dict)

#
# if __name__ == "__main__":
#     main()
b = Building(r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B2.json")
c_a = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_a.csv"
df = make_df(c_a)
df = make_down(df)
print(df)
call = Call(df.loc[0])
print(call.__str__())
e = b.ElevatorList[0]
e.addCall(call)
print(e.floor_timestamp_dict)
print(calc_time(e))
