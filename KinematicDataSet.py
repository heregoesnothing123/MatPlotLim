#File handling for the Kinematic Data
import hashlib #needed to give each element a uniqueID
import numpy as np
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning) #this to supress a numpy complaint.

class KinematicDataset:

	def __init__(self):
		self.dataset = []
		#the instance variable "dataset" is a list of dictionaries
		#dictionaries are defined by the preamble of the raw data
		#Each non-data column will have a dictionary entry
		self.column_names = []
		self.description = ""
		self.units = {}
		self.signs = {}
	
	def construct_from_file(self, filename, directory="C:\kinematicdata"):
	
		#first, check for preamble to the data defining its formatting (see data preamble section)
		
		file = directory+'\\'+filename
		
		f = open(file,'r',encoding='utf-8-sig')
		
		#Read what should be Section 1 of preamble
		firstline = f.readline().split(',')
		
		#Check to ensure it is the correct format
		assert (firstline[0].strip() == "[preamble]"),"File is not in correct format. No preamble found"
		
		if len(firstline) > 1:
			self.description = firstline[1].strip()
			
		#Read Section 2 and convert to integer
		num_nondatacolumns = int(f.readline())
		
		#Loop for lines in Section 3
		for i in range(0,num_nondatacolumns):
			self.column_names.append(f.readline().strip().split(','))
		
		#Read units in Section 4
		temp_unit = f.readline().split(',')
		assert (temp_unit[0].strip() == "Units"),"Section 4 (Units) not found"
		
		#first we need to get the column name that will determine the unit
		for i in range(0,len(self.column_names)):
			if temp_unit[1].strip() == self.column_names[i][0]:
				for j in range(1,len(self.column_names[i])):
					self.units[self.column_names[i][j]] = temp_unit[j+1].strip()
		
		temp_sign = f.readline().split(',')
		assert (temp_sign[0].strip() == "Sign"),"Section 5 (Sign) not found"
		
		for i in range(0,len(self.column_names)):
			if temp_sign[1].strip() == self.column_names[i][0]:
				for j in range(1,len(self.column_names[i])):
					self.signs[self.column_names[i][j]] = temp_sign[j+1].strip()
		
		#now we have set up names and the file pointer is at the first data
		run = True
		
		while run:
			#this is iterating over the data after setting up the preamble. each loop reads one line (one data item)
			line = f.readline().split(',')
			if line == [""]:
				break
			
			currentrow = {}
			
			#to format this data item, we loop over the non-data columns
			for i in range(0,num_nondatacolumns):
				#now we are iterating over the first n elements of this data item (non data description part)
				currentrow[self.column_names[i][0]] = line.pop(0).strip()
				
				if len(self.column_names[i]) > 1: #if the descriptor had more than one element for this column
					encoded_item = currentrow[self.column_names[i][0]]
					currentrow[self.column_names[i][0]] = self.column_names[i][int(encoded_item)]  #then set the title to this number
			
			temp_unit = ""
			temp_sign = ""
			for i in currentrow:
				if currentrow[i] in self.units:
					temp_unit = self.units[currentrow[i]]
				if currentrow[i] in self.signs:
					temp_sign = self.signs[currentrow[i]]
			
			currentrow['Units'] = temp_unit
			currentrow['Signs'] = temp_sign
			
			numeric_data =[]
			for n in line:
				#import as list of strings and strip whitespace
				numeric_data.append(n.strip())
			
			currentrow['Data'] = np.asarray(numeric_data, np.longdouble)
			
			self.dataset.append(currentrow)
		
		#strip out encoding information so column names are each one dimension
		temp = []
		for i in range(0,len(self.column_names)):
			temp.append(self.column_names[i][0])
		self.column_names = temp
		
		self.rehash()
		
	#end of construct_from_file
	
	def filter(self, filter_column, filter_string, keep=True):
		#will return a dataset that contains only the filter criteria if 'keep' is true. Will return the opposite if it is false.
		
		#temp class instance to return
		x = KinematicDataset()
		#note: we have to use copy() to get a value copy and not simply have both instances point to a single object
		x.column_names = self.column_names.copy()
		x.units = self.units.copy()
		x.signs = self.signs.copy()
		
		if keep == True:
			action = "Kept"
			for i in self.dataset:
				keep_element = 1
				if filter_column in i: #if the column to filter exists in this dataset element as a key...
					if i[filter_column] == filter_string: #check that key to see if it matches the filter
						x.dataset.append(i)
		else:
			action = "Removed"
			for i in self.dataset:
				keep_element = 1
				if filter_column in i: #if the column to filter exists in this data element as a key...
					if i[filter_column] != filter_string: #check that key to see if it DOES NOT match the filter
						x.dataset.append(i)
		
		#update the description
		newdesc = ": " + action + " where " + filter_column + " = " + filter_string + " "
		x.description = self.description + newdesc
		
		x.__update_units()
		
		return x
	#end filter
		
	def columns(self):
		return list(self.dataset[0].keys())
		
	def get_units(self, data_item_number):
		#Iterating a dictionary iterates over the keys.
		#this for loop should return the keys to the units dictionary one by one.
		for u in self.units:
			if u in self.dataset[data_item_number].values(): #checks to see if the KEY in units matches a VALUE in this dataset item
				return self.units[u]  #return the unit value to this key
		
		#This line will only run if the unit is not found.
		raise LookupError("Unit not configured correctly")
		
	def get_sign(self, data_item_number):
		#this is a very unique thing to python. iterating a dictionary iterates over the keys.
		#this for loop should return the keys to the signs dictionary one by one.
		for u in self.signs:
			if u in self.dataset[data_item_number].values(): #checks to see if this key exists in this dataset item
				return self.signs[u]  #return the sign value (what is positive) to this key
		
		raise LookupError("Sign not configured correctly")	
	
	def __update_units(self):
	#double underscore marks a method as private. cannot be accessed outside of another class method.
	#this method updates the units dictionary. After filtering, a particular motion may not exist anymore (for example a file with coronal plane rotation and anterior posterior translation, after filtering for AP, will no longer contain rotation)
	
	#get a list of conditions, and remove any that no longer are referenced. In self.units, conditions are keys (and units are values), but in self.dataset, the key is the column and the value is the condition.
	
		#this variable is a dictionary. They key is the unit, and the value is an int count of how many times it occurs in the dataset.
		count_conditions = {}
		
		cond = list(self.units.keys())
		
		for c in cond:
			count_conditions[c] = 0 #initialize the counter as an int
		
		#iterate over each element (which is a dictionary)
		for element in self.dataset:
			#iterate over each condition
			for i in cond:
				if i in element.values():   #if that condition exists in this element
				#note, numpy complains about this line since a numpy array is one of the values. It's OK though, we don't ever actually compare the numpy array.
					count_conditions[i] += 1
		
		items_to_delete = []
		
		for k in count_conditions:
			if count_conditions[k] == 0:
				items_to_delete.append(k)
		
		for j in items_to_delete:
			del self.units[j]
			
		#now do signs
		count_conditions = {}
		
		cond = list(self.signs.keys())
		
		for c in cond:
			count_conditions[c] = 0 #initialize the counter as an int
		
		#iterate over each element (which is a dictionary)
		for element in self.dataset:
			#iterate over each condition
			for i in cond:
				if i in element.values():   #if that condition exists in this element
					count_conditions[i] += 1
		
		items_to_delete = []
		
		for k in count_conditions:
			if count_conditions[k] == 0:
				items_to_delete.append(k)
		
		for j in items_to_delete:
			del self.signs[j]

	def __copy__(self):
		x = KinematicDataset()
		x.column_names = self.column_names.copy()
		x.units = self.units.deepcopy()
		x.signs = self.signs.deepcopy()
		
		for i in self.dataset:
			x.dataset.append(i)
					
		#update the description
		x.description = self.description
		return x

	def rehash(self):
		#hash each element in the dictionary so each has a unique ID that is consistent
		
		#Since the first time we run, there's no 'md5' key with the hash, after we run the hash would be different
		
		for element in self.dataset:
			hsh = str(hashlib.md5(str(element['Data']).encode()).hexdigest())
			element['md5'] = hsh
	
	def remove(self, hsh):
		to_remove = []
		
		for i in self.dataset:
			if i['md5'] == hsh:
				to_remove.append(i) #can't edit an iteratable while you're iterating
		
		for k in to_remove:
			self.dataset.remove(k)
			
	def retrieve(self, hsh):
		for i in self.dataset:
			if i['md5'] == hsh:
				return i
				
	def add_element(self, el):

		hsh = str(hashlib.md5(str(el['Data']).encode()).hexdigest())
		el['md5'] = hsh
		
		self.dataset.append(el)

	def convert_to_rad(self):
		#convert all degrees to radians
		for el in self.dataset:
			if el['Units'] == 'Degrees':
				el['Data'] = (el['Data'] * np.pi) / 180.00 
				el['Units'] = 'Radians'
		self.rehash()
	
	def convert_to_deg(self):
		#convert all radians to degrees
		for el in self.dataset:
			if el['Units'] == 'Radians':
				el['Data'] = (el['Data'] * 180.00) / np.pi 
				el['Units'] = 'Degrees'
		self.rehash()
		

		
	