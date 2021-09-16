import tkinter as tk
from tkinter.constants import LEFT, RIGHT
from PIL import Image, ImageTk
import server as sv
import mail as em
import variables

v = variables

root = tk.Tk()
root.title("Advanced")
root.configure(bg="purple")

advanced_smtp = "a"
advanced_port = 0

def save_advanced():
    global advanced_smtp, advanced_port
    advanced_smtp = advanced_smtp_entry.get()
    advanced_port = advanced_port_entry.get()

def next():
    root.destroy()
    import GUI_login_page

def save_settings():
    save_advanced()
    v.choose_smtp(2, advanced_smtp, advanced_port)
    next()

#logo
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

# Save settings
save_settings_button = tk.Button(root, text="Save settings", padx=10, pady=5, bg="orange", command=save_settings)
save_settings_button.pack(pady=30)

