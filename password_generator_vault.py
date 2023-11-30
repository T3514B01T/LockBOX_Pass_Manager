import tkinter as tk
from tkinter import messagebox
import random
import string
from cryptography.fernet import Fernet
import json
import os

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Function to generate a random password
def generate_password():
    length = 12  # Adjust the password length as needed
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

# Function to save an encrypted password
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

# Function to retrieve passwords
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

# Function to register a new user
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

# Function to authenticate the user
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

# Function to switch to the registration frame
def show_registration_frame():
    login_frame.pack_forget()
    registration_frame.pack()

# Function to switch to the login frame
def show_login_frame():
    registration_frame.pack_forget()
    login_frame.pack()

# Function to switch to the main application frame
def show_main_frame():
    login_frame.pack_forget()
    registration_frame.pack_forget()
    main_frame.pack()

# Create the main window
root = tk.Tk()
root.title("LOCK BOX")
root.geometry("1920x1080")  # Set the window size

# Generate and store a key for encryption
key = generate_key()

# Check if users.json exists; if not, create it with example users
if not os.path.isfile('users.json'):
    example_users = {
        "user1": "password1",
        "user2": "password2",
        "user3": "password3"
    }

    with open('users.json', 'w') as user_file:
        json.dump(example_users, user_file)

# Create frames for different sections
registration_frame = tk.Frame(root)
login_frame = tk.Frame(root)
main_frame = tk.Frame(root)

# Create and place labels and entry fields for registration
font_style = ("Poppins", 14)  # Font style for labels and entry fields
button_style = ("Poppins", 12, "bold")  # Font style for buttons

register_username_label = tk.Label(registration_frame, text="Username:", font=font_style)
register_username_label.pack()
register_username_entry = tk.Entry(registration_frame, font=font_style)
register_username_entry.pack()

register_password_label = tk.Label(registration_frame, text="Password:", font=font_style)
register_password_label.pack()
register_password_entry = tk.Entry(registration_frame, show="*", font=font_style)
register_password_entry.pack()

register_button = tk.Button(registration_frame, text="Register", command=register_user, font=button_style, bg="green", fg="white")
register_button.pack()

switch_to_login_button = tk.Button(registration_frame, text="Already have an account? Login", command=show_login_frame, font=button_style)
switch_to_login_button.pack()

# Create and place labels and entry fields for login
login_username_label = tk.Label(login_frame, text="Username:", font=font_style)
login_username_label.pack()
login_username_entry = tk.Entry(login_frame, font=font_style)
login_username_entry.pack()

login_password_label = tk.Label(login_frame, text="Password:", font=font_style)
login_password_label.pack()
login_password_entry = tk.Entry(login_frame, show="*", font=font_style)
login_password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=login_user, font=button_style, bg="blue", fg="white")
login_button.pack()

switch_to_registration_button = tk.Button(login_frame, text="Don't have an account? Register", command=show_registration_frame, font=button_style)
switch_to_registration_button.pack()

# Create and place labels and entry fields for the main application
website_label = tk.Label(main_frame, text="Website:", font=font_style)
website_label.pack()
website_entry = tk.Entry(main_frame, font=font_style)
website_entry.pack()

username_label = tk.Label(main_frame, text="Username:", font=font_style)
username_label.pack()
username_entry = tk.Entry(main_frame, font=font_style)
username_entry.pack()

password_label = tk.Label(main_frame, text="Password:", font=font_style)
password_label.pack()
password_entry = tk.Entry(main_frame, font=font_style)
password_entry.pack()

# Create buttons for generating, saving, and retrieving passwords
generate_button = tk.Button(main_frame, text="Generate Password", command=generate_password, font=button_style, bg="blue", fg="white")
generate_button.pack()

save_button = tk.Button(main_frame, text="Save Password", command=save_password, font=button_style, bg="green", fg="white")
save_button.pack()

retrieve_button = tk.Button(main_frame, text="Retrieve Password", command=retrieve_password, font=button_style, bg="blue", fg="white")
retrieve_button.pack()

# Initially, show the registration frame
show_registration_frame()

# Start the Tkinter main loop
root.mainloop()
