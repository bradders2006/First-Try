import hashlib
from tkinter import *
import sqlite3
import random

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()

        # Create Users table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (Username TEXT UNIQUE, Password TEXT)''')
        
        hashed_password = self.hash_password(self.password)
        parameters = (self.username, hashed_password)
        try:
            cursor.execute('''INSERT INTO Users (Username, Password) VALUES (?, ?)''', parameters)
            connection.commit()

            clear_frame()
            gameWindow.title("Main Game")
            Button(form_frame, text="Play Game", command=play).grid(row=0, column=0, columnspan=2, pady=10)
            Button(form_frame, text="View Leaderboard", command=lambda: print("Loading Leaderboard")).grid(row=1, column=0, columnspan=2, pady=10)

        except sqlite3.IntegrityError:
            display_message("Error: Username already exists.", "red")

        connection.close()

    def check_user(self):
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        parameters = (self.username,)
        result = ""

        clear_row(row=4)

        try:
            cursor.execute('''SELECT Username, Password FROM Users WHERE Username = ?''', parameters)
            userExists = cursor.fetchone()

            if userExists:
                stored_hashed_password = userExists[1]
                provided_hashed_password = self.hash_password(self.password)
                if stored_hashed_password == provided_hashed_password:
                    result = True
                else:
                    result = "Incorrect Password, please try again"
            else:
                result = "This username does not exist"

        finally:
            connection.close()

        return result

def clear_frame():
    for widget in form_frame.winfo_children():
        widget.destroy()

def clear_row(row):
    for widget in form_frame.grid_slaves(row=row):
        widget.destroy()

def display_message(message, color):
    clear_row(4)
    Label(form_frame, text=message, fg=color).grid(row=4, column=0, columnspan=2)

def on_click():
    global user_details
    username = e1.get()
    password = e2.get()
    passwordAgain = e3.get()
    if password != passwordAgain:
        password_result = "Passwords do not match, please try again"
    else:
        password_result = password_check(username, password)

    clear_row(4)

    if password_result == True:
        user_details = User(username, password)
        user_details.add_user()
    else:
        display_message(password_result, "red")

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

form_frame = Frame(gameWindow)
form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(form_frame, text="Enter Username").grid(row=0, column=0, pady=5)
Label(form_frame, text="Enter Password").grid(row=1, column=0, pady=5)
enterPasswordAgain = Label(form_frame, text="Enter Password Again")
enterPasswordAgain.grid(row=2, column=0, pady=5)

def load_signin():
    gameWindow.title("Sign In")
    enterPasswordAgain.destroy()
    button.destroy()
    signinButton.config(text="Sign In", command=commence_signin)
    e3.destroy()
    e1.delete(0, END)
    e2.delete(0, END)

def commence_signin():
    global user_details
    username = e1.get()
    password = e2.get()
    user_details = User(username, password)
    checkDetails = user_details.check_user()
    if checkDetails == True:
        clear_frame()
        gameWindow.title("Main Game")
        Button(form_frame, text="Play Game", command=play).grid(row=0, column=0, columnspan=2, pady=10)
        Button(form_frame, text="View Leaderboard", command=lambda: print("Loading Leaderboard")).grid(row=1, column=0, columnspan=2, pady=10)
    else:
        display_message(checkDetails, "red")

signinButton = Button(form_frame, text="Already have an account? Sign In", command=load_signin)
signinButton.grid(row=5, column=0, columnspan=2, pady=5)

e1 = Entry(form_frame)
e2 = Entry(form_frame, show="*")
e3 = Entry(form_frame, show="*")
e1.grid(row=0, column=1, pady=5)
e2.grid(row=1, column=1, pady=5)
e3.grid(row=2, column=1, pady=5)

button = Button(form_frame, text="Sign Up", command=on_click)
button.grid(row=3, column=0, columnspan=2, pady=10)

score = 0

def play():
    number = random.randint(1,2)
    
    # Display song initials and song artist
    connection = sqlite3.connect("Users.db")
    cursor = connection.cursor()
        
    try:
        cursor.execute('''SELECT Songname, Artist FROM Songs ORDER BY RANDOM() LIMIT 1''')
        songnameAndArtist = cursor.fetchone()
        answer = songnameAndArtist[0]
        initials = ""
        words = answer.split()
        for i in words:
            initials = initials + i[0] + " "

    finally:
        connection.close()


    
    clear_frame()

    Label(form_frame, text=f"Score: {score}").grid(row=0, column=0, columnspan=2)
    Label(form_frame, text=f"{initials} by {songnameAndArtist[1]}").grid(row=1, column=0, columnspan=2)

    guess_entry = Entry(form_frame)
    guess_entry.grid(row=2, column=0, pady=5, columnspan=2)

    submit_guess = Button(form_frame, text="Enter Answer", command=lambda: checkAnswer(guess_entry.get(), answer))
    submit_guess.grid(row=3, column=0, columnspan=2, pady=5)

def checkAnswer(guess, answer):
    global score, user_details
    global user_details
    if guess.lower() == answer.lower():
        display_message("Correct", "green")
        score+=1
        play()
    else:
        clear_frame()
        Label(form_frame, text=f"Final Score: {score}").grid(row=0, column=0, columnspan=2)

        # Store score if higher than previous high score
        connection = sqlite3.connect("Users.db")
        cursor = connection.cursor()
        cursor.execute('''SELECT HighScore FROM Users WHERE Username = ?''', (user_details.username,))
        current_high_score = cursor.fetchone()[0]

        # Update the high score if the current score is higher
        if score > current_high_score:
            cursor.execute('''UPDATE Users SET HighScore = ? WHERE Username = ?''', (score, user_details.username))
            connection.commit()
            Label(form_frame, text=f"Your High Score: {max(score, current_high_score)}").grid(row=1, column=0, columnspan=2)

        connection.close()
        
        score = 0
        playAgain = Button(form_frame, text="Play Again?", command=lambda: play()).grid(row=2, column=0, columnspan=2)


mainloop()
