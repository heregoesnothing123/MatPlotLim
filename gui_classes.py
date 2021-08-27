import tkinter as tk
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
		y = [i ** 2 for i in range(101)]

		self.plot1 = self.fig.add_subplot(111)
		self.plot1.plot(y)
		self.plot1.set_title('Chart Title')
		self.plot1.set_ylabel('Y Label')
		self.plot1.set_xlabel('X Label')
		self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
		self.toolbar.update()
		self.canvas.get_tk_widget().pack()
		
		self.b0 = tk.Button(self.master, text = "Select Data", command = self.data_select)
		self.b0.place(x=7, y=10)

		self.b1 = tk.Button(self.master, text = "Plot", command = self.placeholder)
		self.b1.place(x=87, y=10)

		self.b2 = tk.Button(self.master, text = "Translate", command = self.placeholder)
		self.b2.place(x=7, y=40)

		#inputs for translation
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
		
		self.UpdateGraph = tk.Button(self.master, text = "Configure Dataset", command = self.data_window)
		self.UpdateGraph.place(x=77, y=427)
		self.UpdateGraph.configure(state='disabled')

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
		self.UpdateGraph.configure(state='normal')
		
	def data_window(self):

		dat = self.dset.description

		if self.data_w == None:
			self.data_w = tk.Toplevel(self.master)
			self.data_w.protocol("WM_DELETE_WINDOW", self.data_win_close)
			self.data_w.geometry("600x200")
			self.txt_desc_w = tk.Text(self.data_w, height = 3, width = 50 )
			self.txt_desc_w.insert(tk.END,dat)
			self.txt_desc_w.pack()
		else:
			self.data_w.show()
	
	def data_win_close(self):
		self.data_w.destroy()
		self.data_w = None
		
		