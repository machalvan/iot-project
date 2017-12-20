from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import pandas as pd
from pandas import DataFrame
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn.cluster import KMeans
from collections import Counter
from mpl_toolkits.mplot3d import Axes3D
from pylab import *

import csv

data1 = []
data2 = []
data3 = []

def show_title(self, title):
    label = Label(self, text=title, bg="gray")
    label.pack(ipady=10, fill=X)

def show_import(self):
    import_button = ttk.Button(self, text="Import", command=lambda: import_data(self), cursor="hand2")
    import_button.pack(anchor='w')

def show_plot_buttons(self):
    scatter_button = ttk.Button(
        self,
        text="Scatter",
        command=lambda: self.controller.show_frame(LinePage), cursor="hand2")

    pie_button = ttk.Button(
        self,
        text="Pie chart",
        command=lambda: self.controller.show_frame(PiePage), cursor="hand2")

    cluster_button = ttk.Button(
        self,
        text="Cluster chart",
        command=lambda: self.controller.show_frame(ClusterPage), cursor="hand2")

    scatter_button.pack(anchor='w')
    pie_button.pack(anchor='w')
    cluster_button.pack(anchor='w')



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

            data1.append(int(tempV))
            data2.append(int(humiV))
            data3.append(int(brigV))
        print("fyllt lista")

    self.display_summery()


def clear_lists():
    global data1, data2, data3
    data1 = []
    data2 = []
    data3 = []

def get_list(variable):
    if variable == "Temperature":
        return data1
    elif variable == "Brightness":
        return data2
    elif variable == "Humidity":
        return data3

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

        for F in (StartPage, LinePage, PiePage, ClusterPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()




class StartPage(tk.Frame):
    summery_displayed = False

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        show_title(self, "Start page")

        show_import(self)


    def display_summery(self):
        if not self.summery_displayed:
            show_plot_buttons(self)

            label = Label(self, text="Summary")
            entries = Label(self, text="Total entries: " + str(len(data1)))
            meanT = Label(self, text="Mean temperature: " + str(self.calc_mean(data1)))
            meanH = Label(self, text="Mean humidity: " + str(self.calc_mean(data2)))
            meanB = Label(self, text="Mean brightness: " + str(self.calc_mean(data3)))

            label.pack()
            entries.pack()
            meanT.pack()
            meanH.pack()
            meanB.pack()

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

        show_title(self, "Scatter plot")

        show_import(self)

        show_plot_buttons(self)


        self.comboBoxes()

        self.scatter_button = ttk.Button(self, text="Show scatter diagram", command=lambda: self.scatter())
        self.scatter_button.pack()


    '''def update(self):
        print("Updating")

        plot.clear()

        x_label = self.box1.get()
        y_label = self.box2.get()

        x_var = get_list(x_label)
        y_var = get_list(y_label)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plot.plot([x_var], [y_var], 'ro')
        self.canvas.draw()'''

    def scatter(self):
        '''update_button = ttk.Button(self, text="Update", command=lambda: self.update())
        update_button.pack()'''

        x_label = self.box1.get()
        y_label = self.box2.get()

        x_var = get_list(x_label)
        y_var = get_list(y_label)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title('Scatter diagram')

        plot.plot([x_var], [y_var], 'ro')
        '''
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

        self.scatter_button.destroy()'''
        plt.show()



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




class PiePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        show_title(self, "Pie chart")

        show_import(self)

        show_plot_buttons(self)

        label = Label(self, text="Pick element to plot.")
        label.pack()
        self.box1 = ttk.Combobox(self)
        self.box1['values'] = ('Temperature', 'Brightness', 'Humidity')
        self.box1.current(0)
        self.box1.pack()

        plot_button = ttk.Button(self, text="Plot", command=lambda: self.calculate_pie_data(),
                                 cursor="hand2")
        plot_button.pack()


    def calculate_pie_data(self):
        plt.close()

        raw_data = {'Temperature': data1, 'Brightness': data2, 'Humidity': data3}
        variables = ['Temperature', 'Brightness', 'Humidity']
        df = pd.DataFrame(raw_data, columns=variables)

        variable = self.box1.get()
        if(variable == 'Temperature'):
            df['bins'] = pd.cut(df[variable],
                                bins=[int(-30), int(-15), 0, 15, 30, 45],
                                labels=["-30 - -15", "-14 - 0", "1 - 15", "16 - 30", "31 - 45"])
        else:
            df['bins'] = pd.cut(df[variable],
                                bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                labels=["0 - 10", "11 - 20", "21 - 30", "31 - 40", "41 - 50", "51 - 60", "61 - 70",
                                        "71 - 80", "81 - 90", "91 - 100"])
        plot = df.groupby('bins').size()
        print(plot)
        plot.plot.pie(figsize=(4, 4), startangle=90, counterclock=False)
        plt.title(variable)
        plt.ylabel("")
        plt.show()

class ClusterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        show_title(self, "Cluster graph")

        show_import(self)

        show_plot_buttons(self)

        label = Label(self, text="The clustering will plot all the datapoints. No choices to make.")
        label.pack()

        cluster_button = ttk.Button(self, text="Plot", command=lambda: self.make_cluster(),
                                    cursor="hand2")
        cluster_button.pack()


    def fix_list(self):
        tempL = np.column_stack((data1, data2, data3))
        return tempL

    def make_cluster(self):

        X = self.fix_list()

        cluster_num = 3

        kmeans = KMeans(n_clusters=cluster_num)
        kmeans.fit(X)

        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_

        color = ["g", "r", "b"]

        fig = figure()
        ax = fig.gca(projection='3d')

        for i in range(len(X)):
            ax.scatter(X[i][0], X[i][1], X[i][2], c=color[labels[i]])

        for cluster_number in range(cluster_num):
            ax.scatter(centroids[:, 0], centroids[:, 1], centroids[:, 2], marker="x", s=150, linewidths=5, zorder=100,
                       c=color)

        plt.show()



#root = Tk()


app = Window()
app.geometry("600x600+300+10")
app.mainloop()
