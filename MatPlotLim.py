import csv
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)

top = Tk()
top.title("MatPlotLim")
top.geometry("820x520")
frm = tk.Frame(top)
frm.place(x=337, y=30)

fig = Figure(figsize=(4.5, 4.5),
             dpi=100)

# list of squares
y = [i ** 2 for i in range(101)]

# adding the subplot
plot1 = fig.add_subplot(111)

# plotting the graph
plot1.plot(y)

# creating the Tkinter canvas
# containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig,
                           master=frm)
canvas.draw()

# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack()

# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas,
                               frm)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack()

def plot():
    # the figure that will contain the plot

    fig = Figure(figsize=(5, 5),
                 dpi=100)

    # list of squares
    y = [i ** 2 for i in range(101)]

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(y)

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig,
                               master=window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,
                                   window)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()




def main():
    for widget in frm.winfo_children():
        widget.destroy()
    CSVfile = "HSSDatav3.txt"

    results = []
    with open(CSVfile) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
        for row in reader:  # each row is a list
            #print(row)
            results.append(row)

    xvar = [float(i[0]) for i in results]
    yvar = [float(i[1]) for i in results]

    fig = Figure(figsize=(4.5, 4.5),dpi=100)

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(xvar, yvar)

    # creating the Tkinter canvas
    # containing the Matplotlib figure


    canvas = FigureCanvasTkAgg(fig, master=frm)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas,frm)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

    #fig = plt.figure()
    #ax = fig.add_subplot()
    #ax.scatter(xvar, yvar)
    #plt.show()

#GUI Buttons

b0 = Button(top, text = "Select Data", command = main)
b0.place(x=7, y=10)

b1 = Button(top, text = "Plot", command = main)
b1.place(x=87, y=10)

b2 = Button(top, text = "Translate", command = main)
b2.place(x=7, y=40)

#inputs for translation

Var11 = Text(top, height = 2, width = 4)
Var11.place(x=37, y=70)

Var12 = Text(top, height = 2, width = 4)
Var12.place(x=37, y=120)

Var13 = Text(top, height = 2, width = 4)
Var13.place(x=37, y=170)

txt_title = Text(top, height = 2, width = 24, )
txt_title.insert(END,"Chart Title")
txt_title.place(x=77, y=227)

txt_xaxis = Text(top, height = 2, width = 24 )
txt_xaxis.insert(END,"X Axis")
txt_xaxis.place(x=77, y=277)

txt_yaxis = Text(top, height = 2, width = 24)
txt_yaxis.insert(END,"Yaxis")
txt_yaxis.place(x=77, y=327)

#input theta for rotation

Theta = Text(top, height = 2, width = 4)
Theta.place(x=187, y=70)

#dropdown menus

tkvar = StringVar(top)
options = ["Rotate About X", "Rotate About Y", "Rotate About Z"]
tkvar.set("Click to select Rotation")

popupMenu = OptionMenu(top, tkvar, *options)
popupMenu.place(x=137, y = 39)

lbl_theta = Label(top,text = "Tx:")
lbl_theta.place(x = 7, y=77)

lbl_theta = Label(top,text = "Ty:")
lbl_theta.place(x = 7, y=127)

lbl_theta = Label(top,text = "Tz:")
lbl_theta.place(x = 7, y=177)

lbl_theta = Label(top,text = "Theta:")
lbl_theta.place(x = 137, y=77)

lbl_title = Label(top,text = "Chart Title:")
lbl_title.place(x = 7, y=232)

lbl_xaxis = Label(top,text = "X Axis Text:")
lbl_xaxis.place(x = 7, y=282)

lbl_yaxis = Label(top,text = "Y Axis Text:")
lbl_yaxis.place(x = 7, y=332)


b0.pack
b1.pack
b2.pack
Var11.pack
Var12.pack
Var13.pack

top.mainloop()