import hashlib
from tkinter import *
import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        hashed_password = self.hash_password(self.password)
        parameters = (self.username, hashed_password, self.password)
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
            for widget in form_frame.grid_slaves(row=4, column=0):
                widget.destroy()
            Label(form_frame, text="Error: Username already exists.", fg="red").grid(row=4, column=0, columnspan=2)

        connection.close()

    def check_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        parameters = (self.username,)
        result = ""

        for widget in form_frame.grid_slaves(row=4, column=0):
                widget.destroy()

        try:
            cursor.execute(''' SELECT Username, Password FROM Users WHERE Username = ?''', parameters)
            userExists = cursor.fetchone()

            if userExists:
                print(f"User found: {userExists[0]}")
                stored_hashed_password = userExists[1]
                provided_hashed_password = self.hash_password(self.password)
                print(stored_hashed_password + " " + provided_hashed_password)
                if stored_hashed_password == provided_hashed_password:
                    result = True
                else:
                    result = "Incorrect Password, please try again"
            else:
                result = "This username does not exist"
            
        finally:
            connection.close()

        return result

def on_click():
    username = e1.get()
    password = e2.get()
    passwordAgain = e3.get()
    if password != passwordAgain:
        password_result = "Passwords do not match, please try again"
    else:
        password_result = password_check(username, password)

    # Clear any existing messages
    for widget in form_frame.grid_slaves(row=4, column=0):
        widget.destroy()
        
    if password_result == True:
        user_details = User(username, password)
        user_details.add_user()
    else:
        Label(form_frame, text=password_result, fg="red").grid(row=4, column=0, columnspan=2)

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
gameWindow.title("Sign Up")

# Create a Frame to hold the form widgets
form_frame = Frame(gameWindow)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Create Username and Password input boxes
enterUsername = Label(form_frame, text="Enter Username").grid(row=0, column=0, pady=5)
enterPassword = Label(form_frame, text="Enter Password").grid(row=1, column=0, pady=5)
enterPasswordAgain = Label(form_frame, text="Enter Password Again")
enterPasswordAgain.grid(row=2, column=0, pady=5)

# Update widgets to load sign in page
def load_signin():
    global form_frame
    gameWindow.title("Sign In")
    enterPasswordAgain.destroy()
    button.destroy()
    signinButton["text"] = "Sign In"
    signinButton.config(command=lambda: commence_signin())
    e3.destroy()
    e1.delete(0, END)
    e2.delete(0, END)

def commence_signin():
    username = e1.get()
    password = e2.get()
    user_details = User(username, password)
    checkDetails = user_details.check_user()
    if checkDetails == True:
        # Clear window and display signup success message
        for widgets in gameWindow.winfo_children():
            widgets.destroy()
        Label(gameWindow, text="Sign Up Successful").pack(pady=20)
        gameWindow.title("Main Game")
    else:
        errorMessage = Label(form_frame, text=checkDetails, fg="red").grid(row=4, column=0, columnspan=2)
    
                
signinButton = Button(form_frame, text="Already have an account? Sign In", command=load_signin)
signinButton.grid(row=5, column=0, columnspan=2, pady=5)


e1 = Entry(form_frame)
e2 = Entry(form_frame, show="*")
e3 = Entry(form_frame, show="*")
e1.grid(row=0, column=1, pady=5)
e2.grid(row=1, column=1, pady=5)
e3.grid(row=2, column=1, pady=5)

# Create button
button = Button(form_frame, text="Sign Up", command=on_click)
button.grid(row=3, column=0, columnspan=2, pady=10)

mainloop()
