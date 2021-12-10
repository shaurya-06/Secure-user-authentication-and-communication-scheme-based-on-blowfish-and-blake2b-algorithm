from tkinter import *


def display_download_success():
    root = Tk()
    success_message = Label(root, text="Authentication was Successful! File Decrypted and Downloaded Successfully.")
    success_message.grid(row=0, column=0, pady=5, columnspan=3)
    success_message.config(width=75)
    success_message.config(font=("Arial", 24))

    registerButton = Button(root, text="OK", command=root.destroy)
    registerButton.grid(row=1, column=0, pady=20, columnspan=3)
    registerButton.config(font=("Arial", 18))
