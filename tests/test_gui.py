from tkinter import *
from tkinter import ttk

#top level window
root = Tk()

#frame widget
frm = ttk.Frame(root, padding=10)

#layout
frm.grid()

#label and button for widget
ttk.Label(frm, text="Howdy Partner").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#mainloop puts everything on display and responds to user input until termination
root.mainloop()
