from KinematicDataSet import *

#Test: Load prepared CSV file
test = KinematicDataset()
test.construct_from_file('jointKinematics.csv')

print("\nTesting Units================")
print("All Units in dataset : " + str(test.units))

print("\nTesting Filtering=================")
#Test: Filtering by information we want
filterdataset = test.filter('Motion','Axial')

print("Original units : " + str(test.units))
print("Units in filtered dataset : " + str(filterdataset.units))

print("Signs : " + str(test.signs))
print("Filtered Signs : " + str(filterdataset.signs))

print(test)
print(filterdataset)

