#File handling for the Kinematic Data

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
					currentrow[self.column_names[i][0]] = self.column_names[i][int(currentrow[self.column_names[i][0]])]  #then set the title to this number
			
			numeric_data =[]
			for n in line:
				numeric_data.append(float(n.strip()))
				
			currentrow['Data'] = numeric_data
			
			self.dataset.append(currentrow)
			
		#strip out encoding information so column names are each one dimension
		temp = []
		for i in range(0,len(self.column_names)):
			temp.append(self.column_names[i][0])
		self.column_names = temp
		
	#end of construct_from_file
	
	def filter(self, filter_column, filter_string):
		#will return a dataset that contains only the filter criteria
		
		#temp class instance to return
		x = KinematicDataset()
		#note: we have to use copy() to get a value copy and not simply have both instances point to a single object
		x.column_names = self.column_names.copy()
		x.units = self.units.copy()
		x.signs = self.signs.copy()
		
		for i in self.dataset:
			keep_element = 1
			if filter_column in i: #if the column to filter exists in this dataset element as a key...
				if i[filter_column] == filter_string: #check that key to see if it matches the filter
					x.dataset.append(i)
		
		#update the description
		newdesc = ": Filtered where " + filter_column + " = " + filter_string + " "
		x.description = self.description + newdesc
		
		x.__update_units()
		
		return x
	#end filter
		
	def remove(self, filter_column, filter_string):
		#will return a dataset that removes the filter criteria
		
		#temp class instance to return
		x = KinematicDataset()
		x.column_names = self.column_names[:]
		x.units = self.units.deepcopy()
		x.signs = self.signs.deepcopy()
		
		for i in self.dataset:
			keep_element = 1
			if filter_column in i: #if the column to filter exists in this data element as a key...
				if i[filter_column] != filter_string: #check that key to see if it DOES NOT match the filter
					x.dataset.append(i)
					
		#update the description
		newdesc = ": Removed elements where " + filter_column + " = " + filter_string + " "
		x.description = self.description + newdesc
		
		x.__update_units()
		
		return x
	#end remove
		
	def columns(self):
		return list(self.dataset[0].keys())
		
	def get_units(self, data_item_number):
		#this is a very unique thing to python. iterating a dictionary iterates over the keys.
		#this for loop should return the keys to the units dictionary one by one.
		for u in self.units:
			if u in self.dataset[data_item_number].values(): #checks to see if the KEY in units matches a VALUE in this dataset item
				return self.units[u]  #return the unit value to this key
		
		#These lines will only return if the unit is not found. Print statement for debugging.
		print("Unit not found. Units in class: " + str(self.units) + " and keys to dataset item are: " + str(list(self.dataset[data_item_number].keys())))
		raise LookupError("Units not configured correctly")
		
	def get_sign(self, data_item_number):
		#this is a very unique thing to python. iterating a dictionary iterates over the keys.
		#this for loop should return the keys to the signs dictionary one by one.
		for u in self.signs:
			if u in self.dataset[data_item_number].values(): #checks to see if this key exists in this dataset item
				return self.signs[u]  #return the sign value (what is positive) to this key
		
		#These lines will only return if the unit is not found. Print statement for debugging.
		print("Sign not found. Signs in class: " + str(self.signs) + " and keys to dataset item are: " + str(list(self.dataset[data_item_number].keys())))
		raise LookupError("Signs not configured correctly")	
	
	def __update_units(self):
	#double underscore marks a method as private. cannot be accessed outside of another class method.
	#this method updates the units dictionary. After filtering, a particular motion may not exist anymore (for example a file with coronal plane rotation and anterior posterior translation, after filtering for AP, will no longer contain rotation)
	
	#get a list of conditions, and remove any that no longer are referenced. In self.units, conditions are keys (and units are values), but in self.dataset, the key is the column and the value is the condition.
	
		count_conditions = {}
		
		cond = list(self.units.keys())
		
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
