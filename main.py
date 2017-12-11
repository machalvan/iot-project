from tkinter import *
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import csv




class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)


        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("IOT")
        self.pack(fill=BOTH, expand=1)

        #self.canvas = Canvas(self, width=800, height=600)
        #self.canvas.place(x=100, y=0)

        import_button = Button(self, text="Import", command=self.import_data, cursor="hand2")
        import_button.place(x=0, y=0)

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

            self.actTemp = temperature
            self.actHumi = humidity
            self.actBrig = brightness

            self.linear_button = Button(self, text="Linear", command=self.linear())
            self.linear_button.place(x=40, y=40)

    def linear(self):
        print("test")
        fig = Figure(figsize=(5,5), dpi=100)
        plot = fig.add_subplot(111)
        plot.plot([self.actTemp], [self.actBrig], 'ro')

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)



root = Tk()
root.geometry("600x400")

app = Window(root)

root.mainloop()
