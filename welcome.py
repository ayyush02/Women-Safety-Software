import tkinter as tk
from tkinter import messagebox
import json
import os

# Create the main window first
root = tk.Tk()
root.title("SafeGuard")
root.geometry("350x700")  # Mobile-like dimensions
root.configure(bg="#000000")

# Function to open index.py
def open_index():
    root.destroy()  # Now 'root' is defined before calling this function
    os.system(f"python \"{os.path.abspath('index.py')}\"")

# Check if user_data.json exists at startup
if os.path.exists("user_data.json"):
    root.after(100, open_index)  # Ensures root is fully initialized before destroying

def save_user_data():
    user_data = {
        "name": entry_name.get(),
        "aadhar": entry_aadhar.get(),
        "gender": gender_var.get(),
        "email": entry_email.get(),
        "family_contacts": [entry_contact1.get(), entry_contact2.get(), entry_contact3.get()]
    }
    if "" in user_data.values() or "" in user_data["family_contacts"]:
        messagebox.showerror("Error", "All fields are required!")
        return
    with open("user_data.json", "w") as f:
        json.dump(user_data, f, indent=4)
    messagebox.showinfo("Success", "User information saved successfully!")
    open_index()

def open_user_info_window():
    global entry_name, entry_aadhar, gender_var, entry_email, entry_contact1, entry_contact2, entry_contact3
    user_info_window = tk.Toplevel(root)
    user_info_window.title("User Information")
    user_info_window.geometry("350x700")
    user_info_window.configure(bg="#000000")

    def create_entry(parent, label_text):
        tk.Label(parent, text=label_text, font=("Arial", 10, "bold"), fg="#00ffcc", bg="#000000").pack(pady=2)
        entry = tk.Entry(parent, width=30, font=("Arial", 12), fg="#000000", bg="#00ffcc", insertbackground="#000000", bd=2, relief="flat")
        entry.pack(pady=5)
        return entry

    tk.Label(user_info_window, text="Enter Your Details", font=("Arial", 16, "bold"), fg="#00ffcc", bg="#000000").pack(pady=10)
    entry_name = create_entry(user_info_window, "Name:")
    entry_aadhar = create_entry(user_info_window, "Aadhar Card:")

    tk.Label(user_info_window, text="Gender:", font=("Arial", 10, "bold"), fg="#00ffcc", bg="#000000").pack(pady=2)
    gender_var = tk.StringVar(value="Male")
    gender_frame = tk.Frame(user_info_window, bg="#000000")
    tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", fg="#00ffcc", bg="#000000", selectcolor="#000000").pack(side="left", padx=5)
    tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", fg="#00ffcc", bg="#000000", selectcolor="#000000").pack(side="left", padx=5)
    tk.Radiobutton(gender_frame, text="Other", variable=gender_var, value="Other", fg="#00ffcc", bg="#000000", selectcolor="#000000").pack(side="left", padx=5)
    gender_frame.pack(pady=5)

    entry_email = create_entry(user_info_window, "Email:")
    entry_contact1 = create_entry(user_info_window, "Family Contact 1:")
    entry_contact2 = create_entry(user_info_window, "Family Contact 2:")
    entry_contact3 = create_entry(user_info_window, "Family Contact 3:")

    tk.Button(user_info_window, text="Save", command=save_user_data, bg="#00ffcc", fg="#000000", font=("Arial", 12, "bold"), padx=10, pady=5, relief="flat").pack(pady=15)

# Welcome Window
welcome_window = tk.Toplevel(root)
welcome_window.title("Welcome to SafeGuard")
welcome_window.geometry("350x700")
welcome_window.configure(bg="#000000")

tk.Label(welcome_window, text="Welcome to SafeGuard!", font=("Arial", 14, "bold"), fg="#00ffcc", bg="#000000").pack(pady=10)
tk.Label(welcome_window, text="Please enter your details before proceeding.", fg="#00ffcc", bg="#000000").pack()
tk.Button(welcome_window, text="Enter Details", command=open_user_info_window, bg="#00ffcc", fg="#000000", font=("Arial", 12, "bold"), relief="flat").pack(pady=20)

root.mainloop()
