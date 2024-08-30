# Import modules
from tkinter import *

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def create(username, password): # initialise User object
    user_details = User(username, password)
    print(user_details.username)
    print(user_details.password)

def on_click():
    # Retrieve the values from the entry fields and call create
    username = e1.get()
    password = e2.get()
    create(username, password)

master = Tk() # create main window

# Create Username and Password input boxes
Label(master, text="Username").grid(row=0)
Label(master, text="Password").grid(row=1)

e1 = Entry(master)
e2 = Entry(master, show="*")
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

# Create button
button = Button(master, text="Sign Up", command=on_click)
button.grid(row=2, column=0, columnspan=2) # position button

mainloop()
