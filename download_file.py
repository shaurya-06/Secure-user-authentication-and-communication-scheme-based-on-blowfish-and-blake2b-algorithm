from tkinter import *
import pymysql
import hashlib
from password_verifier_generator import function_G
import blowfish
from download_success_display import display_download_success
from download_fail_display import display_download_fail

password_verifier = ""
file_name = ""
hash_value = ""


def display_download_page():
    root = Tk()
    connection = pymysql.connect(host="localhost", user="root", passwd="", database="isaa")
    cursor = connection.cursor()

    def generate_password_verifier():
        global password_verifier
        global hash_value
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

    def search_file():
        global file_name
        retrieve = "Select file_name from files where user_name=%s and file_name=%s;"
        try:
            cursor.execute(retrieve, (username_entry.get(), file_search_entry.get()))
            file_name = cursor.fetchall()[0][0]
            if file_name:
                info_str = "\n\nFile Found!\nFile Name: " + file_name
                info.insert(END, info_str)
        except IndexError:
            info_str = "\n\nFile Not Found! Please Enter correct file name."
            info.insert(END, info_str)

    def decrypt_file():
        global file_name
        file_path = "./Download files/" + file_name
        retrieve = "Select data from files where user_name=%s and file_name=%s;"
        cursor.execute(retrieve, (username_entry.get(), file_name))
        encrypted_file = cursor.fetchall()[0][0]

        with open(file_path, "w") as file:
            key = bytes(decryption_key_entry.get(), "utf-8")
            cipher = blowfish.Cipher(key)
            decrypted_file = b"".join(cipher.decrypt_ecb_cts(encrypted_file))
            decrypted_file = decrypted_file.decode()
            file.write(decrypted_file)

    def hash_file():
        global password_verifier
        global hash_value
        retrieve = "Select data from files where user_name=%s and file_name=%s;"
        cursor.execute(retrieve, (username_entry.get(), file_name))
        encrypted_file = cursor.fetchall()[0][0]
        hasher = hashlib.blake2b(digest_size=4)
        hasher.update((str(encrypted_file) + password_verifier).encode('utf-8'))
        hash_value = hasher.hexdigest()
        hash_value = function_G(str(hash_value))

    def download_file():
        hash_file()
        retrieve = "Select data from files where user_name=%s and file_name=%s;"
        cursor.execute(retrieve, (username_entry.get(), file_name))
        encrypted_file = cursor.fetchall()[0][0]
        retrieve = "Select password_verifier from user_details where user_name=%s;"
        cursor.execute(retrieve, (username_entry.get()))
        password_verifier_server = cursor.fetchall()[0][0]
        hasher = hashlib.blake2b(digest_size=4)
        hasher.update((str(encrypted_file) + password_verifier_server).encode('utf-8'))
        hash_value_server = hasher.hexdigest()
        hash_value_server = function_G(str(hash_value_server))
        if hash_value_server == hash_value:
            decrypt_file()
            connection.close()
            root.destroy()
            display_download_success()
        else:
            connection.close()
            root.destroy()
            display_download_fail()

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

    file_search_label = Label(root, text="Enter File Name:")
    file_search_label.grid(row=4, column=0, pady=5, padx=10)
    file_search_label.config(font=("Arial", 18))
    file_search_entry = Entry(root, width=40, borderwidth=5)
    file_search_entry.grid(row=4, column=1, padx=10, pady=5)
    file_search_button = Button(root, text="Search", command=search_file)
    file_search_button.grid(row=4, column=3, padx=10, pady=5)
    file_search_button.config(font=("Arial", 16))

    decryption_key_label = Label(root, text="Enter Decryption Key:")
    decryption_key_label.grid(row=5, column=0, pady=5, padx=10)
    decryption_key_label.config(font=("Arial", 18))
    decryption_key_entry = Entry(root, width=40, borderwidth=5)
    decryption_key_entry.grid(row=5, column=1, padx=10, pady=5)

    info = Text(root, width=75, height=20, borderwidth=5)
    info.grid(row=6, column=0, padx=10, pady=5, columnspan=3)

    download_button = Button(root, text="Download File", command=download_file)
    download_button.grid(row=6, column=3, padx=10, pady=5)
    download_button.config(font=("Arial", 16))

    quitButton = Button(root, text="Quit!", command=root.destroy)
    quitButton.grid(row=7, column=1, pady=20, columnspan=1)
    quitButton.config(font=("Arial", 18))

    root.mainloop()
