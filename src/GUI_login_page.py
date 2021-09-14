import tkinter as tk
from PIL import Image, ImageTk
import server as sv
import mail as em
from getpass import getpass

root = tk.Tk()
root.title("Login")
root.configure(bg="purple")

username_value = "a"
password_value = "b"

#function to get user input from entry widget
def save():
    global username_value, password_value
    username_value = username_entry.get()
    password_value = password_entry.get()

def print_value():
    print("Username: ", username_value, "\nPassword: ", password_value)

def nextPage():
    root.destroy()
    import ui_page

def function_call():
    #sendemail()
    save()
    print_value()
    nextPage()

#logo
page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack(pady=10)

logo1 = Image.open('../images/icon_png-removebg-preview.png')
logo1 = ImageTk.PhotoImage(logo1)

# Username label and entry
username_label = tk.Label(root, text= "E-mail", fg="white", bg="purple")
username_label.pack(pady=10)
username_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
username_entry.pack(pady=5)

# Password label and entry
password_label = tk.Label(root, text= "Password", fg="white", bg="purple")
password_label.pack(pady=10)
password_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange", show="*")
password_entry.pack(pady=5)

# Button for login
enter = tk.Button(root, image=logo1, padx=10, pady=5, fg="white", bg="purple", command=function_call)
enter.pack(pady=30)



root.mainloop()