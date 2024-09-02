from tkinter import *
import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def add_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        parameters = (self.username, str(hash(self.password)), self.password)
        try:
            cursor.execute('''INSERT INTO Users (Username, Password, Password2) VALUES (?, ?, ?)''', parameters)        
            connection.commit()

            # Clear window and display signup success message
            for widgets in gameWindow.winfo_children():
                widgets.destroy()
            Label(gameWindow, text="Sign Up Successful").pack(pady=20)
            gameWindow.title("Main Game")

        except sqlite3.IntegrityError as e:
            # Clear any existing messages
            for widget in form_frame.grid_slaves(row=3, column=0):
                widget.destroy()
            Label(form_frame, text="Error: Username already exists.", fg="red").grid(row=3, column=0, columnspan=2)

        connection.close()

def on_click():
    username = e1.get()
    password = e2.get()
    password_result = password_check(username, password)

    # Clear any existing messages
    for widget in form_frame.grid_slaves(row=3, column=0):
        widget.destroy()
        
    if password_result == True:
        user_details = User(username, password)
        user_details.add_user()
    else:
        Label(form_frame, text=password_result, fg="red").grid(row=3, column=0, columnspan=2)

def password_check(username, passwd):
    SpecialSym = ["$", "@", "#", "%", "&", "*", "!", "."]
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

gameWindow = Tk()

width = gameWindow.winfo_screenwidth()
height = gameWindow.winfo_screenheight()

gameWindow.geometry("%dx%d" % (width, height))
gameWindow.title("Signup Form")

# Create a Frame to hold the form widgets
form_frame = Frame(gameWindow)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create Username and Password input boxes
Label(form_frame, text="Username").grid(row=0, column=0, pady=5)
Label(form_frame, text="Password").grid(row=1, column=0, pady=5)

e1 = Entry(form_frame)
e2 = Entry(form_frame, show="*")
e1.grid(row=0, column=1, pady=5)
e2.grid(row=1, column=1, pady=5)

# Create button
button = Button(form_frame, text="Sign Up", command=on_click)
button.grid(row=2, column=0, columnspan=2, pady=10)

mainloop()
