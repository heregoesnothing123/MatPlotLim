from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from kinematicdataset import *
from element_math import *
from datetime import datetime

#this is a class to hold the plot object. It will need the frame in which the plot resides.
class KinematicPlot:

	def __init__(self, plotframe):

		#This line should be in the calling function
		#plotframe = tk.Frame(self.master)

		plotframe.place(relx=0.4, rely=0.05, relheight=0.95, relwidth=0.6)
		
		self.fig = Figure(figsize=(11,10))
		
		#placeholder plot
		y = [i ** 2 for i in range(30)]

		self.plot1 = self.fig.add_subplot(111)
		self.lineplot = self.plot1.plot(y)
		
		self.charttitle = "Chart Title"
		self.xlabel = "X Label"
		self.ylabel = "Y Label"
		
		self.canvas = FigureCanvasTkAgg(self.fig, master=plotframe)
		self.canvas.draw()
		self.canvas.get_tk_widget().pack()
		
		self.toolbar = NavigationToolbar2Tk(self.canvas, plotframe)
		self.toolbar.update()
		self.canvas.get_tk_widget().pack()

		self.default_graph_properties = {}
		self.default_graph_properties['linestyle'] = 'solid'
		self.default_graph_properties['linewidth'] = 3
		
		#dict with keys ymin, ymax, xmin, xmax
		self.graph_range = {}
		self.graph_range['xmin'] = 0.0
		self.graph_range['xmax'] = 100.0
		self.graph_range['ymin'] = -15.0
		self.graph_range['ymax'] = 15.0

		self.verticallines = [25.0,50.0,75.0]
		self.verticalline_annotation = ['HS', 'FF', 'TO']

	def update_graph_range(self, newrange='None'):

		if newrange != 'None':
			assert (isinstance(newrange,dict)),"Range not correct type"
			assert (len(newrange.keys)==4)), "Range not correct type"
			self.graph_range = newrange
		
		self.x_axis = self.plot1.set_xlim(self.graph_range['xmin'], self.graph_range['xmax'])
		self.y_axis = self.plot1.set_ylim(self.graph_range['ymin'], self.graph_range['ymax'])

	def update_graph_titles(self, newtitle):
		
		self.plot1.set_title(self.charttitle)
		self.plot1.set_xlabel(self.xlabel)
		self.plot1.set_ylabel(self.ylabel)

	def clear_graph(self):
		run = True
		if len(self.lineplot) == 0:
			run = False
		while run:
			try:
				ln = self.lineplot.pop(0)
				ln.remove()
			except IndexError:
				pass
			except TypeError:
				pass
			if len(self.lineplot) == 0:
				run = False

	def update(self):

		self.update_graph_range()
		self.update_graph_titles()

		self.fig.canvas.draw()

	def draw_graph_annotations(self):
		#draw vertical lines
		for i in range(0,len(self.verticallines)):
			self.plot1.axvline(x=self.verticallines[i], linestyle='dashed', color='grey')
			self.plot1.annotate(text=self.verticalline_annotation[i], xy=(self.verticallines[i], 10.0), ha='center', backgroundcolor='w')