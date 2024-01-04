
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import Database
from landing_referral import LandingPage


class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Login Page")

        # Database connection
        self.db = Database()

        # Styling
        style = ttk.Style()
        style.configure("TButton", padding=(10, 5), font='Helvetica 10 bold')

        # Layout
        ttk.Label(master, text="Login", font='Helvetica 16 bold').grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(master, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ttk.Entry(master)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ttk.Label(master, text="Password:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = ttk.Entry(master, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ttk.Button(master, text="Login", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        # Simple email validation using regular expression
        if not self.email_entry.get():
            messagebox.showerror("Error", "Email cannot be empty")
            return

        user = self.db.get_user_by_email_password(self.email_entry.get(), self.password_entry.get())
        if user:

            self.show_landing_referral()
            # messagebox.showinfo("Login", "Login successful!")
            # self.master.destroy()
        else:
            messagebox.showerror("Error", "Invalid email or password")

    def show_landing_referral(self):
        landing_window = tk.Toplevel(self.master)
        landing_page = LandingPage(landing_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
