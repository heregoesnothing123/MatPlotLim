import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from kinematicdataset import *
from element_math import *


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
		
		self.fig = Figure(figsize=(11,10))
		
		#placeholder plot
		y = [i ** 2 for i in range(30)]

		self.plot1 = self.fig.add_subplot(111)
		#self.fig.add_axes()
		self.lineplot = self.plot1.plot(y)
		
		self.charttitle = "Chart Title"
		self.xlabel = "X Label"
		self.ylabel = "Y Label"
		
		self.plot1.set_title(self.charttitle)
		self.plot1.set_ylabel(self.xlabel)
		self.plot1.set_xlabel(self.ylabel)
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		self.toolbar.update()
		self.canvas.get_tk_widget().pack()
		
		self.b0 = tk.Button(self.master, text = "Select Data", command = self.data_select)
		self.b0.place(x=7, y=10)

		self.b1 = tk.Button(self.master, text = "Plot", command = self.plot_data)
		self.b1.place(x=87, y=10)

		self.b2 = tk.Button(self.master, text = "Translate", command = self.placeholder)
		self.b2.place(x=7, y=40)

		#inputs for translation
		yloc = 70
		
		self.Var11 = tk.Text(self.master, height = 2, width = 4)
		self.Var11.place(x=37, y=70)

		self.Var12 = tk.Text(self.master, height = 2, width = 4)
		self.Var12.place(x=37, y=120)

		self.Var13 = tk.Text(self.master, height = 2, width = 4)
		self.Var13.place(x=37, y=170)

		self.txt_title = tk.Text(self.master, height = 2, width = 24, )
		self.txt_title.insert(tk.END,"Chart Title")
		self.txt_title.place(x=77, y=227)

		self.txt_xaxis = tk.Text(self.master, height = 2, width = 24 )
		self.txt_xaxis.insert(tk.END,"X Axis")
		self.txt_xaxis.place(x=77, y=277)

		self.txt_yaxis = tk.Text(self.master, height = 2, width = 24)
		self.txt_yaxis.insert(tk.END,"Y axis")
		self.txt_yaxis.place(x=77, y=327)
		
		self.UpdateGraph = tk.Button(self.master, text = "Update Graph", command = self.update_graph)
		self.UpdateGraph.place(x=77, y=377)
		
		#the button to launch the data import window. It needs to be disabled until a datafile is loaded.
		self.data_config_btn = tk.Button(self.master, text = "Configure Dataset", command = self.data_window)
		self.data_config_btn.place(x=77, y=427)
		self.data_config_btn.configure(state='disabled')
		
		#the button to launch the graph setup window. It needs to be disabled until a datafile is loaded.
		self.graph_config_btn = tk.Button(self.master, text = "Configure Graph", command = self.graph_window)
		self.graph_config_btn.place(x=77, y=477)
		self.graph_config_btn.configure(state='disabled')
				
		#input theta for rotation

		self.Theta = tk.Text(self.master, height = 2, width = 4)
		self.Theta.place(x=187, y=70)

		#dropdown menus

		self.tkvar = tk.StringVar(self.master)
		options = ["Rotate About X", "Rotate About Y", "Rotate About Z"]
		self.tkvar.set("Click to select Rotation")

		self.popupMenu = tk.OptionMenu(self.master, self.tkvar, *options)
		self.popupMenu.place(x=137, y = 39)

		self.lbl_theta = tk.Label(self.master,text = "Tx:")
		self.lbl_theta.place(x = 7, y=77)

		self.lbl_theta = tk.Label(self.master,text = "Ty:")
		self.lbl_theta.place(x = 7, y=127)

		self.lbl_theta = tk.Label(self.master,text = "Tz:")
		self.lbl_theta.place(x = 7, y=177)

		self.lbl_theta = tk.Label(self.master,text = "Theta:")
		self.lbl_theta.place(x = 137, y=77)

		self.lbl_title = tk.Label(self.master,text = "Chart Title:")
		self.lbl_title.place(x = 7, y=232)

		self.lbl_xaxis = tk.Label(self.master,text = "X Axis Text:")
		self.lbl_xaxis.place(x = 7, y=282)

		self.lbl_yaxis = tk.Label(self.master,text = "Y Axis Text:")
		self.lbl_yaxis.place(x = 7, y=332)

		self.b0.pack
		self.b1.pack
		self.b2.pack
		self.Var11.pack
		self.Var12.pack
		self.Var13.pack
		
		self.data_w = None
		self.graph_w = None
		
		self.selected_elements=[]

		self.default_graph_properties = {}
		#self.default_graph_properties['marker'] = 'o'
		self.default_graph_properties['linestyle'] = 'solid'
		self.default_graph_properties['linewidth'] = 3
		#self.default_graph_properties['markersize'] = 12

		self.color_index = 0
		self.graph_range = []
		self.ax_rect = []
		
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
		self.fig.canvas.draw()
		
	def data_select(self):
		fn = fd.askopenfilename(initialdir='C:\kinematicdata')
		#tk.messagebox.showinfo("Debug",fn)
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
			#self.data_w.geometry("600x200")
			self.txt_desc_w = tk.Text(self.data_w, height = 2, width = 60 )
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
			
			#this creates the data tree self.tree. Function for updating
			self.draw_datatree()
			
		else:
			#this doesn't really work
			#self.data_w.show()
			pass
	
	def filter_data(self):
		#gets the first line of the text box, omitting the final newline
		fc = self.txt_filter_column_w.get("1.0",'end-1c')
		ft = self.txt_filter_text_w.get("1.0",'end-1c')
		
		print(fc + ft)
	
		if fc == "Filter Column":
			pass
		else:
			
			self.dset = self.dset.filter(fc,ft)
			self.txt_desc_w.update()
			self.draw_datatree()
			#self.tree.update()
			#self.data_w.update()
		#do nothing yet!
		pass
		
	def remove_data(self):
		#do nothing yet!
		pass
		
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
				self.tree.insert('',tk.END,values=emod)
				
			self.tree.grid(row=2, column = 0, columnspan = 5, sticky = 'nsew', pady = 2)
			
			treescrl = tk.Scrollbar(self.data_w, orient=tk.VERTICAL, command=self.tree.yview)
			self.tree.configure(yscroll=treescrl.set)
			treescrl.grid(row=2, column=4, sticky='ns')
	
	#if we close a window, the class still contains the window state. I don't know how to reshow the window, so instead we'll destroy the window so we can launch it again.
	def data_win_close(self):
		self.data_w.destroy()
		self.data_w = None
		
	def graph_win_close(self):
		self.graph_w.destroy()
		self.graph_w = None
		
	def plot_data(self):
		run = True
		#clear the old graph
		while run:
			ln = self.lineplot.pop(0)
			ln.remove()
			if len(self.lineplot) == 0:
				run = False
	
		num_elem = 0
		#plot the new graph
		for el in self.dset.dataset:
			#we only want to plot elements who's color values are not "None"
			col = el['Color']
			if col != "None":
				if self.ax_rect == []:
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
		self.graph_range = []

		self.graphaxes_x = self.plot1.set_xlim(self.ax_rect[0], self.ax_rect[2])
		self.graphaxes_y = self.plot1.set_ylim(self.ax_rect[1], self.ax_rect[3])

			
		self.canvas.draw()
		
	def focus_next(event):
		#this makes tab move to the next text field. Yes, it's that important to me.
		event.widget.tk_focusNext().focus()
		return("break")
		
	def graph_window(self):

		dat = self.dset.description

		#we don't want to launch a new window if one exists
		if self.graph_w == None:
		
			#the y-padding for this window
			pdy = 2
		
			self.graph_w = tk.Toplevel(self.master)
			self.graph_w.protocol("WM_DELETE_WINDOW", self.graph_win_close)
			#self.data_w.geometry("600x200")
			self.g_txt_desc_w = tk.Text(self.graph_w, height = 2, width = 80 )
			self.g_txt_desc_w.insert(tk.END,dat)
			
			self.g_txt_desc_w.grid(row=0, column = 1, columnspan = 3, sticky = tk.W + tk.E, pady = pdy)
			
			lab1 = tk.Label(self.graph_w, text = "Data Description")
			
			lab1.grid(row=0, column = 0, columnspan = 1, sticky = tk.W, pady = pdy)
			
			self.addgroup_btn_w = tk.Button(self.graph_w, text = "Add Element to Plot", command = self.add_element)
			self.addgroup_btn_w.grid(row=1, column = 0, columnspan = 1, sticky = tk.W + tk.E, pady = pdy)
			
			self.graph_tkvar = tk.StringVar(self.graph_w)
			self.color_options = ["Red", "Green", "Blue", "Black", "Yellow", "Orange", "Purple", "Grey", "Pink"]
			self.graph_tkvar.set(self.color_options[self.color_index])

			self.color_select = tk.OptionMenu(self.graph_w, self.graph_tkvar, *self.color_options)
			self.color_select.grid(row=1, column = 1, columnspan = 2, sticky = tk.W + tk.E, pady = pdy)
			
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
				self.graphtree.column(k, width=60)
			
			for c in treecol:
				self.graphtree.heading(c, text=c)
			
			for e in self.dset.dataset:
				emod = []
				for c in treecol:
					emod.append(e[c])
				self.graphtree.insert('',tk.END,values=emod, iid=e['md5'])
				
			self.graphtree.grid(row=2, column = 0, columnspan = 5,sticky = 'nsew', pady = 2)
			
			treescrl = tk.Scrollbar(self.graph_w, orient=tk.VERTICAL, command=self.tree.yview)
			self.graphtree.configure(yscroll=treescrl.set)
			treescrl.grid(row=2, column=5, sticky='ns')

			self.graph_tkvar.set(self.color_options[self.color_index])
			#next time a different default color! Magic!
			self.color_index += 1


	def add_element(self):
		
		for i in self.graphtree.selection():
			self.selected_elements.append(i)
			element = self.dset.retrieve(i)
			element['Color'] = self.graph_tkvar.get()
			self.dset.remove(i)
			self.dset.add_element(element)

		
		print(self.selected_elements)

		self.draw_graphtree()

		pass
		#this will be to place highlihgted tree item on plotting list
