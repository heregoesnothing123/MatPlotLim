import tkinter as tk
from gui_classes import *

def main():
	top = tk.Tk()
	app = MatPlotLim(top)
	top.mainloop()

if __name__ == '__main__':
    main()