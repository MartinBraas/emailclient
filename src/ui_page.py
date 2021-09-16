import tkinter as tk
from PIL import Image, ImageTk
import server as sv
import mail as em

# Variable and UI initialization
root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")
root.state("zoomed")
root.iconbitmap('../images/small_skrump_icon.ico')

# Functions for changing to the next UI page
def nextPage():
    root.destroy()
    import ui_send_mail
    
# Function for calling numerous functions
def function_calls():
    nextPage()

# UI page initialization
page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack( pady=10)

# Button for login
enter = tk.Button(root, text="Send Email", padx=10, pady=5, fg="white", bg="orange", command=function_calls)
enter.pack(pady=30)

# Function for stopping UI page
root.mainloop()