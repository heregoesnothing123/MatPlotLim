import csv
import math
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
top.geometry("1120x820")
frm = tk.Frame(top)
frm.place(x=337, y=30)

fig = Figure(figsize=(7, 7),
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

    fig = Figure(figsize=(7, 7),
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

def importinput():
    global CSVfile
    CSVfile = fd.askopenfilename()


def main(CSVfile, ctitle, xtext, ytext):
    for widget in frm.winfo_children():
        widget.destroy()
    #CSVfile = CSVfile
    ctitle = txt_title.get("1.0", 'end')
    xtext = txt_xaxis.get("1.0", 'end')
    ytext = txt_yaxis.get("1.0", 'end')
    results = []
    v1 = Var11.get()
    v2 = Var12.get()
    v3 = Var13.get()
    vtheta = Theta.get()

    #These are the transform arrays. Dot them with the coords to transform

    translationarr = []
    translationarr.append([1, 0, 0, 0])
    translationarr.append([0, 1, 0, 0])
    translationarr.append([0, 0, 1, 0])
    translationarr.append([v1, v2, v3, 1])
    translationarr = np.array(translationarr)

    xrotationarr = []
    xrotationarr.append([1, 0, 0, 0])
    xrotationarr.append([0, math.cos(vtheta), -1*math.sin(vtheta), 0])
    xrotationarr.append([0, math.sin(vtheta), math.cos(vtheta), 0])
    xrotationarr.append([0, 0, 0, 1])
    xrotationarr = np.array(xrotationarr)

    yrotationarr = []
    yrotationarr.append([math.cos(vtheta), 0, math.sin(vtheta), 0])
    yrotationarr.append([0, 1, 0, 0])
    yrotationarr.append([-1*math.sin(vtheta), 0, math.cos(vtheta), 0])
    yrotationarr.append([0, 0, 0, 1])
    yrotationarr = np.array(yrotationarr)

    zrotationarr = []
    zrotationarr.append([math.cos(vtheta), -1*math.sin(vtheta), 0, 0])
    zrotationarr.append([math.sin(vtheta), math.cos(vtheta), 0, 0])
    zrotationarr.append([0, 0, 1, 0])
    zrotationarr.append([0, 0, 0, 1])
    zrotationarr = np.array(zrotationarr)

    rtoggle = tkvar.get()

    with open(CSVfile) as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
        for row in reader:  # each row is a list
            #print(row)
            results.append(row)

    xvar = [float(i[0]) for i in results]
    yvar = [float(i[1]) for i in results]

    fig = Figure(figsize=(7, 7))

    # adding the subplot
    plot1 = fig.add_subplot(111)

    # plotting the graph
    plot1.plot(xvar, yvar)

    plot1.set_xlabel(xtext)
    plot1.set_ylabel(ytext)
    plot1.set_title(ctitle)
    plt.tight_layout()
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



#inputs for translation

Var11 = tk.Entry(top)
Var11.place(x=37, y=76)

Var12 = tk.Entry(top)
Var12.place(x=37, y=126)

Var13 = tk.Entry(top)
Var13.place(x=37, y=176)

txt_title = Text(top, height = 2, width = 24, )
txt_title.insert(END,"Chart Title")
txt_title.place(x=77, y=227)

txt_xaxis = Text(top, height = 2, width = 24 )
txt_xaxis.insert(END,"X Axis")
txt_xaxis.place(x=77, y=277)

txt_yaxis = Text(top, height = 2, width = 24)
txt_yaxis.insert(END,"Y Axis")
txt_yaxis.place(x=77, y=327)

#input theta for rotation

Theta = tk.Entry(top)
Theta.place(x=207, y=76)


#Chart Format
#ctitle = tk.StringVar
#xtext = tk.StringVar
#ytext = tk.StringVar

ctitle = txt_title.get("1.0",'end')
xtext = txt_xaxis.get("1.0",'end')
ytext = txt_yaxis.get("1.0",'end')

#GUI Buttons

b0 = Button(top, text = "Select Data", command = importinput)
b0.place(x=7, y=10)

b1 = Button(top, text = "Plot", command = lambda: main(CSVfile, ctitle, xtext, ytext))
b1.place(x=87, y=10)

b2 = Button(top, text = "Translate", command = main)
b2.place(x=7, y=40)

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
lbl_theta.place(x = 167, y=76)

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
