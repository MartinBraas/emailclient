import tkinter as tk
from PIL import Image, ImageTk
import server as sv
import mail as em
import variables
from getpass import getpass

v = variables

# gui_login = GUI_login_page
# smtpserv = gui_login.smtpserv
# port_w_tls = gui_login.port_w_tls
# port = gui_login.port

root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")

#How to send a mail and server config
def sendemail():
    print("letsgo")
    # SMTP SERVER

    server = sv.Server(v.smtp_serv, v.port_w_tls, v.port)
    server.connect()

    email = em.Email()
    with open('../message.txt', 'r') as f:
        message = f.read()
    email.setBody(message)

    email.setRecipient('Martin 2', 'koentimmy@hotmail.com')

    email.setSubject('Din mor')

    server.login(v.email_adress, v.email_password)

    server.send(v.email_adress, 'koentimmy@hotmail.com', email.getString())

    server.quit()

def function_calls():
    root.destroy()
    sendemail()
    

page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack(pady=10)

# Username label and entry
# username_label = tk.Label(root, text= "E-mail", fg="white", bg="purple")
# username_label.pack(pady=10)
# username_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
# username_entry.pack(pady=5)

# Password label and entry
# password_label = tk.Label(root, text= "Password", fg="white", bg="purple")
# password_label.pack(pady=10)
# password_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange", show="*")
# password_entry.pack(pady=5)

# Button for login
enter = tk.Button(root, text="Send", padx=10, pady=5, fg="white", bg="orange", command=function_calls)
enter.pack(pady=30)

root.mainloop()