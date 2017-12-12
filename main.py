from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

import csv


def import_data(self):
    print("Import button was pressed!")
    filePath = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    with open(filePath, 'r')as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        temperature = []
        humidity = []
        brightness = []

        for row in readCSV:
            tempV = row[0]
            humiV = row[1]
            brigV = row[2]

            temperature.append(tempV)
            humidity.append(humiV)
            brightness.append(brigV)
        print("fyllt lista")
        print(temperature)

        self.controller.up_lists(temperature, humidity, brightness)

    self.controller.show_frame(LinePage)



class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Visualization GUI")
        #self.master = master
        #self.init_window()

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.actT = []
        self.actH = []
        self.actB = []

        self.frames = {}

        for F in (StartPage, LinePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def up_lists(self, tem, hum, bri):
        print("upplist")
        self.actT = tem
        self.actH = hum
        self.actB = bri

    def get_t(self):
        print("getT")
        return self.actT

    def get_h(self):
        return self.actH

    def get_b(self):
        return self.actB


    #def init_window(self):
        #self.master.title("IOT")
        #self.pack(fill=BOTH, expand=1)

        #self.canvas = Canvas(self, width=800, height=600)
        #self.canvas.place(x=100, y=0)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Start Page")
        label.pack(pady=10, padx=10)

        import_button = ttk.Button(self, text="Import", command=lambda: import_data(self), cursor="hand2")
        import_button.pack()






class LinePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Linear graph")
        label.pack()

        self.actT = []
        self.actH = []
        self.actB = []

        import_button = ttk.Button(self, text="Import", command=lambda: import_data(self), cursor="hand2")
        import_button.pack()

        scatter_button = ttk.Button(self, text="Show scatter diagram", command=lambda: self.scatter())
        scatter_button.pack()

    def scatter(self):
        self.get_lists()

        x_var = self.actT
        y_var = self.actB

        fig = Figure(figsize=(5, 5), dpi=100)

        plot = fig.add_subplot(111)
        plot.plot([x_var], [y_var], 'ro')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        x_label = "Temperature"
        y_label = "Brightness"
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title('Scatter diagram')




    def get_lists(self):
        self.actT = self.controller.get_t()
        self.actH = self.controller.get_h()
        self.actB = self.controller.get_b()

#root = Tk()


app = Window()
app.geometry("600x400")
app.mainloop()
