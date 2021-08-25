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
		self.__average_elements_by_hash(d, group)
	
def __average_elements_by_hash(dset, list_of_hashes):
	#in place transformation, removes the input hashes
	
	elements = []
	
	#dictionary containing the average result
	newelement = {}
	
	#get the elements that correspond to the input hashes
	for h in list_of_hashes:
		elements.append(dset.retrieve(h))
		
	newlist = []

	result_array = np.zeros(elements[0]['Data'].shape,dtype=np.longdouble)
	
	N = len(elements)
	
	for i in range(0,len(elements)):
		np.add(result_array,elements[i]['Data'],out=result_array) #i hope I can output result into one of the operands
		
	result_array = result_array / N

	newelement['Data'] = result_array
	
	#now iterate over the columns
	col = dset.columns()
	
	for c in col:
		match = 1
		for i in range(0,len(elements)-1):
			if elements[i][c] != elements[i+1][c]:
				match *= 0
		if match == 1:
			newelement[c] == elements[0][c]
		else:
			newelement[c] == ""
	
	return newelement
	
#end
	
	
	