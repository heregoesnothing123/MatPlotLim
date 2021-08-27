from kinematicdataset import *
from element_math import *
from copy import copy
#Testing program for KinematicDataset

#Test: Load prepared CSV file
test = KinematicDataset()
test.construct_from_file('jointKinematics.csv')

#First, we will copy our dataset and work on that
print("\n\n")
print("==================================================")
print("Testing Dataset Averaging=========================")
print("==================================================")
t2 = copy(test)

print("Number of datapoints before averaging: " + str(len(t2.dataset)))
average_dataset(t2)
print("Number of datapoints after averaging : " + str(len(t2.dataset)))
 
print("\n\n")
print("==================================================")
print("Testing Total Rotation============================")
print("==================================================")
t3 = copy(test)

print("Number of datapoints before transform: " + str(len(t3.dataset)))
t3.convert_to_rad()
get_total_rotation(t3)
print("Number of datapoints after transform: " + str(len(t3.dataset)))