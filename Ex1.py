import pandas as pd
from Call import *
from Building import *


def Ex1(Building_json, call_csv):
    building_b = Building(Building_json)
    elev_list = building_b.ElevatorList
    call_file = make_df(call_csv)
    # call_file.to_csv("call_file", index=False)///////////////////////////////
    size = len(call_file)
    data = {'stam_str': [], 'timeStamp': [], 'src': [], 'dest': [], 'status': [], 'elevatorIndex': []}
    output = pd.DataFrame(data)
    # output.to_csv("call_file", index=False)///////////////////////////
    while size != 0:
        if building_b.elevatorAmount == 1:
            output = pd.concat([call_file, output], ignore_index=True)
            output = output.assign(elevatorIndex=0)
            # output.to_csv("call_file", index=False)///////////////////
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
                        for i in range(1, len(src_df)):  # ///////////////////////////////////////
                            curr_call = Call(src_df.iloc[[i]].values[0])
                            e.addCall(curr_call)
                output = allocate_elev(elev_list, output, call_file)
                size = len(call_file)
            else:  # call is DOWN
                temp_df = make_down(call_file.loc[1:])
                for src in range(first_call.originFloor, building_b.minFloor, -1):
                    src_df = temp_df[temp_df['src'] == src]
                    for e in elev_list:
                        for i in range(1, len(src_df)):
                            curr_call = Call(src_df.iloc[[i]].values[0])
                            e.addCall(curr_call)
                output = allocate_elev(elev_list, output, call_file)
                size = len(call_file)
    output["elevatorIndex"] = output['elevatorIndex'].astype(str).astype(float).astype(int)
    output["timeStamp"] = output['timeStamp'].astype(str).astype(float)
    output["src"] = output['src'].astype(str).astype(float).astype(int)
    output["dest"] = output['dest'].astype(str).astype(float).astype(int)
    output["status"] = output['status'].astype(str).astype(float).astype(int)
    make_output(output, "output.csv")

'''This function calculates the average time of the passenger in the elevator (from src to dest)'''


def calc_time(elev):
    if len(elev.callList) != 0:
        call_list = elev.callList
        total_time = 0
        people = len(elev.callList)
        for call in call_list:
            # print(call.__str__())
            total_time += (elev.floor_timestamp_dict[call.destFloor] - call.timeStamp)
        return total_time / people

'''This function receives the elevator list and chooses the best elevator fir the calls.'''


def allocate_elev(elevator_list, output, call_file):
    best = 0
    min_time = calc_time(elevator_list[0])
    # print(min_time, type(min_time))
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
    # wipe(elevator_list[best])
    return output


def update_call_file(call_file, curr_elev):
    for call in curr_elev.callList:
        ts = call.timeStamp
        call_file.drop(call_file[call_file.timeStamp == ts].index, inplace=True)


'''This function receives an elevator and creats the output DataFrame.'''


def send_to_output(curr_elev, output):
    df = elev_df(curr_elev)
    return pd.concat([df, output], ignore_index=True)


'''This functions updates the calls with the correct elevator index.'''


def addIndex(curr_elev):
    for call in curr_elev.callList:
        call.elevatorIndex = int(float(curr_elev.id))


'''This function creates a DataFrame.'''


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


'''This function clears the elevator list and resets the elevator timestamp dictionary.'''


def wipe(curr_elev):
    curr_elev.callList = []
    curr_elev.floor_timestamp_dict = {index: x for index, x in
                                      enumerate([0.0] * curr_elev.total_floors, start=curr_elev.minFloor)}





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
    dataframe = dataframe.sort_values(['timeStamp'], ascending=True)
    new_header = dataframe.iloc[0]  # grab the first row for the header
    dataframe = dataframe[1:]  # take the data less the header row
    dataframe.columns = new_header  # set the header row as the df header
    # returning without index
    # dataframe['elevatorIndex'] = pd.to_numeric(dataframe['elevatorIndex'])
    dataframe.to_csv(df_name, index=False)


'''This is the MAIN function.'''


def main():
    b1 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B1.json"
    b2 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B2.json"
    b3 = r"C:\Users\Leead\Desktop\Ex1_csv\Ex1_Buildings\B3.json"
    c_a = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_a.csv"
    c_d = r"C:\Users\Leead\Desktop\Ex1_csv\calls\Calls_d.csv"
    Ex1(b2, c_a)


if __name__ == "__main__":
    main()
