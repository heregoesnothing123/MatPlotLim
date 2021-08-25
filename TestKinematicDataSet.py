from KinematicDataSet import *
#Testing program for KinematicDataset

#Test: Load prepared CSV file
test = KinematicDataset()
test.construct_from_file('jointKinematics.csv')

print("\n\n")
print("==================================================")
print("Testing Dataset Contsrtuction=====================")
print("==================================================")
#Test: Print information about this dataset
#Print description of data
print("Description of dataset: " + test.description)

#Print number of datapoints
datapoints = len(test.dataset)
print("Number of datapoints : " + str(datapoints))
print("Number of raw data points in element 35 : " + str(len(test.dataset[35]['Data'])))
#Print the name of the columns in the dataset
print("Names of Data Columns : " + str(test.column_names))

print("\n\nTesting Filtering=================")
print("==================================================")
#Test: Filtering by information we want
filterpts = len(test.filter('ParentSegment','Tibia',True).dataset)
print("Datapoints after filtering : " + str(filterpts))
removepts = len(test.filter('ParentSegment','Tibia',False).dataset)
print("Datapoints after removing : " + str(removepts))
#test that the description is updated correctly
print("New Description: " + test.filter('ParentSegment','Tibia').description)

print("Math check: Original = " + str(datapoints) + "; Filtering = " + str(filterpts) + "; Removing = " + str(removepts))
assert (filterpts + removepts == datapoints),"Math Failure during filtering"

print("\n\nTesting Retreiving a Single Element==============")
print("==================================================")
print(test.dataset[14])

print("\n\nTesting what columns exist================")
print("==================================================")
print(test.columns())

print("\n\nTesting Units================")
print("==================================================")
print("All Units in dataset : " + str(test.units))
print("Unit of element 35 : " + str(test.get_units(35)))
temp = dict(test.dataset[35])
del temp['Data']
print(temp)

print("\n\nTesting Signs================")
print("==================================================")
print("All Signs in dataset : " + str(test.signs))
print("Sign (Direction positive) of element 35 : " + str(test.get_sign(35)))
