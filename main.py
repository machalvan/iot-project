from tkinter import *
from tkinter import filedialog
import csv


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("IOT")
        self.pack(fill=BOTH, expand=1)

        import_button = Button(self, text="Import", command=self.import_data)
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


root = Tk()
root.geometry("400x300")

app = Window(root)

root.mainloop()
