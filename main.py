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

data1 = []
data2 = []
data3 = []

def import_data(self):
    self.controller.show_frame(StartPage)
    print("Import button was pressed!")
    filePath = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))

    clear_lists()

    with open(filePath, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        for row in readCSV:
            tempV = row[0]
            humiV = row[1]
            brigV = row[2]

            data1.append(tempV)
            data2.append(humiV)
            data3.append(brigV)
        print("fyllt lista")

    self.display_summery()


def clear_lists():
    global data1, data2, data3
    data1 = []
    data2 = []
    data3 = []

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

        self.frames = {}

        for F in (StartPage, LinePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def customGet(self, string):
        if (string == "Temperature"):
            return data1
        elif (string == "Brightness"):
            return data2
        elif (string == "Humidity"):
            return data3


class StartPage(tk.Frame):
    summery_displayed = False

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Start Page")
        label.pack(pady=10, padx=10)

        import_button = ttk.Button(self, text="Import", command=lambda: import_data(self), cursor="hand2")
        import_button.pack()


    def display_summery(self):
        if not self.summery_displayed:
            label = Label(self, text="Summary")
            label.pack()

            entries = Label(self, text="Total entries: " + str(len(data1)))
            entries.pack()

            meanT = Label(self, text="Mean temperature: " + str(self.calc_mean(data1)))
            meanH = Label(self, text="Mean humidity: " + str(self.calc_mean(data2)))
            meanB = Label(self, text="Mean brightness: " + str(self.calc_mean(data3)))

            meanT.pack()
            meanH.pack()
            meanB.pack()

            scatter_button = ttk.Button(self, text="Scatter", command=lambda: self.controller.show_frame(LinePage),
                                        cursor="hand2")
            scatter_button.pack()

            self.summery_displayed = True

    def calc_mean(self, target):
        total = 0
        divide = len(target)
        if divide == 0:
            divide = 1
        for number in target:
            total += int(number)
        return round(total / divide, 2)



fig = plt.figure(figsize=(5, 5), dpi=100)
plot = fig.add_subplot(111)


class LinePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        import_button = ttk.Button(self, text="Import", command=lambda: import_data(self), cursor="hand2")
        import_button.pack()

        label = Label(self, text="Linear graph")
        label.pack()

        self.comboBoxes()

        self.scatter_button = ttk.Button(self, text="Show scatter diagram", command=lambda: self.scatter())
        self.scatter_button.pack()

    def update(self):
        print("Updating")

        plot.clear()

        x_label = self.box1.get()
        y_label = self.box2.get()

        x_var = self.get_list(x_label)
        y_var = self.get_list(y_label)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plot.plot([x_var], [y_var], 'ro')
        self.canvas.draw()

    def scatter(self):
        update_button = ttk.Button(self, text="Update", command=lambda: self.update())
        update_button.pack()

        x_label = self.box1.get()
        y_label = self.box2.get()

        x_var = self.get_list(x_label)
        y_var = self.get_list(y_label)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title('Scatter diagram')

        plot.plot([x_var], [y_var], 'ro')

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        self.scatter_button.destroy()


    def comboBoxes(self):
        self.box_value = StringVar()
        labelx = Label(self, text="X")
        labely = Label(self, text="Y")

        self.box1 = ttk.Combobox(self)
        self.box1['values'] = ('Temperature', 'Brightness', 'Humidity')
        self.box1.current(1)

        self.box2 = ttk.Combobox(self)
        self.box2['values'] = ('Temperature', 'Brightness', 'Humidity')
        self.box2.current(0)

        labelx.pack()
        self.box1.pack()
        labely.pack()
        self.box2.pack()

    def get_list(self, string):
        return self.controller.customGet(string)



class PiePage(tk.Frame):#lär inte bli att vi använder såvida vi inte hittar något sätt att fixa de på
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="Linear graph")
        label.pack()

        self.labelx = Label(self, text="X")
        self.labely = Label(self, text="Y")
        self.box1 = ttk.Combobox(self)
        self.box1['values'] = ('Temperature', 'Brightness', 'Humidity')
        self.box1.current(1)
        self.box1.pack()

    def get_list(self, string):
        return self.controller.customGet(string)

    def calculatePieData(self):
        #ta fram högsta och lägsta talet, ta fram mellan skillnaden och sedan dela upp mellanskillnaden i 5 lika stora delar, sen plotta en ny lista av med dessa indelningar
        tempL = self.get_list(self.box1.get())
        tempL.sort()
        high = tempL[0]
        low = tempL[-1]


#root = Tk()


app = Window()
app.geometry("600x600")
app.mainloop()
