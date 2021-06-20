from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from sort import build
from pathlib import Path
from search import Search


class Home:
    def __init__(self):

        root = Tk()
        root.title("Clima-tools")
        root.geometry("1200x600")
        root.update()

        root.columnconfigure(0, weight=1)  # centers column
        root.rowconfigure(0, weight=1)  # centers rows
        frame = ttk.Frame(root, name="main")
        frame.grid(column=0, row=0)
        self.advanced = False

        self.root = root
        self.frame = frame
        self.build_home_screen()
        self.root.mainloop()


    def build_home_screen(self):
        single_station = Button(self.frame, text="Single Station File", command=self.search)
        bulk_stations = Button(self.frame, text="Multiple Stations File", command=None)
        padding = self.root.winfo_width()*.005
        single_station.grid(column=0, row=0, padx=padding)
        bulk_stations.grid(column=1, row=0, padx=padding)

    def search(self):
        padding = self.root.winfo_width()*.005
        for widget in self.frame.winfo_children():
            widget.destroy()



        file_label = Label(self.frame, text="File Path:")
        file_entry = Entry(self.frame, name="file_entry", state="readonly")

        def fetch_file(event):
            f_path = filedialog.askopenfilename()
            file_entry.configure(state="normal")
            file_entry.delete(0, END)
            file_entry.insert(END, f_path)
            file_entry.configure(state="readonly")
            file_entry.xview_moveto(1)

        advanced = Button(self.frame, text="Advanced Settings", name="settings", command=lambda: self.settings(file_entry.get(), not self.advanced))
        submit = Button(self.frame, text="Submit", name="submit", command=lambda: self.submit(file_entry.get()))

        file_entry.bind("<1>", fetch_file)
        file_label.grid(column=0, row=0, sticky='w', padx=padding)
        file_entry.grid(column=1, row=0, columnspan=3, sticky='ew', padx=padding)

        advanced.grid(column=0, row=1, columnspan=4, sticky="ew", padx=padding)
        submit.grid(column=0, row=2, columnspan=4, sticky="ew", padx=padding)

    def settings(self, path, advanced_state):
        print(path)
        self.advanced = advanced_state
        curate_by_headers = None
        curate_into_monthly = None
        curate_by_station = None  # if single station, off.
        curate_by_date = None

        single_station = False
        if advanced_state:
            padding = self.root.winfo_width() * .005
            if len(path) < 1:
                print("Path: {0}".format(path))
                error('Please select a proper file.')
                return

            search = Search(path)
            adjustment = self.adjustment()
            row = adjustment[0]

            monthly = Checkbutton(self.frame, text="Curate data by monthly.")
            station = Checkbutton(self.frame, text="Create file for each station")
            date = Checkbutton(self.frame, text="Curate by date range. (intensive)")

            font = ("TkDefaultFont", 12)
            curation = Label(self.frame, text="Curation Options", font=font)

            curation.grid(column=0, row=row, sticky='ew', columnspan=5, pady=(padding*2, 0))
            row += 1

            monthly.grid(column=1, row=row, sticky='w')
            station.grid(column=2, row=row, sticky='w')
            date.grid(column=3, row=row, sticky='w')
            row += 1

            headers = Label(self.frame, text="Headers (to include in curation)", name='headers', font=font)
            headers.grid(column=0, row=row, columnspan=5, sticky='ew', pady=(padding*2, 0))
            row += 1

            choices = {}
            column = 1
            max_col = 3
            # test = Frame(self.frame)
            # test.grid(row=row, column=column)

            try:
                for choice in search.input_headers:
                    choices[choice] = BooleanVar(value=False)
                    button = Checkbutton(self.frame, text=choice, onvalue=1, offvalue=0, variable=choices[choice])
                    button.grid(row=row, column=column, sticky='w')
                    button.columnconfigure(column, weight=1)
                    column += 1
                    if column > max_col:
                        column = 1
                        row += 1

            except:
                error("Issue loading headers... are you sure you selected the right file?")
                for widget in self.frame.winfo_children():
                    if 'row' in widget.grid_info() and not isinstance(widget, Button):
                        if widget.grid_info()['row'] > 0:
                            widget.destroy()
                return

            row += 1
            self.root.nametowidget('.main.file_entry').grid(column=1, columnspan=3)
            self.root.nametowidget('.main.settings').configure(text='Disable Advanced Settings')
            self.root.nametowidget('.main.settings').grid_configure(column=1, row=row, columnspan=3)
            row += 1
            self.root.nametowidget('.main.submit').grid_configure(column=1, row=row, columnspan=3)

            for col_num in range(self.frame.grid_size()[0]):
                self.frame.grid_columnconfigure(col_num, weight=1, uniform='fred')
        else:

            for widget in self.frame.winfo_children():
                if 'row' in widget.grid_info() and not isinstance(widget, Button):
                    if widget.grid_info()['row'] > 0:
                        widget.destroy()
            self.root.nametowidget('.main.settings').configure(text='Advanced Settings')





        choices = {}


        """
        max_col = 4
        column=0

        headers = Label(self.frame, text="Headers")
        for choice in search.input_headers:
            choices[choice] = BooleanVar(value=False)
            button = Checkbutton(self.frame, text=choice, onvalue=1, offvalue=0, variable=choices[choice])
            button.grid(row=row, column=column, sticky='w')
            column += 1
            if column > max_col:
                column = 0
                row += 1

        if single_station:
            pass

        row += 1
        for button in adjustment[1]:
            button.grid(row=row, columnspan=5, sticky='ew')
            row += 1
         """

    def adjustment(self):
        row_higher = 0
        removed = []
        for item in self.frame.winfo_children():
            if item.grid_info()['row'] > row_higher:
                row_higher = item.grid_info()['row']
        return [row_higher+1, removed]

    def submit(self, path, options=None):
        print("ee")
        if not self.advanced:
            pass
            # options should be none
        else:
            pass


def error(message):
    root = Tk()
    root.title("Error Message")
    root.geometry('200x100')
    frame = Frame(root)
    label = Label(frame, text=message)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.grid(column=0, row=0)
    label.grid(column=0, row=0)

    root.mainloop()
   

"""

file_label = Label(frame, text="File Path:")
file_path = Entry(frame, state="readonly")


def fetch_file():
    file_path.delete(0, END)
    f_path = filedialog.askopenfilename()
    file_path.configure(state="normal")
    file_path.insert(END, f_path)
    file_path.configure(state="readonly")


get_fi = ttk.Button(frame, text="Load file", command=fetch_file)
submit = ttk.Button(frame, text="Submit", command=lambda: build(Path(file_path.get())))
advanced = ttk.Button(frame, text="Advanced settings")


frame.grid(column=0, row=0)
file_label.grid(column=0, row=0)
file_path.grid(column=1, row=0, columnspan=2)
get_fi.grid(column=3, row=0)

submit.grid(column=0, row=1, columnspan=4, sticky="ew")
advanced.grid(column=0, row=2, columnspan=4, sticky="ew")
file_path.icursor(20)

"""

s = Home()