from tkinter import *
import pymysql
import hashlib
from password_verifier_generator import function_G
import blowfish
from upload_success_display import display_upload_success
from upload_fail_display import display_upload_fail

encrypted_file = ""
password_verifier = ""
hash_value = ""


def display_upload_page():
    root = Tk()
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="isaa")
    cursor = connection.cursor()

    def generate_password_verifier():
        global password_verifier
        retrieve = "Select salt from user_details where user_name=%s;"
        username = username_entry.get()
        password = password_entry.get()
        try:
            if username == "" or password == "":
                raise RuntimeError
            data = (username)
            cursor.execute(retrieve, data)
            salt = cursor.fetchall()[0][0]
            hasher = hashlib.blake2b(digest_size=4)
            hasher.update(str(salt + username + password).encode('utf-8'))
            hash_value = hasher.hexdigest()
            password_verifier = function_G(str(hash_value))
            password_verifier_entry.insert(0, password_verifier)
            info_str = "User Name: " + username
            info.insert(END, info_str)
        except RuntimeError:
            username_entry.delete(0, END)
            username_entry.insert(0, "PLEASE ENTER A USERNAME")
            password_entry.delete(0, END)
            password_entry.insert(0, "PLEASE ENTER A PASSWORD")

    def encrypt_file():
        global encrypted_file
        file_path = file_upload_entry.get()
        try:
            with open(file_path, "rb") as file:
                data = file.read()
                key = bytes(encryption_key_entry.get(), "utf-8")
                cipher = blowfish.Cipher(key)
                encrypted_file = b"".join(cipher.encrypt_ecb_cts(data))
                info_str = "\n\nFile Name: " + file_path + "\nSample of Encrypted file:\n" + str(encrypted_file[0:50]) + "\n"
                info.insert(END, info_str)
        except FileNotFoundError:
            file_upload_entry.delete(0, END)
            file_upload_entry.insert(0, "PLEASE SELECT A VALID FILE")

    def hash_file():
        global encrypted_file
        global password_verifier
        global hash_value
        hasher = hashlib.blake2b(digest_size=4)
        hasher.update((str(encrypted_file) + password_verifier).encode('utf-8'))
        hash_value = hasher.hexdigest()
        hash_value = function_G(str(hash_value))
        info_str = "\nHash Value of Encrypted File: " + hash_value
        info.insert(END, info_str)

    def upload_file():
        global encrypted_file
        global hash_value
        retrieve = "Select password_verifier from user_details where user_name=%s;"
        cursor.execute(retrieve, (username_entry.get()))
        password_verifier_server = cursor.fetchall()[0][0]
        hasher = hashlib.blake2b(digest_size=4)
        hasher.update((str(encrypted_file) + password_verifier_server).encode('utf-8'))
        hash_value_server = hasher.hexdigest()
        hash_value_server = function_G(str(hash_value_server))
        if hash_value_server == hash_value:
            inp_query = "Insert into files(user_name, file_name, data, verifier) values (%s, %s, %s, %s);"
            data = (username_entry.get(), file_upload_entry.get().split("/")[-1], encrypted_file, hash_value)
            cursor.execute(inp_query, data)
            connection.commit()
            connection.close()
            root.destroy()
            display_upload_success()
        else:
            connection.close()
            root.destroy()
            display_upload_fail()

    username_label = Label(root, text="Username*:")
    username_label.grid(row=1, column=0, pady=5, padx=10)
    username_label.config(font=("Arial", 18))
    username_entry = Entry(root, width=40, borderwidth=5)
    username_entry.grid(row=1, column=1, padx=10, pady=5)

    password_label = Label(root, text="Password*:")
    password_label.grid(row=2, column=0, pady=5, padx=10)
    password_label.config(font=("Arial", 18))
    password_entry = Entry(root, width=40, borderwidth=5)
    password_entry.grid(row=2, column=1, padx=10, pady=5)

    password_verifier_label = Label(root, text="Your Password Verifier:")
    password_verifier_label.grid(row=3, column=0, pady=5, padx=10)
    password_verifier_label.config(font=("Arial", 18))
    password_verifier_entry = Entry(root, width=40, borderwidth=5)
    password_verifier_entry.grid(row=3, column=1, padx=10, pady=5)
    password_verifier_button = Button(root, text="GET", command=generate_password_verifier)
    password_verifier_button.grid(row=3, column=3, padx=10, pady=5)
    password_verifier_button.config(font=("Arial", 16))

    file_upload_label = Label(root, text="File Path:")
    file_upload_label.grid(row=4, column=0, pady=5, padx=10)
    file_upload_label.config(font=("Arial", 18))
    file_upload_entry = Entry(root, width=40, borderwidth=5)
    file_upload_entry.grid(row=4, column=1, padx=10, pady=5)

    encryption_key_label = Label(root, text="Enter Encryption key:")
    encryption_key_label.grid(row=5, column=0, pady=5, padx=10)
    encryption_key_label.config(font=("Arial", 18))
    encryption_key_entry = Entry(root, width=40, borderwidth=5)
    encryption_key_entry.grid(row=5, column=1, padx=10, pady=5)
    encryption_key_button = Button(root, text="Encrypt", command=encrypt_file)
    encryption_key_button.grid(row=5, column=3, padx=10, pady=5)
    encryption_key_button.config(font=("Arial", 16))

    hash_label = Label(root, text="Enter Hash key:")
    hash_label.grid(row=6, column=0, pady=5, padx=10)
    hash_label.config(font=("Arial", 18))
    hash_entry = Entry(root, width=40, borderwidth=5)
    hash_entry.grid(row=6, column=1, padx=10, pady=5)
    hash_button = Button(root, text="Hashing", command=hash_file)
    hash_button.grid(row=6, column=3, padx=10, pady=5)
    hash_button.config(font=("Arial", 16))

    info = Text(root, width=75, height=20, borderwidth=5)
    info.grid(row=7, column=0, padx=10, pady=5, columnspan=3)

    upload_button = Button(root, text="Upload File", command=upload_file)
    upload_button.grid(row=7, column=3, padx=10, pady=5)
    upload_button.config(font=("Arial", 16))

    quitButton = Button(root, text="Quit!", command=root.destroy)
    quitButton.grid(row=8, column=1, pady=20, columnspan=1)
    quitButton.config(font=("Arial", 18))

    root.mainloop()
