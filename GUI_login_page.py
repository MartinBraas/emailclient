import tkinter as tk
from PIL import Image, ImageTk

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

def OpenNewWindow():
    global UI
    UI = tk.Toplevel(root)
    UI.title("Skrumpen Mail")
    UI.geometry("750x400")
    UI.configure(bg="purple")
    UI_label = tk.Label(UI, text="Skrumpen Mail", font='Helvetica, 20', bg="purple", fg="white")
    UI_label.pack()


def function_call():
    save()
    print_value()
    OpenNewWindow()

#logo
logo = Image.open('logo.png')
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

enter = tk.Button(root, text="Enter", padx=10, pady=5, fg="white", bg="orange", command=function_call)
enter.pack(pady=30)



root.mainloop()