import tkinter as tk
from PIL import Image, ImageTk
from tkinter.constants import LEFT, RIGHT, TOP, BOTTOM
import server as sv
import mail as em
import variables
from getpass import getpass

v = variables

recipient_email = "a"
recipient_name = "a"

root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")

#How to send a mail and server config
def sendemail():
    #print("letsgo")
    # SMTP SERVER

    server = sv.Server(v.smtp_serv, v.port_w_tls, v.port)
    server.connect()

    email = em.Email()
    with open('../message.txt', 'r') as f:
        message = f.read()
    email.setBody(message)
    
    email.setRecipient(recipient_name, recipient_email)

    email.setSubject('Din mor')

    server.login(v.email_adress, v.email_password)

    server.send(v.email_adress, recipient_email, email.getString())

    server.quit()

def save():
    global recipient_email, recipient_name
    recipient_email = recipient_mail_entry.get()
    recipient_name = recipient_name_entry.get()

def NextUI():
    root.destroy()

def function_calls():
    save()
    sendemail()
    NextUI()
    
page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack(pady=10)

# Recipient name
recipient_name_label = tk.Label(root, text= "Recipient Name", fg="white", bg="purple")
recipient_name_label.pack(pady=10, side=TOP)
recipient_name_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
recipient_name_entry.pack(side=TOP)

# Recipient email adress
recipient_mail_label = tk.Label(root, text= "Recipient Email Adress", fg="white", bg="purple")
recipient_mail_label.pack(pady=10, side=TOP)
recipient_mail_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
recipient_mail_entry.pack(side=TOP)

# Send email button
enter = tk.Button(root, text="Send", padx=10, pady=5, fg="white", bg="orange", command=function_calls)
enter.pack(pady=20)

root.mainloop()