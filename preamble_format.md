#Preamble Format

##What is the preamble?
The preamble is a section at the beginning of a CSV dataset that defines the information in the dataset. It defines the names of each point of data, the units, and the sign convention.

##Format of the preamble
A preamble has four sections

Section | Name and Description | Number of lines 
------ | ------ | ------ | ------
1 | Preamble Tag and Dataset Description | 1 
2 | Number of Non-Data Columns in Dataset | 1
3 | Column Names | Number of lines should match the value of section 2
4 | Units | 1
5 | Sign | 1

###Section 1
Section 1 is a single line with the following format:

'''[preamble],DatasetDescription'''

