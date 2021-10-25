import tkinter as tk
from tkinter.constants import LEFT, RIGHT
from PIL import Image, ImageTk
import server as sv
import mail as em
import variables

# Initialization
v = variables
root = tk.Tk()
root.title("Advanced")
root.configure(bg="purple")

# Variable initialization
advanced_smtp = "a"
advanced_port = 0
advanced_imap = "a"
advanced_im_port = 0

# Saves variables passed from UI, to pass to other functions
def save_advanced():
    global advanced_smtp, advanced_port, advanced_imap, advanced_im_port
    advanced_smtp = advanced_smtp_entry.get()
    advanced_port = advanced_port_entry.get()
    advanced_imap = advanced_imap_entry.get()
    advanced_im_port = advanced_im_port_entry.get()
    

# Next page function. Open next UI page
def next():
    root.destroy()
    import GUI_login_page

# executes functions at push of button
def save_settings():
    save_advanced()
    v.choose_smtp(2, advanced_smtp, advanced_port)
    v.choose_imap(2, advanced_imap, advanced_im_port)
    next()

# Start of UI page
page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack(pady=10)

# SMTP Server
advanced_smtp_label = tk.Label(root, text= "SMTP Server", fg="white", bg="purple")
advanced_smtp_label.pack(pady=10)
advanced_smtp_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
advanced_smtp_entry.pack(pady=5)

# SMTP port
advanced_port_label = tk.Label(root, text= "TSL Port", fg="white", bg="purple")
advanced_port_label.pack(pady=10)
advanced_port_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
advanced_port_entry.pack(pady=5)

# IMAP Server
advanced_imap_label = tk.Label(root, text= "IMAP Server", fg="white", bg="purple")
advanced_imap_label.pack(pady=10)
advanced_imap_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
advanced_imap_entry.pack(pady=5)

# IMAP Port
advanced_im_port_label = tk.Label(root, text= "IMAP Port", fg="white", bg="purple")
advanced_im_port_label.pack(pady=10)
advanced_im_port_entry = tk.Entry(root, width=40, borderwidth=5, bg="orange")
advanced_im_port_entry.pack(pady=5)

# Save settings
save_settings_button = tk.Button(root, text="Save settings", padx=10, pady=5, bg="orange", command=save_settings)
save_settings_button.pack(pady=30)

