from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from search import Search, SearchType


class Home:
    def __init__(self):

        # Initialize GUI interface, set title and resolution.
        root = Tk()
        root.title("Clima-tools")
        root.geometry("1200x600")
        root.columnconfigure(0, weight=1)  # centers column
        root.rowconfigure(0, weight=1)  # centers rows
        root.update()

        frame = ttk.Frame(root, name="main")  # add frame to GUI.
        frame.grid(column=0, row=0)  # place frame in GUI grid.

        # set program attributes.
        self.advanced = False  # advanced settings is set to False.
        self.choices = {}  # choices made in advanced settings
        self.root = root
        self.frame = frame
        self.search = Search()

        self.padding = self.root.winfo_width() * .005
        self.build_home_screen()  # build the home screen, adding it to our first frame.
        self.root.mainloop()

    def build_home_screen(self):
        self.destroy_widgets()

        local = Button(self.frame, text="Local File", command=self.local_file)
        local.grid(column=0, row=0, sticky='ew')

        api = Button(self.frame, text="NOAA Online Request", command=None)
        api.grid(column=0, row=1, pady=self.padding, sticky='ew')

    def fetch_file(self, event):
        f_path = filedialog.askopenfilename()
        event.widget.configure(state="normal")
        event.widget.delete(0, END)
        event.widget.insert(END, f_path)
        event.widget.configure(state="readonly")
        event.widget.xview_moveto(1)

        self.search.update({'local_file': event.widget.get()})

        self.choices = {
            "monthly": BooleanVar(value=False),
            "separate_files": BooleanVar(value=False),
            "date": BooleanVar(value=False),
            "output_options": {
                "csv": BooleanVar(value=False),
                "png": BooleanVar(value=False),
            },
            "header_options": {}
        }

        for header in self.search.input_headers:
            self.choices['header_options'][header] = BooleanVar(value=False)

    def local_file(self):
        self.destroy_widgets()
        self.search.update({'search_type': SearchType.LOCAL_FILE})

        file_label = Label(self.frame, text="File Path:")
        t = StringVar(self.frame, value=self.search.local_file)
        file_entry = Entry(self.frame, name="file_entry", state="readonly", textvariable=t)
        load_file = Button(self.frame, text="Next", name="load_file", command=self.output_options)
        back = Button(self.frame, text="Back", command=self.build_home_screen)

        file_entry.bind('<1>', self.fetch_file)

        file_label.grid(column=0, row=0, padx=self.padding)
        file_entry.grid(column=1, row=0, padx=self.padding)
        back.grid(row=1, column=0, sticky='ew', padx=self.padding, pady=self.padding)

        load_file.grid(row=1, column=1, columnspan=2, sticky='ew', padx=self.padding, pady=self.padding)

    def output_options(self):
        self.destroy_widgets()

        output_label = Label(self.frame, text="Select Output File Type", font=("TkDefaultFont", 20))
        graph_option = Checkbutton(self.frame, text="Graphs", onvalue=True, offvalue=False,
                                   variable=self.choices['output_options']['png'])
        csv_option = Checkbutton(self.frame, text="CSV file", onvalue=True, offvalue=False,
                                 variable=self.choices['output_options']['csv'])

        curation = Label(self.frame, text="Curation Options", font=("TkDefaultFont", 14))
        monthly = Checkbutton(self.frame, text="Curate data by monthly.", onvalue=True, offvalue=False,
                              variable=self.choices['monthly'])
        station = Checkbutton(self.frame, text="Create file for each station", onvalue=True, offvalue=False,
                              variable=self.choices['separate_files'])
        date = Checkbutton(self.frame, text="Curate by date range. (intensive)", onvalue=True, offvalue=False,
                           variable=self.choices['date'])
        back = Button(self.frame, text="Back", command=self.local_file)
        curate = Button(self.frame, text="Next", command=self.curate_options)
        curate.bind('<1>')

        output_label.grid(row=0, column=0, sticky='ew', pady=self.padding * 2, columnspan=3)
        graph_option.grid(row=1, column=0, columnspan=2)
        csv_option.grid(row=1, column=1, columnspan=2)
        curation.grid(row=2, column=0, columnspan=5, pady=(self.padding * 2, 0))

        monthly.grid(row=3, column=0, sticky='w')
        station.grid(row=3, column=1, sticky='w')
        date.grid(row=3, column=2, sticky='w')

        back.grid(row=4, column=0, sticky='ew', pady=self.padding * 2, padx=self.padding)
        curate.grid(row=4, column=1, sticky='ew', columnspan=2, pady=self.padding * 2, padx=self.padding)

        # TO DO: we need to update NewSearch with Checkbutton selections.

    def curate_options(self):
        self.destroy_widgets()

        headers = Label(self.frame, text="Headers", name='headers', font=("TkDefaultFont", 14))
        headers.grid(row=0, column=1, columnspan=4, sticky='ew')

        column = 1
        max_col = 4
        row = 1

        try:
            for choice in self.search.input_headers:
                button = Checkbutton(self.frame, text=choice, onvalue=1, offvalue=0,
                                     variable=self.choices['header_options'][choice])

                button.grid(row=row, column=column, sticky='w')
                column += 1

                if column > max_col:
                    column = 1
                    row += 1
        except Exception as err:
            print(err)
            error("Issue loading headers... are you sure you selected the right file?")
            for widget in self.frame.winfo_children():
                if 'row' in widget.grid_info() and not isinstance(widget, Button):
                    if widget.grid_info()['row'] > 0:
                        widget.destroy()
            return

        back = Button(self.frame, text="Back", command=self.output_options)
        submit = Button(self.frame, text="Submit", command=self.submit)

        back.grid(row=4, column=1, sticky='ew', pady=self.padding * 2, padx=self.padding)
        submit.grid(row=4, column=2, sticky='ew', columnspan=3, pady=self.padding * 2, padx=self.padding)

    def submit(self):
        output = {}

        for key, val in self.choices.items():

            if isinstance(val, dict):
                for subkey, subval in val.items():
                    if 'subkey' == 'DATE_OPT' and self.choices['date'].get():
                        pass
                    else:
                        if subval.get():
                            if key not in output:
                                output[key] = [subkey]
                            else:
                                output[key].append(subkey)
            else:
                output[key] = val.get()

        print(output)

    def destroy_widgets(self):
        for widget in self.frame.winfo_children():
            widget.destroy()


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


s = Home()
