import tkinter as tk
from tkinter import messagebox
import json
import hashlib
import getpass
import os
from cryptography.fernet import Fernet

# Function for Hashing the Master Password.
def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    return sha256.hexdigest()

# Generate a secret key. This should be done only once as you'll see.
def generate_key():
    return Fernet.generate_key()

# Initialize Fernet cipher with the provided key.
def initialize_cipher(key):
    return Fernet(key)

# Global variable for the cipher
cipher = None

# Function to initialize the cipher
def init_cipher():
    global cipher
    key_filename = 'encryption_key.key'
    if os.path.exists(key_filename):
        with open(key_filename, 'rb') as key_file:
            key = key_file.read()
    else:
        key = generate_key()
        with open(key_filename, 'wb') as key_file:
            key_file.write(key)
    cipher = initialize_cipher(key)
    return cipher

# Function to register a user.
def register(username, master_password):
    hashed_master_password = hash_password(master_password)
    user_data = {'username': username, 'master_password': hashed_master_password}
    file_name = 'user_data.json'
    with open(file_name, 'w+') as file:
        file.truncate()  # Clear the file content
        json.dump(user_data, file)
    messagebox.showinfo("Registration", f"User {username} registered successfully.")

# Function to log a user in.
def login(username, entered_password):
    try:
        with open('user_data.json', 'r') as file:
            user_data = json.load(file)
        stored_password_hash = user_data.get('master_password')
        entered_password_hash = hash_password(entered_password)
        if entered_password_hash == stored_password_hash and username == user_data.get('username'):
            messagebox.showinfo("Login", "Login Successful.")
            # Here you would proceed with other functionalities
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("Password Manager")

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Password label and entry
password_label = tk.Label(root, text="Master Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, show='*', width=30)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Register button
register_button = tk.Button(root, text="Register", command=lambda: register(username_entry.get(), password_entry.get()))
register_button.grid(row=2, column=0, padx=10, pady=10)

# Login button
login_button = tk.Button(root, text="Login", command=lambda: login(username_entry.get(), password_entry.get()))
login_button.grid(row=2, column=1, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
