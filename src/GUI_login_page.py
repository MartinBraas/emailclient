import tkinter as tk
from tkinter.constants import LEFT, RIGHT
from PIL import Image, ImageTk
import server as sv
import mail as em
import variables

# Initialization
v = variables
root = tk.Tk()
root.title("Login")
root.configure(bg="purple")

# Variable initialization
username_value = "a"
password_value = "b"
smtpserv = "a"
port_w_tls = 0
port = 0

#function to get user input from entry widget
def save():
    global username_value, password_value
    username_value = username_entry.get()
    password_value = password_entry.get()

def print_value():
    print("Username: ", username_value, "\nPassword: ", password_value)

#SMTP server settings autodetect GMAIL/OUTLOOK
def smtp():
    if "@gmail" in username_value:
        v.choose_smtp(1, " ", 0)
    elif "@outlook" in username_value or "@hotmail" in username_value or "@live" in username_value:
        v.choose_smtp(0, " ", 0)

# Moves to next UI page
def nextPage():
    root.destroy()
    import ui_page

# Calls number of functions at push of button
def function_call():
    #sendemail()
    save()
    #print_value()
    smtp()
    v.load_login(username_value, password_value)
    nextPage()

# Opens advanced tab
def advanced_tab():
    root.destroy()
    import advanced

# Start of UI page
page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack(pady=10)
#root.iconbitmap('../images/small_skrump_icon.ico') #change

# Username label and entry
username_label = tk.Label(root, text= "E-mail", fg="white", bg="purple")
username_label.pack(pady=10)
username_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
username_entry.pack(pady=5)
username_entry.focus_force()

# Password label and entry
password_label = tk.Label(root, text= "Password", fg="white", bg="purple")
password_label.pack(pady=10)
password_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange", show="*")
password_entry.pack(pady=5)

# Auto detect label
info = tk.Label(root, text="GMAIL and Outlook/Hotmail/Live is autodetected", pady=5, fg="white", bg="purple")
info.pack(pady=10)

# Button for login
enter = tk.Button(root, text="Login", padx=10, pady=5, bg="orange", command=function_call)
enter.pack(pady=30)

# Button for Advanced tab
advanced = tk.Button(root, text="Advanced", padx=10, pady=5, bg="orange", command=advanced_tab)
advanced.pack(pady=30)

#End of UI page
root.mainloop()