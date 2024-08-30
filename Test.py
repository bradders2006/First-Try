# Import modules
from tkinter import *

master = Tk() # create main window

# Create Username and Password input boxes
Label(master, text="Username").grid(row=0)
Label(master, text="Password").grid(row=1)

e1 = Entry(master)
e2 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

# Create button
button = Button(master, text="Signup")
button.grid(row=2, column=0, columnspan=2) # position button

mainloop()
