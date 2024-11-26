# Modules
import base64
import bcrypt
import secrets
import tkinter as tk
import datetime as dt
from tkinter import *
from cryptography.fernet import Fernet

user_input = bytes(input("Please enter the 32-character key you would like to use for encryption/decryption: "), "utf-8")
key = base64.urlsafe_b64encode(user_input)

def generate():
    secure_pass = secrets.token_bytes(32)
    time_of_creation = dt.datetime.now()

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(secure_pass, salt)

    with open(r"Password.txt", "a+", encoding="utf-8") as f:
        f.write("\n" + str(hash) + " at " + str(time_of_creation) + "\n")

        line = f.read()

        while line != '':
            continue

    confirm = Label(root, text='Password Generated')
    confirm.place(x=2.5, y=30)

def encrypt_file():    
    fernet = Fernet(key)
    time_of_encryption = dt.datetime.now()


    with open(r"Password.txt", "rb") as f:
        normal = f.read()

    encrypted = fernet.encrypt(normal)

    with open(r"Password.txt", "wb") as l:
        l.write(encrypted + bytes(str(time_of_encryption), "utf-8"))

    file_encrypted = Label(root, text='File Encrypted')
    file_encrypted.place(x=2.5, y=100)

def decrypt_file():
    fernet = Fernet(key)

    with open(r"Password.txt", "rb") as f:
        encrypted = f.read()
        
    decrypted = fernet.decrypt(encrypted)
    
    with open(r"Password.txt", "wb") as l:
        l.write(decrypted)
    
    file_decrypted = Label(root, text='File Decrypted')
    file_decrypted.place(x=2.5, y=100)

root = Tk()
root.title("Secure Password Generator")
root.geometry('400x250+50+50')

make_pass = tk.Button(root, text='Generate Password', command=lambda: generate())
file_encrypt = tk.Button(root, text='Encrypt File', command=lambda: encrypt_file())
file_decrypt = tk.Button(root, text='Decrypt File', command=lambda: decrypt_file())

make_pass.place(x=5, y=5)
file_encrypt.place(x=5, y=75)
file_decrypt.place(x=100, y=75)

root.mainloop()