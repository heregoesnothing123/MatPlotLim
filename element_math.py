#contains range of motion functions
from kinematicdataset import *
import numpy as np
import scipy as sp
from copy import copy

def average_dataset(dset):
	'''Transforms dataset by averaging everything that matches except for run ID'''
	assert (isinstance(dset,KinematicDataset)),"Must pass KinematicDataset type to average_dataset function"
	
	#make a list of the distinct groups

	matching_elements = []
	
	d = copy(dset)
	
	for e in dset.dataset:
		m = get_matching_elements(d, e['md5'])
		m.sort() #sorting will make it easier to remove duplicates
		if m not in matching_elements:
			matching_elements.append(m)
	
	for group in matching_elements:
		_average_elements_by_hash(dset, group)
	
def _average_elements_by_hash(dset, list_of_hashes):
	#in place transformation, removes the input hashes
	#underscore in front of function is Python suggestion to other programmers that you aren't supposed to directly call this function
	
	elements = []
	
	#dictionary containing the average result
	newelement = {}
	
	#get the elements that correspond to the input hashes
	for h in list_of_hashes:
		elements.append(dset.retrieve(h))
		dset.remove(h)
		
	#make numpy array of zeros that is same dimension as one of the datasets (will crash if elements don't match size)
	sh = elements[0]['Data'].shape
	
	result_array = np.zeros(sh,dtype=np.longdouble)
	
	N = len(elements)
	
	for i in range(0,len(elements)):
		np.add(result_array,elements[i]['Data'],out=result_array) #i hope I can do an inplace by setting result to be one of the inputs
		
	result_array = result_array / N

	newelement['Data'] = result_array
	
	#now iterate over the columns
	col = dset.columns()
	col.remove('Data')
	
	#this code sets the averaged data element descriptive columns. If all elements that went into the average match, then set this element
	#descriptive columns to match. If they don't all match, leave it blank.
	for c in col:
		match = 1
		for i in range(0,len(elements)-1):
			if elements[i][c] != elements[i+1][c]:
				match *= 0
		if match == 1:
			newelement[c] = elements[0][c]
		else:
			newelement[c] = ""
			
	dset.add_element(newelement)

def get_matching_elements(dset, hash):
	#given one element, this algorithm will return the hashes of elements that describe the same run with different motions
	
	#These are the columns that must match
	matching_columns = ['SpecimenNumber','TrialRun','ParentSegment','ChildSegment','Condition']
	element_to_match = dset.retrieve(hash)
	matching_elements = []
	matching_elements.append(hash)
	
	for el in dset.dataset:
		keep_element = 1
		for i in matching_columns:
			if el[i] != element_to_match[i]:
				keep_element *= 0
		if keep_element == 1:
			if el['md5'] not in matching_elements:
				matching_elements.append(el['md5'])
			
	return matching_elements
		
def total_rotation(dset, hash):
	#you need hashes from matching data in all three planes
	hash_set = get_matching_elements(dset, hash)
	elements = []
	for h in hash_set:
		elements.append(dset.retrieve(h))
		#this is where hashing isn't great. converting from deg to rad means changing the hash
		assert (elements[-1]['Units'] == 'Radians'),'Units must be in radians'
		assert (elements[-1]['Motion'] != 'TotalRotation'), 'TrailRun has already been calculated'
		dset.remove(h)
	
	n = elements[0]['Data'].size
	
	result_array = np.zeros(elements[0]['Data'].shape,dtype=np.longdouble)
	
	#possibly assert that elements has three.... elements. one for each plane of motion
	for i in range(0,len(elements[0]['Data'].size)-1):
		dim1 = elements[0]['Data'][i+1] - elements[0]['Data'][i]
		dim2 = elements[1]['Data'][i+1] - elements[1]['Data'][i]
		dim3 = elements[2]['Data'][i+1] - elements[2]['Data'][i]
		
		dim1 = dim1 ** 2
		dim2 = dim2 ** 2
		dim3 = dim3 ** 2
		
		#since all are summed we will do in-place addition (accumulation the way assembly does it)
		dim1 += dim2
		dim1 += dim3
		
		#in place division, now our result is stored in dim1. Since every loop dim1 is reset this is OK.
		dim1 /= 3.0
		
		result_array[i] = dim1
	
	result_element = {}
	
	result_element['Data'] = result_array
	
	matching_columns = ['SpecimenNumber','TrialRun','ParentSegment','ChildSegment','Condition','Units']
	for k in matching_columns:
		result_element[k] = elements[0][k]
	
	result_element['Signs'] = 'AbsoluteValue'
	result_element['Motion'] = 'TotalRotation'
	
	dset.add_element(result_element)
	
def total_distance(dset, hash):

	el = retrieve(hash)
	assert (el['Motion'] == 'TotalRotation'),'Element is not magnitude of rotation format'
	
	accumulator = np.longdouble(0.0)
	
	for i in range(0,el['Data'].size):
		accumulator += (el['Data'][i])
		
	return accumulator