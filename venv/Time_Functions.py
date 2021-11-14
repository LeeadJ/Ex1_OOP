import json
from elevator import*
from Call import*
from Building import*
import csv
import copy



def call_time(curr_elevator, curr_call):
  start_time = curr_call.timeStamp
  labor_time = curr_elevator.closetime + curr_elevator.opentime + curr_elevator.starttime + curr_elevator.stoptime
  total_floors = abs(curr_call.destFloor - curr_call.originFloor)
  total_time = (total_floors * curr_elevator.speed) + labor_time
  return total_time






