import tkinter as tk
from PIL import Image, ImageTk
import server as sv
import mail as em
from getpass import getpass

root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")

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
enter = tk.Button(root, text="Enter", padx=10, pady=5, fg="white", bg="orange")
enter.pack(pady=30)

root.mainloop()