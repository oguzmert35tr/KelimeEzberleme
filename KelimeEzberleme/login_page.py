from utils import tkinter, sqlite3, bcrypt, customtkinter
from tkinter import messagebox
from PIL import Image
import app

conn = sqlite3.connect("credentials.db")
cursor = conn.cursor()

cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
             username TEXT NOT NULL,
             password TEXT NOT NULL)""")
conn.close()


# window settings
customtkinter.set_appearance_mode(("dark"))  # background color
customtkinter.set_default_color_theme(("blue"))  # button color
window = customtkinter.CTk()
window.title("Welcome")
window.geometry("480x600")
window.configure(bg="#333333")
window.resizable(False, False)


background = customtkinter.CTkImage(light_image=Image.open("Background.sand.jpg"),
                                    dark_image=Image.open("Background.sand.jpg"), size=(480, 600))
background_label = customtkinter.CTkLabel(master=window, text="", image=background)
background_label.pack(pady=10)

def signup():
    username = usernameEntry.get()
    password = passwordEntry.get()

    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()

    if username != "" and password != "":
        cursor.execute("SELECT username FROM users WHERE username=?", [username])
        if cursor.fetchone() is not None:
            messagebox.showerror("Error", "This username already exists.")
        else:
            encoded_password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
            cursor.execute("INSERT INTO users VALUES (?,?)", [username, hashed_password])
            conn.commit()
            messagebox.showinfo("Successful", "Account has been created.")
            conn.close()

    else:
        messagebox.showerror("Missing Input", "Please create username and password.")

def login():
    signupScreen.destroy()
    loginScreen = customtkinter.CTkFrame(master=window, width=360, height=480)
    loginScreen.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    global usernameLogin
    global passwordLogin

    usernameLogin = customtkinter.CTkEntry(master=loginScreen, width=220, placeholder_text="Username")
    usernameLogin.place(x=70, y=80)

    passwordLogin = customtkinter.CTkEntry(master=loginScreen, width=220, show="*", placeholder_text="Password")
    passwordLogin.place(x=70, y=140)

    logInButton2 = customtkinter.CTkButton(master=loginScreen, text="Login", command=login_account,
                                               corner_radius=15, cursor="hand2")
    logInButton2.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

def login_account():
    username = usernameLogin.get()
    password = passwordLogin.get()

    conn = sqlite3.connect("credentials.db")
    cursor = conn.cursor()

    if username != "" and password != "":
        cursor.execute("SELECT password FROM users WHERE username=?", [username])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(password.encode("utf-8"), result[0]):
                #messagebox.showinfo("Welcome", "Logged in succesfully")

                window.destroy()
                app.app()
            else:
                messagebox.showerror("Error", "Invalid password.")
        else:
            messagebox.showerror("Error", "Invalid username.")
    else:
        messagebox.showerror("Error", "Enter all data")
    conn.close()


signupScreen = customtkinter.CTkFrame(master=window, width=360, height=480)
signupScreen.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

usernameEntry = customtkinter.CTkEntry(master=signupScreen, width=220, placeholder_text="Username")
usernameEntry.place(x=70, y=80)

passwordEntry = customtkinter.CTkEntry(master=signupScreen, show="*", width=220, placeholder_text="Password")
passwordEntry.place(x=70, y=140)

signUpButton = customtkinter.CTkButton(master=signupScreen, text="Sign up", command=signup, corner_radius=15,
                                         cursor="hand2")
signUpButton.place(relx=0.5, rely=0.42, anchor=tkinter.CENTER)

logInButton = customtkinter.CTkButton(master=signupScreen, text="Login", command=login, corner_radius=15,
                                          cursor="hand2")
logInButton.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)

haveAccountLabel = customtkinter.CTkLabel(master=signupScreen, text="Already have an account?")
haveAccountLabel.place(relx=0.5, rely=0.58, anchor=tkinter.CENTER)

window.mainloop()




