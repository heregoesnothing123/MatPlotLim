import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from kinematicdataset import *
from element_math import *
from datetime import datetime


class MatPlotLim:

	def __init__(self, master):
		self.master = master
		self.master.title("MatPlotLim")
		self.master.state('zoomed')
		
		self.dset = KinematicDataset()
		
		self.h = self.master.winfo_height()
		self.w = self.master.winfo_width()
		
		self.graph_frame = tk.Frame(self.master)
		self.graph_frame.place(relx=0.4, rely=0.05, relheight=0.95, relwidth=0.6)
		
		self._set_chart_defaults()

		spacing = 37
		yind = 10

		self.select_data_btn = tk.Button(self.master, text = "Select Data", command = self.data_select)
		self.select_data_btn.place(x=77, y=yind)
		self.select_data_btn.pack

		self.select_data2_btn = tk.Button(self.master, text = "Select Secondary Data", command = self.placeholder)
		self.select_data2_btn.place(x=177, y=yind)
		self.select_data2_btn.pack

		#y index to align features
		yind += spacing
		#the button to launch the data import window. It needs to be disabled until a datafile is loaded.
		self.data_config_btn = tk.Button(self.master, text = "Configure Dataset", command = self.data_window)
		self.data_config_btn.place(x=77, y=yind)
		self.data_config_btn.configure(state='disabled')

		yind += spacing
		#the button to launch the graph setup window. It needs to be disabled until a datafile is loaded.
		self.graph_config_btn = tk.Button(self.master, text = "Configure Graph", command = self.graph_window)
		self.graph_config_btn.place(x=77, y=yind)
		self.graph_config_btn.configure(state='disabled')

		yind += spacing
		self.plot_btn = tk.Button(self.master, text = "Plot", command = self.plot_data)
		self.plot_btn.place(x=77, y=yind)
		self.plot_btn.pack

		yind += spacing
		self.lbl_title = tk.Label(self.master,text = "Chart Title:")
		self.lbl_title.place(x = 7, y=yind)

		self.txt_title = tk.Text(self.master, height = 1, width = 24, )
		self.txt_title.insert(tk.END,"Chart Title")
		self.txt_title.place(x=77, y=yind)

		yind += spacing
		self.lbl_xaxis = tk.Label(self.master,text = "X Axis Text:")
		self.lbl_xaxis.place(x = 7, y=yind)

		self.txt_xaxis = tk.Text(self.master, height = 1, width = 24 )
		self.txt_xaxis.insert(tk.END,"X Axis")
		self.txt_xaxis.place(x=77, y=yind)

		yind += spacing
		self.lbl_yaxis = tk.Label(self.master,text = "Y Axis Text:")
		self.lbl_yaxis.place(x = 7, y=yind)

		self.txt_yaxis = tk.Text(self.master, height = 1, width = 24)
		self.txt_yaxis.insert(tk.END,"Y axis")
		self.txt_yaxis.place(x=77, y=yind)

		yind += spacing
		self.lbl_ymaxmin = tk.Label(self.master,text = "Y max,min")
		self.lbl_ymaxmin.place(x = 7, y=yind)

		self.txt_ymaxmin = tk.Text(self.master, height = 1, width = 24, )
		self.txt_ymaxmin.insert(tk.END,"")
		self.txt_ymaxmin.place(x=77, y=yind)

		yind += spacing
		self.lbl_xmaxmin = tk.Label(self.master,text = "X max,min")
		self.lbl_xmaxmin.place(x = 7, y=yind)

		self.txt_xmaxmin = tk.Text(self.master, height = 1, width = 24, )
		self.txt_xmaxmin.insert(tk.END,"")
		self.txt_xmaxmin.place(x=77, y=yind)

		yind += spacing
		self.UpdateGraph = tk.Button(self.master, text = "Update Graph Titles", command = self.update_graph)
		self.UpdateGraph.place(x=77, y=yind)

		yind += spacing
		self.numeric_xform_btn = tk.Button(self.master, text = "Transform Data", command = self.xform_data_window)
		self.numeric_xform_btn.place(x=77, y=yind)

		yind += spacing
		self.export_all_e_btn = tk.Button(self.master, text = "Export element set", command = self.export_elements)
		self.export_all_e_btn.place(x=77, y=yind)

		yind += spacing
		self.export_plot_e_btn = tk.Button(self.master, text = "Export plotted element set", command = self.export_plot_elements)
		self.export_plot_e_btn.place(x=77, y=yind)

		self.data_w = None
		self.graph_w = None
		self.xform_w = None
		self.selected_elements=[]

		self.color_index = 0

		
	def placeholder(self):
		#do nothing!
		pass
	
	def update_graph(self):
		input = self.txt_title.get("1.0","end-1c")
		self.plot1.set_title(input)
		input = self.txt_xaxis.get("1.0","end-1c")
		self.plot1.set_xlabel(input)
		input = self.txt_yaxis.get("1.0","end-1c")
		self.plot1.set_ylabel(input)

		self.update_graph_range()

		self.fig.canvas.draw()
		
	def data_select(self):
		fn = fd.askopenfilename(initialdir='C:\kinematicdata')
		#tk.messagebox.showinfo("Debug",fn)

		if fn == '':
			return "blank"

		self.dset.construct_from_file(fn)

		#using dictionaries are great. We can add keys on the fly
		for e in self.dset.dataset:
			e['Color'] = "None"
			e['Formatting'] = self.default_graph_properties
			
		self.data_config_btn.configure(state='normal')
		self.graph_config_btn.configure(state='normal')
		
	def data_window(self):

		dat = self.dset.description

		#we don't want to launch a new window if one exists
		if self.data_w == None:
			#the y-padding for this window
			pdy = 2
		
			self.data_w = tk.Toplevel(self.master)
			self.data_w.protocol("WM_DELETE_WINDOW", self.data_win_close)
			self.txt_desc_w = tk.Text(self.data_w, height = 2, width = 40 )
			self.txt_desc_w.insert(tk.END,dat)
			self.txt_desc_w.grid(row=0, column = 1, columnspan = 3, sticky = tk.W + tk.E, pady = pdy)
			
			lab1 = tk.Label(self.data_w, text = "Data Description")
			
			lab1.grid(row=0, column = 0, columnspan = 1, sticky = tk.W, pady = pdy)
			
			self.filter_btn_w = tk.Button(self.data_w, text = "Filter Data", command = self.filter_data)
			self.filter_btn_w.grid(row=1, column = 0, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)
			
			self.remove_btn_w = tk.Button(self.data_w, text = "Remove Data", command = self.remove_data)
			self.remove_btn_w.grid(row=1, column = 1, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)
			
			self.txt_filter_column_w = tk.Text(self.data_w, height = 1)
			self.txt_filter_column_w.insert(tk.END,"Filter Column")
			self.txt_filter_column_w.bind("<Tab>",self.focus_next)
			self.txt_filter_column_w.grid(row=1, column = 2, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)
			
			self.txt_filter_text_w = tk.Text(self.data_w, height = 1)
			self.txt_filter_text_w.insert(tk.END,"Filter Text")
			self.txt_filter_column_w.bind("<Tab>",self.focus_next)
			self.txt_filter_text_w.grid(row=1, column = 3, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)

			self.fast_filter_btn_w = tk.Button(self.data_w, text = "Tibia/Talus Fast", command = self.fast_filter)
			self.fast_filter_btn_w.grid(row=1, column = 4, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)

			self.draw_datatree()
			
		else:
			pass
	
	def filter_data(self):
		#gets the first line of the text box, omitting the final newline
		fc = self.txt_filter_column_w.get("1.0",'end-1c')
		ft = self.txt_filter_text_w.get("1.0",'end-1c')
		
		if fc == "Filter Column":
			pass
		else:
			self.dset = self.dset.filter(fc,ft)
			self.txt_desc_w.update()
			self.draw_datatree()
		
	def fast_filter(self):
		#gets the first line of the text box, omitting the final newline
		self.dset = self.dset.filter("ParentSegment","Tibia")
		self.dset = self.dset.filter("ChildSegment","Talus")
		self.txt_desc_w.update()
		self.draw_datatree()
	
	def remove_data(self):
		#gets the first line of the text box, omitting the final newline
		fc = self.txt_filter_column_w.get("1.0",'end-1c')
		ft = self.txt_filter_text_w.get("1.0",'end-1c')
		
		if fc == "Filter Column":
			pass
		else:
			self.dset = self.dset.filter(fc,ft,keep=False)
			self.txt_desc_w.update()
			self.draw_datatree()

	def export_elements(self):
		current_datetime = datetime.now()
		formatted_datetime = current_datetime.strftime(r'%d%b%y%H%M%S') + ".txt"
		f = open(formatted_datetime,'a')
		for e in self.dset.dataset:
			f.write(str(e) + "\n")

	def export_plot_elements(self):
		current_datetime = datetime.now()
		formatted_datetime = current_datetime.strftime(r'%d%b%y%H%M%S') + ".txt"
		f = open(formatted_datetime,'a')
		for e in self.dset.dataset:
			if e['Color'] != 'None':
				f.write(str(e) + "\n")
		
	def draw_datatree(self):
			treecol = []
			
			for i in self.dset.columns():
				if i != 'md5' and i != 'Data' and i!= 'Color' and i!= 'Formatting':
					treecol.append(i)
				
			self.tree = ttk.Treeview(self.data_w, columns = treecol, show='headings', height = 30)
			
			for k in treecol:
				self.tree.column(k, width=80)
			
			for c in treecol:
				self.tree.heading(c, text=c)
			
			for e in self.dset.dataset:
				emod = list(e.values())
				self.tree.insert('',tk.END,values=emod,iid=e['md5'])
				
			self.tree.grid(row=2, column = 0, columnspan = 5, sticky = 'nsew', pady = 2)
			
			treescrl = tk.Scrollbar(self.data_w, orient=tk.VERTICAL, command=self.tree.yview)
			self.tree.configure(yscroll=treescrl.set)
			treescrl.grid(row=2, column=5, sticky='ns')
	
	#if we close a window, the class still contains the window state. I don't know how to reshow the window, so instead we'll destroy the window so we can launch it again.
	def data_win_close(self):
		self.data_w.destroy()
		self.data_w = None
		
	def graph_win_close(self):
		self.graph_w.destroy()
		self.graph_w = None

	def xform_win_close(self):
		self.xform_w.destroy()
		self.xform_w = None
		
	def plot_data(self):
		run = True
		#clear the old graph
		while run:
			x=1
			try:
				ln = self.lineplot.pop(0)
				ln.remove()
			except IndexError:
				pass
			except TypeError:
				pass

			if len(self.lineplot) == 0:
				run = False
	
		num_elem = 0
		#plot the new graph
		for el in self.dset.dataset:
			#print(el)
			#we only want to plot elements who's color values are not "None"
			col = el['Color']
			if col != "None":
				self.graph_range.append(get_range(self.dset, el['md5']))
				if num_elem < el['Data'].size:
					num_elem = el['Data'].size
				self.lineplot.append(self.plot1.plot(el['Data'], color=col, **self.default_graph_properties))

		tempmax = self.graph_range[0][0]
		tempmin = self.graph_range[0][1]

		if len(self.graph_range) > 1:
			for i in self.graph_range:
				if tempmax < i[0]:
					tempmax = i[0]
				if tempmin > i[1]:
					tempmin = i[1]
		
		self.ax_rect = [0.0, tempmin, num_elem, tempmax]

		self.update_graph_range(self.ax_rect)

		self.canvas.draw()
		
	def focus_next(self, event, **kwargs):
		#this makes tab move to the next text field. Yes, it's that important to me.
		event.widget.tk_focusNext().focus()
		return("break")

	def update_graph_range(self, newrange=[]):
		#this will check and see if the axes ranges are set. If they are not they will be set to auto range.
		#newrange is a rectangle with the desired new range. [xmin, ymin, xmax, ymax]

		input = str(self.txt_ymaxmin.get("1.0","end-1c"))

		if input == "" and newrange != []:
			new_ymin = round(newrange[1]*1.05,5)
			new_ymax = round(newrange[3]*1.05,5)
			string = str(new_ymin) + "," + str(new_ymax)
			self.txt_ymaxmin.insert(1.0,string)
		else:
			input = input.split(",")
			new_ymin = float(input[0].strip())
			new_ymax = float(input[1].strip())

		self.graphaxes_y = self.plot1.set_ylim(new_ymin, new_ymax)

		input = str(self.txt_xmaxmin.get("1.0","end-1c"))
		if input == "" and newrange != []:
			new_xmin = round(newrange[0],5)
			new_xmax = round(newrange[2],5)
			string = str(new_xmin) + "," + str(new_xmax)
			self.txt_xmaxmin.insert(1.0,string)
		else:
			input = input.split(",")
			new_xmin = float(input[0].strip())
			new_xmax = float(input[1].strip())

		self.graphaxes_x = self.plot1.set_xlim(new_xmin, new_xmax)

		
	def graph_window(self):

		dat = self.dset.description

		#we don't want to launch a new window if one exists
		if self.graph_w == None:
		
			#the y-padding for this window
			pdy = 2
		
			self.graph_w = tk.Toplevel(self.master)
			self.graph_w.protocol("WM_DELETE_WINDOW", self.graph_win_close)
			self.g_txt_desc_w = tk.Text(self.graph_w, height = 2, width = 80 )
			self.g_txt_desc_w.insert(tk.END,dat)
			
			self.g_txt_desc_w.grid(row=0, column = 1, columnspan = 3, sticky = tk.W + tk.E, pady = pdy)
			
			lab1 = tk.Label(self.graph_w, text = "Data Description")
			
			lab1.grid(row=0, column = 0, columnspan = 1, sticky = tk.W, pady = pdy)
			
			self.addgroup_btn_w = tk.Button(self.graph_w, text = "Add Element to Plot", command = self.add_element_to_plotlist)
			self.addgroup_btn_w.grid(row=1, column = 0, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)
			
			self.graph_color_options = tk.StringVar(self.graph_w)
			self.color_options = ["Red", "Green", "Blue", "Black", "Yellow", "Orange", "Purple", "Grey", "Pink"]
			self.graph_color_options.set(self.color_options[self.color_index])
			self.color_select = tk.OptionMenu(self.graph_w, self.graph_color_options, *self.color_options)
			self.color_select.grid(row=1, column = 1, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)

			self.graph_line_options = tk.StringVar(self.graph_w)
			self.line_options = ["solid", "dashed", "dashdot", "dotted"]
			self.graph_line_options.set(self.line_options[0])
			self.line_select = tk.OptionMenu(self.graph_w, self.graph_line_options, *self.line_options)
			self.line_select.grid(row=1, column = 2, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)
			
			self.remgroup_btn_w = tk.Button(self.graph_w, text = "Remove Element from Plot", command = self.rem_element_from_plotlist)
			self.remgroup_btn_w.grid(row=1, column = 3, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)

			#this creates the data tree self.tree. Function for updating
			self.draw_graphtree()
			
		else:
			#this doesn't really work
			#self.data_w.show()
			pass
		
	def draw_graphtree(self):
			treecol = []
			
			for i in self.dset.columns():
				if i != 'md5' and i != 'Data':
					treecol.append(i)

			#tk.messagebox.showinfo("Debug",treecol)
			self.graphtree = ttk.Treeview(self.graph_w, columns = treecol, show='headings', height = 30)
			
			for k in treecol:
				if k != 'Formatting':
					self.graphtree.column(k, width=60)
				else:
					self.graphtree.column(k, width=160)
			
			for c in treecol:
				self.graphtree.heading(c, text=c)
			
			for e in self.dset.dataset:
				emod = []
				for c in treecol:
					emod.append(e[c])
				self.graphtree.insert('',tk.END,values=emod, iid=e['md5'])
				if e['Color'] != "None":
					self.graphtree.item(e['md5'],tag='plotted')

			self.graphtree.tag_configure('plotted',background='#B5DAFE')
				
			self.graphtree.grid(row=2, column = 0, columnspan = 5,sticky = 'nsew', pady = 2)
			
			treescrl = tk.Scrollbar(self.graph_w, orient=tk.VERTICAL, command=self.graphtree.yview)
			self.graphtree.configure(yscroll=treescrl.set)
			treescrl.grid(row=2, column=5, sticky='ns')

			self.graph_color_options.set(self.color_options[self.color_index])
			#next time a different default color! Magic!
			self.color_index += 1

	def add_element_to_plotlist(self):
		
		for i in self.graphtree.selection():
			#print(i)
			self.selected_elements.append(i)
			element = self.dset.retrieve(i)
			element['Color'] = self.graph_color_options.get()
			#print(element)
			self.dset.element_remove(i)
			self.dset.add_element(element)
		self.draw_graphtree()
	
	def rem_element_from_plotlist(self):
		
		for i in self.graphtree.selection():
			#print(i)
			if i in self.selected_elements:
				self.selected_elements.remove(i)
			element = self.dset.retrieve(i)
			element['Color'] = 'None'
			#print(element)
			self.dset.element_remove(i)
			self.dset.add_element(element)
		self.draw_graphtree()

	def setup_textbox(self, txtbox):
		pass

	def average_data(self):
		x = 1
		b = 2
		c = 3

		average_dataset(self.dset)

	def _total_rotation(self):
		x=1
		self.dset.convert_to_rad()
		get_total_rotation(self.dset)

	def xform_data_window(self):

		dat = self.dset.description

		#we don't want to launch a new window if one exists
		if self.xform_w == None:
			#the y-padding for this window
			pdy = 2
		
			self.xform_w = tk.Toplevel(self.master)
			self.xform_w.protocol("WM_DELETE_WINDOW", self.xform_win_close)

			self.txt_xform_w = tk.Text(self.xform_w, height = 2, width = 60 )
			self.txt_xform_w.insert(tk.END,dat)
			self.txt_xform_w.grid(row=0, column = 1, columnspan = 3, sticky = tk.W + tk.E, pady = pdy)
			
			lab1 = tk.Label(self.xform_w, text = "Data Description")
			lab1.grid(row=0, column = 0, columnspan = 1, sticky = tk.W, pady = pdy)
			
			self.average_btn_w = tk.Button(self.xform_w, text = "Average Data", command = self.average_data)
			self.average_btn_w.grid(row=1, column = 0, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)

			self.tr_btn_w = tk.Button(self.xform_w, text = "Transform to total rotation", command = self._total_rotation)
			self.tr_btn_w.grid(row=1, column = 1, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)

	def _set_chart_defaults(self):
		self.fig = Figure(figsize=(11,10))
		
		#placeholder plot
		y = [i ** 2 for i in range(30)]

		self.plot1 = self.fig.add_subplot(111)
		self.lineplot = self.plot1.plot(y)
		
		self.charttitle = "Chart Title"
		self.xlabel = "X Label"
		self.ylabel = "Y Label"
		
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		self.toolbar.update()
		self.canvas.get_tk_widget().pack()
		self.default_graph_properties = {}
		self.default_graph_properties['linestyle'] = 'solid'
		self.default_graph_properties['linewidth'] = 3
		self.graph_range = []
		self.ax_rect = []


