import base64
import secrets
import tkinter as tk
import datetime as dt
import cryptography as crypt
from cryptography.fernet import Fernet

global key
BYTES = 32


def get_key():
    entered_key = key_input.get("1.0", "end-1c")

    if len(entered_key) == BYTES:
        converted_key = bytes(entered_key, "utf-8")

        global key
        key = base64.urlsafe_b64encode(converted_key)

        root.destroy()

    else:
        message("The inputted key must be exactly 32 characters!", 125, 90)


def generate():
    secure_pass = secrets.token_bytes(BYTES)
    time_of_creation = dt.datetime.now()

    try:
        with open(r"Password.txt", "a", encoding="utf-8") as f:
            f.write("\n" + str(secure_pass) + " at " + str(time_of_creation) + "\n")

        message("Password Generated: " + str(secure_pass), 2.5, 30)
    except PermissionError:
        message("Couldn't access file, permission denied", 2.5, 30)


def encrypt_file():
    try:
        fernet = Fernet(key)

        with open(r"Password.txt", "rb") as f:
            normal = f.read()

        encrypted = fernet.encrypt(normal)

        with open(r"Password.txt", "wb") as f:
            f.write(encrypted)

        message("File Encrypted", 2.5, 100)
    except NameError:
        message("There is no key for encryption!", 2.5, 100)
    except FileNotFoundError:
        message("The file does not exist!", 2.5, 100)
    except PermissionError:
        message("Couldn't access file, permission denied", 2.5, 100)


def message(text, x, y):
    msg = tk.Label(root, text=text)
    msg.place(x=x, y=y)
    msg.after(3000, lambda: msg.destroy())


def decrypt_file():
    try:
        fernet = Fernet(key)

        with open(r"Password.txt", "rb") as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted)

        with open(r"Password.txt", "wb") as f:
            f.write(decrypted)

        message("File Decrypted", 2.5, 100)
    except NameError:
        message("There is no key for decryption!", 2.5, 100)
    except crypt.fernet.InvalidToken:
        message("Cannot decrypt an unencrypted text file!", 2.5, 100)
    except crypt.exceptions.InvalidSignature:
        message("The key is not the same!", 2.5, 100)
    except FileNotFoundError:
        message("The file does not exist!", 2.5, 100)
    except PermissionError:
        message("Couldn't access file, permission denied", 2.5, 100)


root = tk.Tk()
root.title("Secure Password Generator")
root.geometry('600x250+50+50')

statement = tk.Label(text="Please enter the 32-character key you would like to use for encryption/decryption: ")
key_input = tk.Text(root, height=2.5, width=50)
enter_key = tk.Button(root, text="Enter", command=lambda: get_key())

statement.pack()
key_input.pack()
enter_key.pack()

root.mainloop()

root = tk.Tk()
root.title("Secure Password Generator")
root.geometry('500x250+50+50')

make_pass = tk.Button(root, text='Generate Password', command=lambda: generate())
file_encrypt = tk.Button(root, text='Encrypt File', command=lambda: encrypt_file())
file_decrypt = tk.Button(root, text='Decrypt File', command=lambda: decrypt_file())

make_pass.place(x=5, y=5)
file_encrypt.place(x=5, y=75)
file_decrypt.place(x=120, y=75)

root.mainloop()
