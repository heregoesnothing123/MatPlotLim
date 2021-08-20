# Preamble Format

## What is the preamble?
The preamble is a section at the beginning of a CSV dataset that defines the information in the dataset. It defines the names of each point of data, the units, and the sign convention.

## Format of the preamble
A preamble has four sections

Section | Name and Description | Number of lines 
------ | ------ | ------
1 | Preamble Tag and Dataset Description | 1 
2 | Number of Non-Data Columns in Dataset | 1
3 | Column Names | Number of lines should match the value of section 2
4 | Units | 1
5 | Sign | 1

### Section 1: Preamble Tag and Dataset Description
Section 1 is a single line with the following format:

 `[preamble],DatasetDescription`

The first part is the text `[preamble]` to let the program know that this data is formatted correctly. After the comma is the description of the dataset. It can take on any UTF-8 character with the exception of a comma.

*Note: The file is read with Python's `'UTF-8-Sig'` Text parser to handle Byte Order Mark text files.*

### Section 2: Number of non-data columns in dataset
Section 2 is a single line describing the number of columns that do not contain data, but contain information about the data (such as motion, specimen ID, condition, etc). The line should be a number which can be parsed as an integer in Python. It defines how many of the column name lines follow this one.

### Section 3: Column names
Section 3 is variable number of lines, defined by Section 2. It can be one of two formats:

* Format 1: Simple column name
	* Column Name: A string describing the name of this column (first line of section 3 describes first column, second line describes second column, etc). The string cannot contain a comma. The name of this string will be used to search and filter later, so a simpler column name is better.
* Format 2: Column name with encoded data
	* List: A comma seperated list for an encoded column. The first item in the list is the Column Name (the same as format 1), followed by a comma, then an ordered list, also ordered by a comma. The first item after the column name is the name that the data in this column should be converted to for filtering and searching if the value is "1", the second item if the value is "2", etc. See special section below for formatting. Currently only supports simple ordered numbers as encoding. This can be changed in the future as needed.
	
#### Example of column name with encoded data
Consider a dataset where the fifth column contains either a "1" or a "2", where "1" means control condition and "2" means experimental condition. The desired name to search and filter this column is "Condition". As this is the fifth column, the statement should be on the fifth Section 3 line (seventh line in the preamble as lines 1 and 2 are sections 1 and 2) and appear as:

`Condition,Control,Experimental`

This will name the column as "Condition" and where a data item contains "1" in column 5, it will be renamed to "Control", in this dataset. If the data in column five for this item is "2", it will be renamed "Experimental".

### Section 4: Units
The units section is a single line with comma seperated values. The first element is the string `units`, followed by the column name from section 3 which distinguishes which column can be used to determine the units of this data item, followed by a comma. The following elements describe, in order, the units if the value of this column are "1", "2", "3", etc. An example is below.

#### Example of unit encoding
Consider a dataset where the sixth column, named "Motion", describes which type of motion exists. Data items that contain "1" in this column are Sagittal plane rotation in degree. "2" Denotes Coronal plane rotation, "3" denotes Anterior / Posterior translation in millimeters. An example Section 3 column name line followed by a unit line would appear as:

```
Line 8              : Motion,Sagittal,Coronal,AP
...
Second to last line : Units,Motion,Degree,Degree,mm
```
