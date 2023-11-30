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
    website = website_entry.get().strip().lower()
    if website:
        cipher_suite = Fernet(key)
        with open('passwords.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                normalized_line = line.lower()
                if f"Website: {website}" in normalized_line:
                    print(f"Found line: {normalized_line}")
                    encrypted_password = normalized_line.split("|")[2].strip()
                    decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
                    messagebox.showinfo("Password Retrieval", f"Password for {website}: {decrypted_password}")
                    return
            print(f"Website not found: {website}")
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
    clear_frame_content()
    login_frame.pack_forget()
    registration_frame.pack(expand=True, fill='both')

def show_login_frame():
    clear_frame_content()
    registration_frame.pack_forget()
    login_frame.pack(expand=True, fill='both')

def show_main_frame():
    clear_frame_content()
    login_frame.pack_forget()
    registration_frame.pack_forget()
    main_frame.pack(expand=True, fill='both')

def clear_frame_content():
    for widget in registration_frame.winfo_children():
        widget.destroy()

    for widget in login_frame.winfo_children():
        widget.destroy()

    for widget in main_frame.winfo_children():
        widget.destroy()

def go_back():
    # Determine the current frame and go back accordingly
    current_frame = root.nametowidget(root.winfo_currentid())
    current_frame.pack_forget()

    if current_frame == registration_frame:
        show_login_frame()
    elif current_frame == login_frame:
        show_registration_frame()

root = tk.Tk()
root.title("LOCK BOX")
root.geometry("1000x480")

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

# ... (unchanged code)

# Add a back button to the left side of the interface
back_button = ttk.Button(main_frame, text="Back", command=go_back, style="TButton")
back_button.pack(side=tk.LEFT, padx=20, pady=10)

# ... (unchanged code)

show_registration_frame()

root.mainloop()
