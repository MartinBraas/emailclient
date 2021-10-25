import tkinter as tk
from PIL import Image, ImageTk
import server as sv
import mail as em
import variables as v

# Variable and UI initialization
root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")
#root.state("normal")
#root.iconbitmap('../images/small_skrump_icon.ico')

# Functions for changing to the next UI page
def nextPage():
    root.destroy()
    import ui_send_mail
    
# Function for calling numerous functions
def function_calls():
    nextPage()

# def fetch_email():
#     server = sv.Server(0, v.imap_serv, v.port_w_tls, v.port)
#     server.login()
#     server.quit()


# UI page initialization
page = tk.Frame(root)
logo = Image.open('../images/logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.pack( pady=10)

# Button for moving to send email ui page
enter = tk.Button(root, text="Send Email", padx=10, pady=5, fg="white", bg="orange", command=function_calls)
enter.pack(pady=30)

# enter = tk.Button(root, text="Fetch Email", padx=10, pady=5, fg="white", bg="orange", command=fetch_email)
# enter.pack(pady=30)

# Function for stopping UI page
root.mainloop()