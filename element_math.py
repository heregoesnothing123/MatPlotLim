#contains range of motion functions
from KinematicDataset import *
import numpy as np
import scipy as sp


def average_dataset(dset):
	'''Transforms dataset by averaging everything that matches except for run ID'''
	assert (isinstance(d,KinematicDataset)),"Must pass KinematicDataset type to average_dataset function"
	
	#make a list of the distinct groups
	
	d = dset.copy() #don't edit the passed object. make a new one
	
	list_of_elements = {}
	
	list_of_keys = d.columns()
	
	matching_elements = []
	
	for element1 in dset:
		matching_group = []
		match = 1
		
		already_matched = any(element1['md5'] in i for i in matching_elements) #checks if hash has already been added to 2D list
		
		if not already_matched:
			matching_group.append(element1['md5'])
			for element2 in d:
				for k in list_of_keys:
					if k != 'Data' and k != 'TrialRun' and k != 'md5':
						if element2[k] != element1[k]:
							match *= 0
				
				#if all non data and trialrun matched (as did the hash), then match should still be 1
				if match == 1:
					matching_group.append(element2['md5'])
					
		if matching_group != []:
			matching_elements.append(matching_group)
			
	#now we have a 2D list, each item of the list is a list of the hashes of elements where everything matches except the trialrun (and actual data and hash).
	
	for group in matching_elements:
		dset.average_elements_by_hash(d, group)
	
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
		
	newlist = []

	#make numpy array of zeros that is same dimension as one of the datasets (will crash if elements don't match size)
	result_array = np.zeros(elements[0]['Data'].shape,dtype=np.longdouble)
	
	N = len(elements)
	
	for i in range(0,len(elements)):
		np.add(result_array,elements[i]['Data'],out=result_array) #i hope I can do an inplace by setting result to be one of the inputs
		
	result_array = result_array / N

	newelement['Data'] = result_array
	
	#now iterate over the columns
	col = dset.columns()
	
	#this code sets the averaged data element descriptive columns. If all elements that went into the average match, then set this element
	#descriptive columns to match. If they don't all match, leave it blank.
	for c in col:
		match = 1
		for i in range(0,len(elements)-1):
			if elements[i][c] != elements[i+1][c]:
				match *= 0
		if match == 1:
			newelement[c] == elements[0][c]
		else:
			newelement[c] == ""
			
	dset.add_element(newelement)

def get_matching_elements(dset, hash):
		#given one element, this algorithm will return the hashes of elements that describe the same run with different motions
		
		#These are the columns that must match
		matching_columns = ['SpecimenNumber','TrialRun','ParentSegment','ChildSegment','Condition']
		d = dset.copy()
		element_to_match = d.retrieve(hash)
		d.remove(hash) #so we don't get a duplicate	
		keep_element = 1
		matching_elements = []
		matching_elements.append(hash)
		
		for el in d:
			for i in matching_columns:
				if el[i] != element_to_match[i]:
					keep_element *= 0
			if keep_element == 1:
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
	
	#sum of squares using elementwise math
	
	#square each element
	for e in elements:
		np.square(e['Data'],out=e['Data'])
	
	#sum the squares by element
	result_array = np.zeros(elements[0]['Data'].shape,dtype=np.longdouble)
	for i in range(0,len(elements)):
		np.add(result_array,elements[i]['Data'],out=result_array)
	
	#square root for magnitude
	np.sqrt(result_array)
	
	result_element = {}
	
	matching_columns = ['SpecimenNumber','TrialRun','ParentSegment','ChildSegment','Condition','Units']
	for k in matching_columns:
		result_element[k] = elements[0][k]
	
	result_element['Signs'] = 'AbsoluteValue'
	result_element['Motion'] = 'TotalRotation'
	
	dset.add_element(result_element)
	
def total_distance(dset, hash):
#not working. I screwed up distance calculation
	el = retrieve(hash)
	assert (el['Motion'] == 'TotalRotation'),'Element is not a representation of magnitude of rotation'
	
	accumulator = np.longdouble(0.0)
	
	for i in range(1,el['Data'].size)
		accumulator += (el['Data'][i]