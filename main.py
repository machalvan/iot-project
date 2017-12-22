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

VAR1 = "Temperature"
VAR2 = "Humidity"
VAR3 = "Brightness"

all_vars = (VAR1, VAR2, VAR3)
all_vars_list = [VAR1, VAR2, VAR3]

def show_title(self, title):
    label = Label(self, text=title, bg="gray")
    label.pack(ipady=10, fill=X)

def show_import(self):
    import_button = ttk.Button(self, text="Import", command=lambda: import_data(self), cursor="hand2")
    import_button.pack(anchor='w')

def show_plot_buttons(self):
    summary_button = ttk.Button(
        self,
        text="Summary",
        command=lambda: self.controller.show_frame(StartPage),
        cursor="hand2")

    scatter_button = ttk.Button(
        self,
        text="Scatter",
        command=lambda: self.controller.show_frame(LinePage),
        cursor="hand2")

    pie_button = ttk.Button(
        self,
        text="Pie chart",
        command=lambda: self.controller.show_frame(PiePage),
        cursor="hand2")

    cluster_button = ttk.Button(
        self,
        text="Cluster chart",
        command=lambda: self.controller.show_frame(ClusterPage),
        cursor="hand2")

    summary_button.pack(anchor='w')
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
            data1.append(int(row[0]))
            data2.append(int(row[1]))
            data3.append(int(row[2]))
        print("fyllt lista")

    self.show_summery()


def clear_lists():
    global data1, data2, data3
    data1 = []
    data2 = []
    data3 = []

def get_list(variable):
    if variable == VAR1:
        return data1
    elif variable == VAR2:
        return data2
    elif variable == VAR3:
        return data3

class Window(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Visualization GUI")


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


    def show_summery(self):
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

            fig, ax = plt.subplots()

            # hide axes
            fig.patch.set_visible(False)
            ax.axis('off')
            ax.axis('tight')

            raw_data = {VAR1: data1, VAR2: data2, VAR3: data3}
            df = pd.DataFrame(raw_data, columns=all_vars_list)

            ax.table(cellText=df.values, colLabels=df.columns, loc='center')

            fig.tight_layout()

            # plt.show()
            canvas = FigureCanvasTkAgg(fig, master=self)
            canvas.get_tk_widget().pack()
            canvas.draw()

            self.summery_displayed = True

    def calc_mean(self, target):
        total = 0
        divide = len(target)
        if divide == 0:
            divide = 1
        for number in target:
            total += int(number)
        return round(total / divide, 2)


class LinePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.box1 = ttk.Combobox(self)
        self.box2 = ttk.Combobox(self)

        show_title(self, "Scatter plot")

        show_import(self)

        show_plot_buttons(self)

        self.comboBoxes()

        self.scatter_button = ttk.Button(self, text="Show scatter diagram", command=lambda: self.scatter())
        self.scatter_button.pack()

    def scatter(self):
        x_label = self.box1.get()
        y_label = self.box2.get()

        x_var = get_list(x_label)
        y_var = get_list(y_label)

        fit = np.polyfit(x_var, y_var, 1)
        fit_fn = np.poly1d(fit)
        
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title('Scatter diagram')

        plt.plot([x_var], [y_var], 'ro', x_var, fit_fn(x_var), '--k')
        plt.show()



    def comboBoxes(self):
        label_x = Label(self, text="X")
        label_y = Label(self, text="Y")

        self.box1['values'] = all_vars
        self.box1.current(1)

        self.box2['values'] = all_vars
        self.box2.current(0)

        label_x.pack()
        self.box1.pack()
        label_y.pack()
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
        self.box1['values'] = all_vars
        self.box1.current(0)
        self.box1.pack()

        plot_button = ttk.Button(self, text="Plot", command=lambda: self.calculate_pie_data(), cursor="hand2")
        plot_button.pack()


    def calculate_pie_data(self):
        plt.close()

        raw_data = {VAR1: data1, VAR2: data2, VAR3: data3}
        df = pd.DataFrame(raw_data, columns=all_vars_list)

        variable = self.box1.get()
        '''
        if variable == 'Temperature':
            df['bins'] = pd.cut(df[variable],
                                bins=[int(-30), int(-15), 0, 15, 30, 45],
                                labels=["-30 - -15", "-14 - 0", "1 - 15", "16 - 30", "31 - 45"])
        else:
            df['bins'] = pd.cut(df[variable],
                                bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                                labels=["0 - 10", "11 - 20", "21 - 30", "31 - 40", "41 - 50", "51 - 60", "61 - 70",
                                        "71 - 80", "81 - 90", "91 - 100"])
        '''

        df['bins'] = pd.cut(df[variable],
                bins=[-100, -90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                labels=["-100 - -91",
                        "-90 - -81",
                        "-80 - -71",
                        "-70 - -61",
                        "-60 - -51",
                        "-50 - -41",
                        "-40 - -31",
                        "-30 - -21",
                        "-20 - -11",
                        "-10 - 0",
                        "1 - 10",
                        "11 - 20",
                        "21 - 30",
                        "31 - 40",
                        "41 - 50",
                        "51 - 60",
                        "61 - 70",
                        "71 - 80",
                        "81 - 90",
                        "91 - 100"])

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

        label = Label(self, text="The clustering will plot all the data points. No choices to make.")
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

        ax.set_xlabel('Temperature')
        ax.set_ylabel('Humidity')
        ax.set_zlabel('Brightness')

        plt.show()


app = Window()
app.state('zoomed')
#app.geometry("600x600+300+10")
app.mainloop()
