from kinematicdataset import *
from element_math import *

#this file gets the data we need and spits it out to the console for our charts

dataset = KinematicDataset()
dataset.construct_from_file('c:\kinematicdata\jointKinematics.csv')

dataset = dataset.filter("ParentSegment","Tibia")
dataset = dataset.filter("ChildSegment","Talus")
dataset = dataset.filter("SpecimenNumber","6",keep=False)

#dataset.convert_to_rad()
#get_total_rotation(dataset)
#average_dataset(dataset)
#get_total_distance(dataset)

average_dataset(dataset)
get_dataset_ranges(dataset)