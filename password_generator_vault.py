import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
from cryptography.fernet import Fernet
import json
import os
from ttkthemes import ThemedStyle

def generate_key():
    return Fernet.generate_key()

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if website and username and password:
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(password.encode())
        
        with open('passwords.txt', 'a') as file:
            file.write(f"Website: {website} | Username: {username} | Password: {encrypted_password.decode()}\n")
        website_entry.delete(0, tk.END)
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Password saved successfully!")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def retrieve_password():
    website = website_entry.get()
    if website:
        cipher_suite = Fernet(key)
        with open('passwords.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if f"Website: {website}" in line:
                    encrypted_password = line.split("|")[2].strip()
                    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                    messagebox.showinfo("Password Retrieval", f"Password for {website}: {decrypted_password}")
                    return
        messagebox.showerror("Error", f"No password found for {website}")
    else:
        messagebox.showerror("Error", "Please enter the website for which you want to retrieve the password.")

def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()

    if username and password:
        with open('users.json', 'r') as user_file:
            users = json.load(user_file)

        if username not in users:
            users[username] = password
            with open('users.json', 'w') as user_file:
                json.dump(users, user_file)
            messagebox.showinfo("Success", "Registration successful!")
            show_login_frame()
        else:
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    with open('users.json', 'r') as user_file:
        users = json.load(user_file)

    if username in users and users[username] == password:
        messagebox.showinfo("Success", "Login successful!")
        show_main_frame()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def show_registration_frame():
    login_frame.pack_forget()
    registration_frame.pack(expand=True, fill='both')

def show_login_frame():
    registration_frame.pack_forget()
    login_frame.pack(expand=True, fill='both')

def show_main_frame():
    login_frame.pack_forget()
    registration_frame.pack_forget()
    main_frame.pack(expand=True, fill='both')

root = tk.Tk()
root.title("LOCK BOX")
root.geometry("1920x1080")

key = generate_key()

if not os.path.isfile('users.json'):
    example_users = {
        "user1": "password1",
        "user2": "password2",
        "user3": "password3"
    }

    with open('users.json', 'w') as user_file:
        json.dump(example_users, user_file)

style = ThemedStyle(root)
style.set_theme("equilux")

registration_frame = ttk.Frame(root)
login_frame = ttk.Frame(root)
main_frame = ttk.Frame(root)

font_style = ("Poppins", 15)
button_style = ("Poppins", 12, "bold")

register_username_label = ttk.Label(registration_frame, text="Username:", font=font_style)
register_username_label.pack(padx=20, pady=10)
register_username_entry = ttk.Entry(registration_frame, font=font_style)
register_username_entry.pack(padx=20, pady=10)

register_password_label = ttk.Label(registration_frame, text="Password:", font=font_style)
register_password_label.pack(padx=20, pady=10)
register_password_entry = ttk.Entry(registration_frame, show="*", font=font_style)
register_password_entry.pack(padx=20, pady=10)

register_button = ttk.Button(registration_frame, text="Register", command=register_user, style="TButton")
register_button.pack(pady=20)

switch_to_login_button = ttk.Button(registration_frame, text="Already have an account? Login", command=show_login_frame, style="TButton")
switch_to_login_button.pack(pady=10)

login_username_label = ttk.Label(login_frame, text="Username:", font=font_style)
login_username_label.pack(padx=20, pady=10)
login_username_entry = ttk.Entry(login_frame, font=font_style)
login_username_entry.pack(padx=20, pady=10)

login_password_label = ttk.Label(login_frame, text="Password:", font=font_style)
login_password_label.pack(padx=20, pady=10)
login_password_entry = ttk.Entry(login_frame, show="*", font=font_style)
login_password_entry.pack(padx=20, pady=10)

login_button = ttk.Button(login_frame, text="Login", command=login_user, style="TButton")
login_button.pack(pady=20)

switch_to_registration_button = ttk.Button(login_frame, text="Don't have an account? Register", command=show_registration_frame, style="TButton")
switch_to_registration_button.pack(pady=10)

website_label = ttk.Label(main_frame, text="Website:", font=font_style)
website_label.pack(padx=20, pady=10)
website_entry = ttk.Entry(main_frame, font=font_style)
website_entry.pack(padx=20, pady=10)

username_label = ttk.Label(main_frame, text="Username:", font=font_style)
username_label.pack(padx=20, pady=10)
username_entry = ttk.Entry(main_frame, font=font_style)
username_entry.pack(padx=20, pady=10)

password_label = ttk.Label(main_frame, text="Password:", font=font_style)
password_label.pack(padx=20, pady=10)
password_entry = ttk.Entry(main_frame, font=font_style)
password_entry.pack(padx=20, pady=10)

generate_button = ttk.Button(main_frame, text="Generate Password", command=generate_password, style="TButton")
generate_button.pack(pady=10)

save_button = ttk.Button(main_frame, text="Save Password", command=save_password, style="TButton")
save_button.pack(pady=10)

retrieve_button = ttk.Button(main_frame, text="Retrieve Password", command=retrieve_password, style="TButton")
retrieve_button.pack(pady=10)

show_registration_frame()

root.mainloop()
