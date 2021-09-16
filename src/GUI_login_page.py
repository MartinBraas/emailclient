import tkinter as tk
from tkinter.constants import LEFT, RIGHT
from PIL import Image, ImageTk
import server as sv
import mail as em
import variables

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

def smtp():
    if "gmail" in username_value:
        v.choose_smtp(1)
    elif "outlook" in username_value or "hotmail" in username_value or "live" in username_value:
        v.choose_smtp(0, " ", 0)

def nextPage():
    root.destroy()
    import ui_page
    
def function_call():
    #sendemail()
    save()
    #print_value()
    smtp()
    v.load_login(username_value, password_value)
    nextPage()

# def outlook_smtp():
#     v.choose_smtp(0)

# def gmail_smtp():
#     v.choose_smtp(1)

def advanced_tab():
    root.destroy()
    import advanced

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
username_entry.focus_force()

# Password label and entry
password_label = tk.Label(root, text= "Password", fg="white", bg="purple")
password_label.pack(pady=10)
password_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange", show="*")
password_entry.pack(pady=5)

# # Button for picking Outlook SMTP Servers
# outlook = tk.Checkbutton(root, text="OUTLOOK", padx=10, pady=5, bg="orange", command=outlook_smtp)
# outlook.pack(side=RIGHT)

# # Button for picking GMAIL SMTP Servers
# gmail = tk.Checkbutton(root, text="GMAIL", padx=10, pady=5, bg="orange", command=gmail_smtp)
# gmail.pack(side=LEFT)

info = tk.Label(root, text="GMAIL and Outlook/Hotmail/Live is autodetected", pady=5, fg="white", bg="purple")
info.pack(pady=10)

# Button for login
enter = tk.Button(root, text="Login", padx=10, pady=5, bg="orange", command=function_call)
enter.pack(pady=30)

# Button for Advanced tab
advanced = tk.Button(root, text="Advanced", padx=10, pady=5, bg="orange", command=advanced_tab)
advanced.pack(pady=30)

#image=logo1

root.mainloop()