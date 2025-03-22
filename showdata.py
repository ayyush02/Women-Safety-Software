import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json

# Sample user data file
user_data_file = "user_data.json"

# Load user data from file
def load_user_data():
    try:
        with open(user_data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save user data to file
def save_user_data(data):
    with open(user_data_file, "w") as file:
        json.dump(data, file, indent=4)

# Update user data
def update_user_data():
    user_data["name"] = name_entry.get()
    user_data["aadhar"] = aadhar_entry.get()
    user_data["gender"] = gender_entry.get()
    user_data["email"] = email_entry.get()
    user_data["phone"] = phone_entry.get()
    user_data["family_contacts"] = [contact_entry_1.get(), contact_entry_2.get(), contact_entry_3.get()]
    save_user_data(user_data)
    messagebox.showinfo("Success", "User data updated successfully!")

# Load user data
user_data = load_user_data()
print("Loaded user data:", user_data)  # Debugging statement

# Create the main window
root = tk.Tk()
root.title("User Information Dashboard")
root.geometry("350x700")  # Mobile-like dimensions
root.configure(bg="black")

# Title label
title_label = tk.Label(root, text="User Information Dashboard", font=("Arial", 18, "bold"), bg="black", fg="#FF0000")
title_label.pack(pady=10)

# Function to enable editing
def enable_editing(entry):
    entry.config(state=tk.NORMAL)

# Load pen icon
pen_image = Image.open("pen_icon.png")
pen_image = pen_image.resize((20, 20), Image.LANCZOS)
pen_icon = ImageTk.PhotoImage(pen_image)

# Name label and entry
name_frame = tk.Frame(root, bg="black")
name_label = tk.Label(name_frame, text="Name:", font=("Arial", 12), bg="black", fg="#FF0000")
name_label.pack(side=tk.LEFT, padx=5)
name_entry = tk.Entry(name_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
name_entry.pack(side=tk.LEFT, padx=5)
name_entry.insert(0, user_data.get("name", ""))
print("Name:", user_data.get("name", ""))  # Debugging statement
name_edit_btn = tk.Button(name_frame, image=pen_icon, bg="black", command=lambda: enable_editing(name_entry))
name_edit_btn.pack(side=tk.LEFT, padx=5)
name_frame.pack(pady=10)

# Aadhar label and entry
aadhar_frame = tk.Frame(root, bg="black")
aadhar_label = tk.Label(aadhar_frame, text="Aadhar:", font=("Arial", 12), bg="black", fg="#FF0000")
aadhar_label.pack(side=tk.LEFT, padx=5)
aadhar_entry = tk.Entry(aadhar_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
aadhar_entry.pack(side=tk.LEFT, padx=5)
aadhar_entry.insert(0, user_data.get("aadhar", ""))
print("Aadhar:", user_data.get("aadhar", ""))  # Debugging statement
aadhar_edit_btn = tk.Button(aadhar_frame, image=pen_icon, bg="black", command=lambda: enable_editing(aadhar_entry))
aadhar_edit_btn.pack(side=tk.LEFT, padx=5)
aadhar_frame.pack(pady=10)

# Gender label and entry
gender_frame = tk.Frame(root, bg="black")
gender_label = tk.Label(gender_frame, text="Gender:", font=("Arial", 12), bg="black", fg="#FF0000")
gender_label.pack(side=tk.LEFT, padx=5)
gender_entry = tk.Entry(gender_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
gender_entry.pack(side=tk.LEFT, padx=5)
gender_entry.insert(0, user_data.get("gender", ""))
print("Gender:", user_data.get("gender", ""))  # Debugging statement
gender_edit_btn = tk.Button(gender_frame, image=pen_icon, bg="black", command=lambda: enable_editing(gender_entry))
gender_edit_btn.pack(side=tk.LEFT, padx=5)
gender_frame.pack(pady=10)

# Email label and entry
email_frame = tk.Frame(root, bg="black")
email_label = tk.Label(email_frame, text="Email:", font=("Arial", 12), bg="black", fg="#FF0000")
email_label.pack(side=tk.LEFT, padx=5)
email_entry = tk.Entry(email_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
email_entry.pack(side=tk.LEFT, padx=5)
email_entry.insert(0, user_data.get("email", ""))
print("Email:", user_data.get("email", ""))  # Debugging statement
email_edit_btn = tk.Button(email_frame, image=pen_icon, bg="black", command=lambda: enable_editing(email_entry))
email_edit_btn.pack(side=tk.LEFT, padx=5)
email_frame.pack(pady=10)

# Phone label and entry
phone_frame = tk.Frame(root, bg="black")
phone_label = tk.Label(phone_frame, text="Phone:", font=("Arial", 12), bg="black", fg="#FF0000")
phone_label.pack(side=tk.LEFT, padx=5)
phone_entry = tk.Entry(phone_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
phone_entry.pack(side=tk.LEFT, padx=5)
phone_entry.insert(0, user_data.get("phone", ""))
print("Phone:", user_data.get("phone", ""))  # Debugging statement
phone_edit_btn = tk.Button(phone_frame, image=pen_icon, bg="black", command=lambda: enable_editing(phone_entry))
phone_edit_btn.pack(side=tk.LEFT, padx=5)
phone_frame.pack(pady=10)

# Family contacts label and entries
contacts_frame = tk.Frame(root, bg="black")
contacts_label = tk.Label(contacts_frame, text="Family Contacts:", font=("Arial", 12), bg="black", fg="#FF0000")
contacts_label.pack(pady=5)

contact_entry_1 = tk.Entry(contacts_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
contact_entry_1.pack(pady=5)
contact_entry_1.insert(0, user_data.get("family_contacts", [""])[0])
print("Family Contact 1:", user_data.get("family_contacts", [""])[0])  # Debugging statement

contact_entry_2 = tk.Entry(contacts_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
contact_entry_2.pack(pady=5)
contact_entry_2.insert(0, user_data.get("family_contacts", ["", ""])[1])
print("Family Contact 2:", user_data.get("family_contacts", ["", ""])[1])  # Debugging statement

contact_entry_3 = tk.Entry(contacts_frame, font=("Arial", 12), bg="black", fg="#FFFFFF", insertbackground="#FFFFFF", highlightbackground="#FF0000", highlightcolor="#FF0000", state=tk.DISABLED)
contact_entry_3.pack(pady=5)
contact_entry_3.insert(0, user_data.get("family_contacts", ["", "", ""])[2])
print("Family Contact 3:", user_data.get("family_contacts", ["", "", ""])[2])  # Debugging statement

contacts_edit_btn = tk.Button(contacts_frame, image=pen_icon, bg="black", command=lambda: [enable_editing(contact_entry_1), enable_editing(contact_entry_2), enable_editing(contact_entry_3)])
contacts_edit_btn.pack(pady=5)
contacts_frame.pack(pady=10)

# Update button
update_button = tk.Button(root, text="Update", font=("Arial", 12, "bold"), bg="black", fg="#FF0000", activebackground="black", activeforeground="#FF0000", command=update_user_data)
update_button.pack(pady=20)

# Run the application
root.mainloop()