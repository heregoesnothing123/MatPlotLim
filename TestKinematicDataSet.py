from KinematicDataSet import *
#Testing program for KinematicDataset

#Test: Load prepared CSV file
test = KinematicDataset()
test.construct_from_file('jointKinematics.csv')

#Test: Print number of 
print(test.num_datapoints())

print("========================================\n\n")

print(test.filter('ParentSegment','Tibia').num_datapoints())

print("========================================\n\n")

print(test.column_names)

print("========================================\n\n")

print(test.data[14])

print("========================================\n\n")

print(test.columns())
