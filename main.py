# Modules
import base64
import bcrypt
import secrets
import tkinter as tk
import datetime as dt
from tkinter import *
import cryptography as crypt
from cryptography.fernet import Fernet

def get_key():
    entered_key = key_input.get("1.0", "end-1c")
    
    if len(entered_key) == 32:
        converted_key = bytes(entered_key, "utf-8")

        global key
        key = base64.urlsafe_b64encode(converted_key)

        root.destroy()

    elif len(entered_key) != 32:
        error_msg = Label(root, text="The inputted key must be exactly 32 characters!")
        error_msg.place(x=125, y=90)
        error_msg.after(3000, lambda: error_msg.destroy())

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
    confirm.after(3000, lambda: confirm.destroy())

def encrypt_file():
    try:
        fernet = Fernet(key)
        time_of_encryption = dt.datetime.now()


        with open(r"Password.txt", "rb") as f:
            normal = f.read()

        encrypted = fernet.encrypt(normal)

        with open(r"Password.txt", "wb") as l:
            l.write(encrypted + bytes(str(time_of_encryption), "utf-8"))

        file_encrypted = Label(root, text='File Encrypted')
        file_encrypted.place(x=2.5, y=100)
        file_encrypted.after(3000, lambda: file_encrypted.destroy())
    except NameError:
        error_msg2 = Label(root, text="There is no key for encryption!")
        error_msg2.place(x=2.5, y=100)
        error_msg2.after(3000, lambda: error_msg2.destroy())
    except FileNotFoundError:
        error_msg5 = Label(root, text="The file does not exist!")
        error_msg5.place(x=2.5, y=100)
        error_msg5.after(3000, lambda: error_msg5.destroy())

def decrypt_file():
    try:
        fernet = Fernet(key)

        with open(r"Password.txt", "rb") as f:
            encrypted = f.read()
            
        decrypted = fernet.decrypt(encrypted)
        
        with open(r"Password.txt", "wb") as l:
            l.write(decrypted)
        
        file_decrypted = Label(root, text='File Decrypted')
        file_decrypted.place(x=2.5, y=100)
        file_decrypted.after(3000, lambda: file_decrypted.destroy())
    except NameError:
        error_msg2 = Label(root, text="There is no key for decryption!")
        error_msg2.place(x=2.5, y=100)
        error_msg2.after(3000, lambda: error_msg2.destroy())
    except crypt.fernet.InvalidToken:
        error_msg3 = Label(root, text="Cannot decrypt an unencrypted text file!")
        error_msg3.place(x=2.5, y=100)
        error_msg3.after(3000, lambda: error_msg3.destroy())
    except crypt.exceptions.InvalidSignature:
        error_msg4 = Label(root, text="The key is not the same!")
        error_msg4.place(x=2.5, y=100)
        error_msg4.after(3000, lambda: error_msg4.destroy())
    except FileNotFoundError:
        error_msg5 = Label(root, text="The file does not exist!")
        error_msg5.place(x=2.5, y=100)
        error_msg5.after(3000, lambda: error_msg5.destroy())

root = Tk()
root.title("Secure Password Generator")
root.geometry('600x250+50+50')

statement = Label(text="Please enter the 32-character key you would like to use for encryption/decryption: ")
key_input = Text(root, height=2.5 , width=50)
enter_key = Button(root, text="Enter", command=lambda: get_key())

statement.pack()
key_input.pack()
enter_key.pack()

root.mainloop()

root = Tk()
root.title("Secure Password Generator")
root.geometry('500x250+50+50')

make_pass = tk.Button(root, text='Generate Password', command=lambda: generate())
file_encrypt = tk.Button(root, text='Encrypt File', command=lambda: encrypt_file())
file_decrypt = tk.Button(root, text='Decrypt File', command=lambda: decrypt_file())

make_pass.place(x=5, y=5)
file_encrypt.place(x=5, y=75)
file_decrypt.place(x=100, y=75)


root.mainloop()
