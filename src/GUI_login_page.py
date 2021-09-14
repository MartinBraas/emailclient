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

#How to send a mail and server config
def sendemail():
    print("letsgo")
    # SMTP SERVER
    smtpserv = "smtp-mail.outlook.com"
    port_w_tls = 587
    port = 25

    server = sv.Server(smtpserv, port_w_tls, port)
    server.connect()

    email = em.Email()
    with open('../message.txt', 'r') as f:
        message = f.read()
    email.setBody(message)

    email.setRecipient('Martin 2', 'koentimmy@hotmail.com')

    email.setSubject('Din mor')

    print("Input password here\n")
    pwd = getpass()
    server.login('martin.hatting@hotmail.com', pwd)

    server.send('martin.hatting@hotmail.com', 'koentimmy@hotmail.com', email.getString())

    server.quit()

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
enter = tk.Button(root, text="Enter", padx=10, pady=5, fg="white", bg="orange", command=function_call)
enter.pack(pady=30)

root.mainloop()