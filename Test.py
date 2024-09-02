# Import modules
from tkinter import *
import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_user(self): # add user to database
        connection = sqlite3.connect("Users.db") # create or connect to database
        cursor = connection.cursor() # create a cursor object to interact with the database

        # Insert username and hashed password into database
        parameters = (self.username, str(hash(self.password)))
        try:
            cursor.execute('''INSERT INTO Users (Username, Password) VALUES (?, ?)''', parameters)        
            connection.commit()

            # Clear window and display signup success message
            for widgets in signup_form.winfo_children():
                widgets.destroy()
                Label(signup_form, text="Sign Up Successful").grid(row=0)

        except sqlite3.IntegrityError as e: # error handling if user tries to signup with an existing username
            # Clear any existing messages
            for widget in signup_form.grid_slaves(row=3, column=0):
                widget.destroy()
            Label(signup_form, text="Error: Username already exists.", fg="red").grid(row=3)

        # Close the connection
        connection.close()

def create(username, password): # initialise User object
    user_details = User(username, password)
    user_details.add_user()

def on_click():
    # Retrieve the values from the entry fields and call create
    username = e1.get()
    password = e2.get()
    password_result = password_check(username, password)

    # Clear any existing messages
    for widget in signup_form.grid_slaves(row=3, column=0):
        widget.destroy()
        
    if password_result == True:
        create(username, password) # take user to 
    else:
        Label(signup_form, text=password_result, fg="red").grid(row=3)
        

# Function to validate the password
def password_check(username, passwd):
     
    SpecialSym =["$", "@", "#", "%", "&", "*", "!", "."]
    val = True
     
    if len(passwd) < 6:
        val = "Password should be at least 6 characters long"
         
    elif not any(char.isdigit() for char in passwd):
        val = "Password should have at least one number"
         
    elif not any(char.isupper() for char in passwd):
        val = "Password should have at least one uppercase letter"
         
    elif not any(char.islower() for char in passwd):
        val = "Password should have at least one lowercase letter"
         
    elif not any(char in SpecialSym for char in passwd):
        val = "Password should have at least one special symbol"

    return val
    

signup_form = Tk() # create main window

# Getting screen width and height of display
width= signup_form.winfo_screenwidth() 
height= signup_form.winfo_screenheight()

# Setting tkinter window size
signup_form.geometry("%dx%d" % (width, height))
signup_form.title("Signup Form")

# Create Username and Password input boxes
Label(signup_form, text="Username").grid(row=0)
Label(signup_form, text="Password").grid(row=1)

e1 = Entry(signup_form)
e2 = Entry(signup_form, show="*")
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)

# Create button
button = Button(signup_form, text="Sign Up", command=on_click)
button.grid(row=2, column=0, columnspan=2) # position button

mainloop()
