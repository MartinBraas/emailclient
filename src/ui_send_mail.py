import tkinter as tk
from PIL import Image, ImageTk
from tkinter.constants import LEFT, RIGHT, TOP, BOTTOM
import server as sv
import mail as em
import variables

# Variable initialization
v = variables
recipient_email = "a"
recipient_name = "a"
mail_subject = "a"
mail_body = "a"

# UI initialization
root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")
root.state("zoomed")
root.iconbitmap('../images/small_skrump_icon.ico')

# Function for sending mails
def sendemail():
    #print("letsgo")
    # SMTP SERVER
    print(v.smtp_serv, v.port, v.port_w_tls)
    server = sv.Server(v.smtp_serv, v.port_w_tls, v.port)
    server.connect()

    email = em.Email()
    with open('../messages.txt', 'r') as f:
        message = f.read()
    email.setBody(message)
    
    email.setRecipient(recipient_name, recipient_email)
    
    email.setSubject(mail_subject)

    server.login(v.email_adress, v.email_password)

    server.send(v.email_adress, recipient_email, email.getString())

    server.quit()

# Function for saving data entries from the UI
def save():
    global recipient_email, recipient_name, mail_subject, mail_body
    recipient_email = recipient_mail_entry.get()
    recipient_name = recipient_name_entry.get()
    mail_subject = subject_entry.get()
    mail_body = body_entry.get()

# Function for shutting down UI. Can be updated to go to another UI page
def NextUI():
    root.destroy()

# Function for writing text from UI to text file, to be send as body of email
def writeBody():
    File_object = open(r"../messages.txt", 'w')
    File_object.write(mail_body)
    File_object.close()

# Function for calling numerous functions by push of button
def function_calls():
    save()
    writeBody()
    sendemail()
    NextUI()

# UI initialization   
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

# Email subject
subject_label = tk.Label(root, text= "Email Subject", fg="white", bg="purple")
subject_label.pack(pady=10, side=TOP)
subject_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
subject_entry.pack(side=TOP)

# Email body
body_label = tk.Label(root, text= "Email body", fg="white", bg="purple")
body_label.pack(pady=10)
body_entry = tk.Entry(root, width=100, borderwidth=5, bg="orange")
body_entry.pack(pady=10, ipady=50)

# Send email button
enter = tk.Button(root, text="Send", padx=10, pady=5, fg="white", bg="orange", command=function_calls)
enter.pack(pady=20)

# Stop UI page
root.mainloop()