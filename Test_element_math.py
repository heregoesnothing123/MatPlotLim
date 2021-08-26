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

datapoints = len(t2.dataset)
print("Number of datapoints before averaging: " + str(datapoints))
average_dataset(t2)
print("Number of datapoints after averaging : " + str(len(t2.dataset)))
 
