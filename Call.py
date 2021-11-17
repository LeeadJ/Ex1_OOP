class Call:
    """
    Here the initializer will receive a list from the call list.
    - The list will represent a single call.
    - Each index of the list will represent a certain value from the call (0-5)
    """

    def __init__(self, csv_file_list):
        self.stam_str = csv_file_list[0]
        self.timeStamp = float(csv_file_list[1])
        self.originFloor = int(csv_file_list[2])
        self.destFloor = int(csv_file_list[3])
        self.status = int(csv_file_list[4])
        self.elevatorIndex = int(csv_file_list[5])
        # self.stam_str = str(csv_file_list[0])
        # self.timeStamp = float(csv_file_list[1])
        # self.originFloor = int(csv_file_list[2])
        # self.destFloor = int(csv_file_list[3])
        # self.status = int(csv_file_list[4])
        # self.elevatorIndex = int(csv_file_list[5])


    def __str__(self):
        return self.stam_str, self.timeStamp, self.originFloor, self.destFloor, self.status, self.elevatorIndex
