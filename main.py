from tkinter import *
from user_reg import displayRegistration
from upload_file import display_upload_page
from download_file import display_download_page

root = Tk()
projectName = Label(root, text="ISAA Project")
projectName.grid(row=0, column=1, pady=5, columnspan=1)
projectName.config(width=20)
projectName.config(font=("Arial", 24))

windowHeading = Label(root, text="MAIN PAGE")
windowHeading.grid(row=1, column=1, pady=5, columnspan=1)
windowHeading.config(font=("Arial", 22))

registerButton = Button(root, text="Register", command=displayRegistration)
registerButton.grid(row=5, column=0, pady=5, padx=5, columnspan=1)
registerButton.config(font=("Arial", 18))

uploadButton = Button(root, text="Upload File", command=display_upload_page)
uploadButton.grid(row=5, column=1, pady=5, padx=5, columnspan=1)
uploadButton.config(font=("Arial", 18))

download = Button(root, text="Download File", command=display_download_page)
download.grid(row=5, column=2, pady=5, padx=5, columnspan=1)
download.config(font=("Arial", 18))

quitButton = Button(root, text="Quit!", command=root.destroy)
quitButton.grid(row=6, column=1, pady=20, columnspan=1)
quitButton.config(font=("Arial", 18))

root.mainloop()
