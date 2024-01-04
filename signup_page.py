# signup_page.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database


class SignupPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Signup Page")

        # Database connection
        self.db = Database()

        # Styling
        style = ttk.Style()
        style.configure("TButton", padding=(10, 5), font='Helvetica 10 bold')

        # Layout
        ttk.Label(master, text="Signup", font='Helvetica 16 bold').grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(master, text="First Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.first_name_entry = ttk.Entry(master)
        self.first_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(master, text="Last Name:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.last_name_entry = ttk.Entry(master)
        self.last_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(master, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ttk.Entry(master)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(master, text="Password:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = ttk.Entry(master, show="*")
        self.password_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(master, text="Signup", command=self.signup).grid(row=5, column=0, columnspan=2, pady=10)

    def signup(self):
        # Simple email validation using regular expression
        if not self.email_entry.get():
            messagebox.showerror("Error", "Email cannot be empty")
            return

        # Check if email already exists in the database
        user = self.db.get_user_by_email_password(self.email_entry.get(), "")
        if user:
            messagebox.showerror("Error", "Email already exists")
            return

        # Other signup logic goes here
        # ...

        # Insert user data into the database
        self.db.insert_user(
            self.first_name_entry.get(),
            self.last_name_entry.get(),
            self.email_entry.get(),
            self.password_entry.get()
        )

        messagebox.showinfo("Signup", "Signup successful!")
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SignupPage(root)
    root.mainloop()
