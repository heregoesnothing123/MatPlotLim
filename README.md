# MatPlotLim
A Program to plot kinematic data.

## Sections of this document
- [Preamble Format](#preamble-format)
- List of Important Classes and Their Methods
  - [KinematicDataset](#kinematicdataset)

## Current work
Nate: Working on adding total rotational distance

# List of important classes and their methods

## KinematicDataset

### Instance Variables

Instance Variable | Description | Format
------ | ------ | ------
dataset | Main data | A list of dictionaries. Each dictionary contains a line from the CSV file. The keys are set by the [preamble](#preamble-format), with one key, `Data`, having a value of a list which is the non-descriptive data from the row. 
column_names | The name of non-data columns | A list containing the titles of the columns which contain descriptive data. Can be used to find out what properties are available for filtering.
description | Description of this dataset | This is a string with the description of this dataset
Units | Units in this dataset | A dictionary containing a key of a condition, and the value being the unit of an element if this key is in the dataset
Signs | Sign convention | A dictionary containing a key of a condition, and the direction that is defined as being positive

Instance variable examples using an instance named `example`: 

Description | Example
----- | -----
Getting number of rows (data elements) in the dataset | `len(example.dataset)`
Get the number of data points in the raw data of element 35 | `len(example.dataset[35]['Data'])`
Print string describing the dataset | `print(example.description)`
List all of the units in the dataset | `print(example.units)`

### Class Methods

Method | Description | Arguments (in order) | Return
----- | ----- | ----- | -----
construct_from_file | Processes CSV file into KinematicDataset class | `filename` is required. `directory` is assumed to be `c:\kinematicdata` unless specified | No return
filter | Keeps all dataset elements which match the filtering criteria | `filter_column` is required. A string describing the column for which a condition must be met. `filter_string` is required. A string containing the values that must be met in the column provided in the previous argument. | Returns a new KinematicDataset object. Updates description reflecting filtering.
remove | Identical to `filter` method, but removes matching filtering criteria | Same arguments as `filter` | Same return as `filter` but excluding matching elements
columns | Returns list of columns. Each column is a key which can be used to retrieve data in the element's dictionary. Useful for filtering | None | Python list of columns
get_units | Returns the units of a particular element | Integer describing which element for which to return units (0 to n-1) | Returns a string of the units for that element.
get_units | Returns the direction for which a motion is positive of a particular element | Integer describing which element for which to return the sign convention (0 to n-1) | Returns a string describing what motion is positive for that element.


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
### Section 5: Signs
The signs section defines the sign convention that a data element uses. It lists what is considered positive. Formatting is very similar to Section 4. 
