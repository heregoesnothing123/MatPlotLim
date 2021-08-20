#File handling for the Kinematic Data

#Kinematic data files should have a "preamble" before the csv data, showing the structure of the data
#Structure of the preamble:
#1st line should be "[preamble]"
#2nd line should be the number of non-data columns
#The next n lines of the file should be the description of each non-data column, where n is the number in the 2nd line
#Format for non-data column description in the preamble:
#Descriptive name, Condition if this column is "1", Condition if this column is "2", etc (for encoded data).
#If no comma is in the non-data column description, the descriptive name is the only thing recorded and no conditions are replaced.

class KinematicDataset:

	def __init__(self):
		self.data = []
		#the instance variable "data" is a list of dictionaries
		#dictionaries are defined by the preamble of the raw data
		#Each non-data column will have a dictionary entry
		self.column_names = []
		self.description = ""
	
	def construct_from_file(self, filename, directory="C:\kinematicdata"):
	
		#first, check for preamble to the data defining its formatting (see data preamble section)
		
		file = directory+'\\'+filename
		
		f = open(file,'r',encoding='utf-8-sig')
		
		firstline = f.readline().split(',')
		
		if firstline[0].strip() != "[preamble]":
			raise NameError('File is not in correct format. No preamble found')
		else if len(firstline) > 1:
			self.description = firstline[1].strip()
			
		num_nondatacolumns = int(f.readline())
		
		for i in range(0,num_nondatacolumns):
			self.column_names.append(f.readline().strip().split(','))
			
		#now we have set up names and the file pointer is at the first data
		
		run = True
		
		while run:
			line = f.readline().split(',')
			if line == [""]:
				break
			
			currentrow = {}
			
			for i in range(0,num_nondatacolumns):
				currentrow[self.column_names[i][0]] = line.pop(0).strip()
				
				#this is wizard algorithm
				if len(self.column_names[i]) > 1: #if the descriptor had more than one element for this column
					currentrow[self.column_names[i][0]] = self.column_names[i][int(currentrow[self.column_names[i][0]])]  #then set the title to this number
					
			numeric_data =[]
			for n in line:
				numeric_data.append(float(n.strip()))
				
			currentrow['data'] = numeric_data
			
			self.data.append(currentrow)
			
		temp = []
		for i in range(0,len(self.column_names)):
			temp.append(self.column_names[i][0])
		self.column_names = temp
		
	#end of __init__
	
	def filter(self, filter_column, filter_string):
		#will return a dataset that contains only the filter criteria
		
		if self.data == []:
			raise ValueError('KinematicDataset instance has not been created yet!')
			
		if not isinstance(filter_column, list):
			filter_column = [filter_column]
		if not isinstance(filter_string, list):
			filter_string = [filter_string]
		
		if len(filter_column) != len(filter_string):
			raise ValueError('Dimensions of filter call do not match')
		
		x = KinematicDataset()
		
		for i in self.data:
			keep_element = 1
			for j in filter_column:
				k = self.column_names.index(j)
				if i['Condition'][k] == filter_string[filter_column.index(j)]:
					keep_element *= 1
				else:
					keep_element *= 0
		
			if keep_element == 1:
				x.data.append(i)
		
		return x
		
	def columns(self):
		return self.data[0].keys()
		
	def num_datapoints(self):
		return len(self.data)
						
