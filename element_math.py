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
		dset.element_remove(h)
		
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
	#given one element, this algorithm will return the hashes of elements that describe the same motions with different runs
	
	#These are the columns that must match
	matching_columns = ['SpecimenNumber','ParentSegment','ChildSegment','Condition','Motion']
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
	
def get_complement_elements(dset, hash):
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
		
def _total_rotation(dset, hash_set):
	#you need hashes from matching data in all three planes
	
	elements = []
	for h in hash_set:
		elements.append(dset.retrieve(h))
		#this is where hashing isn't great. converting from deg to rad means changing the hash
		assert (elements[-1]['Units'] == 'Radians'),'Units must be in radians'
		assert (elements[-1]['Motion'] != 'TotalRotation'), 'TrailRun has already been calculated'
		dset.element_remove(h)
	
	n = elements[0]['Data'].size
	
	result_array = np.zeros(elements[0]['Data'].shape,dtype=np.longdouble)
	
	#possibly assert that elements has three.... elements. one for each plane of motion
	checkstring = str(elements[0]['Motion']) + " " + str(elements[1]['Motion']) + " " + str(elements[2]['Motion'])
	
	for i in range(0,elements[0]['Data'].size-1):

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
	#oringinally had the non-string keyword as none. Caused problems.
	result_element['Color'] = 'None'
	
	dset.add_element(result_element)
	
def _total_distance(dset, hash):

	el = dset.retrieve(hash)
	assert (el['Motion'] == 'TotalRotation'),'Element is not magnitude of rotation format'
	
	accumulator = 0.0
	
	for i in range(0,el['Data'].size):
		accumulator += (el['Data'][i])
		
	return accumulator
	
def get_total_rotation(dset):
	'''Transforms dataset by calculating how much specimen rotated'''
	assert (isinstance(dset,KinematicDataset)),"Must pass KinematicDataset type to get_total_rotation function"
	
	#make a list of the distinct groups

	complement_elements = []
	
	d = copy(dset)
	
	for e in dset.dataset:
		m = get_complement_elements(d, e['md5'])
		m.sort() #sorting will make it easier to remove duplicates
		if m not in complement_elements:
			complement_elements.append(m)
	
	for group in complement_elements:
		_total_rotation(dset, group)

def get_range(dset, hash):
	el = dset.retrieve(hash)
	max = np.amax(el['Data'])
	min = np.amin(el['Data'])
	return [max, min]

def get_dataset_ranges(dset):

	result = []
	el_range = []

	for el in dset.dataset:
		el_range = get_range(dset,el['md5'])
		result.append([el['md5'],el_range[0],el_range[1]])
	
	pretty_print(dset,result)

def get_total_distance(dset):
	#return list of elements with their hashes

	result = []

	for e in dset.dataset:
		hsh = e['md5']
		tot_dist = _total_distance(dset,hsh)
		result.append([hsh,tot_dist])

	pretty_print(dset,result)

def pretty_print(dset, hashlist):
	#if hashlist is single element, print just the dataset
	#if hashlist is dual element, don't print data, print whatever is element 2 thru n is instead

	output = []
	output_string = ""

	col = dset.columns()
	if 'Color' in col:
		col.remove('Color')
	
	if 'md5' in dset.columns():
		col.remove('md5')

	if len(hashlist[0]) > 1:
		extra_data = True
		col.remove('Data')

	for c in col:
		output_string = output_string + str(c) + ","
	output_string.rstrip(",")

	print(output_string)

	for h in hashlist:
		output_string = ""
		if extra_data:
			el = dset.retrieve(h[0])
		else:
			el = dset.retrieve(h)
		for c in col:
			#print(str(c) + "  " + str(el[c]))
			output_string = output_string + str(el[c]) + ","
		if extra_data:
			for i in range(1,len(h)):
				output_string = output_string + str(h[i]) + ","
		output_string.rstrip(",")
		output_string.rstrip(",")
		print(output_string)



