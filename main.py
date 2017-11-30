from tkinter import *


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

root = Tk()
root.geometry("400x300")

app = Window(root)

root.mainloop()
