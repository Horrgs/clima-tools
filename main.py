from contextlib import contextmanager
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from utils import build


root = Tk()
root.title("Clima-tools")
root.geometry("1000x700")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame = ttk.Frame(root)

file_label = Label(frame, text="File Path:")
file_path = Entry(frame, state="readonly")


def fetch_file():
    file_path.delete(0, END)
    f_path = filedialog.askopenfilename()
    file_path.configure(state="normal")
    file_path.insert(END, f_path)
    file_path.configure(state="readonly")


get_fi = ttk.Button(frame, text="Load file", command=fetch_file)
print(file_path.config())


def t():
    print(file_path.get())


submit = ttk.Button(frame, text="Submit", command=lambda: build(file_path.get()))
advanced = ttk.Button(frame, text="Advanced settings")



frame.grid(column=0, row=0)
file_label.grid(column=0, row=0)
file_path.grid(column=1, row=0, columnspan=2)
get_fi.grid(column=3, row=0)

submit.grid(column=0, row=1, columnspan=4, sticky="ew")
advanced.grid(column=0, row=2, columnspan=4, sticky="ew")
file_path.icursor(20)
root.mainloop()


