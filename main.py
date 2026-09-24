import base64
import secrets
import tkinter as tk
import datetime as dt
from cryptography.fernet import Fernet
from cryptography import fernet
from cryptography import exceptions


key = None
BYTES = 32


def message(text):
    msg = tk.Label(root, text=text)
    msg.pack()
    msg.after(3000, lambda: msg.destroy())


def get_key():
    entered_key = key_input.get("1.0", "end-1c").strip(" ")

    if len(entered_key) == BYTES:
        converted_key = bytes(entered_key, "utf-8")

        global key
        key = base64.urlsafe_b64encode(converted_key)

        key_input.destroy()
        enter_key.destroy()

    else:
        message("The inputted key must be exactly 32 characters!")


def generate():
    secure_pass = secrets.token_urlsafe(BYTES)
    time_of_creation = dt.datetime.now()

    try:
        with open(r"Password.txt", "a", encoding="utf-8") as f:
            f.write("\n" + str(secure_pass) + " at " + str(time_of_creation) + "\n")

        message("Password Generated: " + str(secure_pass))

    except PermissionError:
        message("Couldn't access file, permission denied")


def encrypt_file():
    try:
        fernet_key = Fernet(key)

        with open(r"Password.txt", "rb") as f:
            normal = f.read()

        encrypted = fernet_key.encrypt(normal)

        with open(r"Password.txt", "wb") as f:
            f.write(encrypted)

        message("File Encrypted")

    except TypeError:
        message("There is no key for encryption!")
    except FileNotFoundError:
        message("The file does not exist!")
    except PermissionError:
        message("Couldn't access file, permission denied")


def decrypt_file():
    try:
        fernet_key = Fernet(key)

        with open(r"Password.txt", "rb") as f:
            encrypted = f.read()

        decrypted = fernet_key.decrypt(encrypted)

        with open(r"Password.txt", "wb") as f:
            f.write(decrypted)

        message("File Decrypted")

    except TypeError:
        message("There is no key for decryption!")
    except fernet.InvalidToken:
        message("Cannot decrypt an unencrypted text file!")
    except exceptions.InvalidSignature:
        message("The key is not the same!")
    except FileNotFoundError:
        message("The file does not exist!")
    except PermissionError:
        message("Couldn't access file, permission denied")


def show_passwords():
    try:
        with open(r"Password.txt", 'r') as file:
            content = file.read()

            file.close()

        pass_window = tk.Toplevel(root)
        pass_window.title("Passwords")
        pass_window.geometry("800x800+50+50")

        pass_display = tk.Text(pass_window, height=750, width=750)
        pass_display.insert("1.0", content)
        pass_display.configure(state="disabled")
        pass_display.pack()

    except FileNotFoundError:
        message("The file does not exist!")
    except PermissionError:
        message("Couldn't access file, permission denied")


root = tk.Tk()
root.title("Secure Password Generator")
root.geometry('600x300+50+50')

key_input = tk.Text(root, height=1.0, width=50)
enter_key = tk.Button(root, text="Enter", command=lambda: get_key())

key_input.pack()
enter_key.pack()

make_pass = tk.Button(root, text='Generate Password', command=lambda: generate())
show_pass = tk.Button(root, text='Show Password', command=lambda: show_passwords())
file_encrypt = tk.Button(root, text='Encrypt File', command=lambda: encrypt_file())
file_decrypt = tk.Button(root, text='Decrypt File', command=lambda: decrypt_file())

make_pass.pack()
show_pass.pack()
file_encrypt.pack()
file_decrypt.pack()

root.mainloop()
