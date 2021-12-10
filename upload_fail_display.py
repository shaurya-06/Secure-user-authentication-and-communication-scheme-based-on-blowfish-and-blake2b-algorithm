from tkinter import *


def display_upload_fail():
    root = Tk()
    success_message = Label(root, text="Authentication Failed! Please try again with correct details.")
    success_message.grid(row=0, column=0, pady=5, columnspan=3)
    success_message.config(width=50)
    success_message.config(font=("Arial", 24))

    registerButton = Button(root, text="OK", command=root.destroy)
    registerButton.grid(row=1, column=0, pady=20, columnspan=3)
    registerButton.config(font=("Arial", 18))
