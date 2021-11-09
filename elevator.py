class elevator:
    def __init__(self, id, speed, minFloor, maxFloor, closetime, opentime, starttime, stoptime):
        self.minFloor = minFloor
        self.maxFloor = maxFloor
        self.id = id
        self.speed = speed
        self.closetime = closetime
        self.opentime = opentime
        self.starttime = starttime
        self.stoptime = stoptime
        self.pos = 0  # the elevator is starting at ground floor
        self.state = 0  # Moving Down: -1/ Level: 0/ Moving Up: 1

    def goto(self, floor):
        if self.pos < floor:
            self.setState(1)
        elif self.pos > floor:
            self.setState(-1)
        else:
            self.setState(0)
        self.pos = floor

    def setState(self, num):
        self.state = num

    def stop(self, floor):
        self.goto(floor)

    def __str__(self):
        return self.id, self.speed,self.minFloor, self.maxFloor,  self.closetime, self.opentime,\
               self.starttime, self.stoptime




