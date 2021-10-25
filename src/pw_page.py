import tkinter as tk
from tkinter import font
from tkinter.constants import BOTH, LEFT, RIGHT, TOP, VERTICAL

root = tk.Tk()
root.title("Skrumpen Mail")
root.configure(bg="purple")
root.geometry("1920x1080")
#root.state("zoomed")

## Left panel
left_panel = tk.PanedWindow(bd=4, relief="raised", bg="orange")
left_panel.pack(fill=BOTH, expand=1)

## Button stack + stack panel
stack = tk.PanedWindow(left_panel, orient=VERTICAL, bd=4, relief="raised", bg="orange")
left_panel.add(stack)

inbox_button = tk.Button(stack, text="Inbox", bg="orange")
stack.add(inbox_button)
deleted_button = tk.Button(stack, text="Deleted Mails", bg="orange")
stack.add(deleted_button)
draft_button = tk.Button(stack, text="Drafts", bg="orange")
stack.add(draft_button)

## Main panel
main_panel = tk.PanedWindow(left_panel, orient=VERTICAL, bd=4, relief="raised", bg="purple", height=1000)
left_panel.add(main_panel)

email_label = tk.Label(text="Here you can write emails", fg="White", font="Helvetica, 20", bg="purple")
main_panel.add(email_label)

# Recipient name
recipient_name_label = tk.Label(text= "Recipient Name", fg="white", bg="purple")
main_panel.add(recipient_name_label)

recipient_name_entry = tk.Entry(width=40, borderwidth=5, bg="orange")
main_panel.add(recipient_name_entry)

# Recipient email adress
recipient_mail_label = tk.Label(text= "Recipient Email Adress", fg="white", bg="purple")
main_panel.add(recipient_mail_label)
recipient_mail_entry = tk.Entry(width=40, borderwidth=5, bg="orange")
main_panel.add(recipient_mail_entry)

# Email subject
subject_label = tk.Label(text= "Email Subject", fg="white", bg="purple")
main_panel.add(subject_label)
subject_entry = tk.Entry(width=40, borderwidth=5, bg="orange")
main_panel.add(subject_entry)

# Email body
body_label = tk.Label(text= "Email body", fg="white", bg="purple")
main_panel.add(body_label)
body_entry = tk.Entry(width=100, borderwidth=5, bg="orange")
main_panel.add(body_entry)

# Send email button
enter = tk.Button(text="Send", padx=10, pady=5, fg="white", bg="orange", height=20, width=20)
main_panel.add(enter)

root.mainloop()
