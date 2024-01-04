import tkinter as tk
from tkinter import ttk
from signup_page import SignupPage
from login_page import LoginPage


class LandingPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Landing Page")

        # Styling
        style = ttk.Style()
        style.configure("TButton", padding=(10, 5), font='Helvetica 10 bold')

        # Layout
        ttk.Label(master, text="Welcome to the App", font='Helvetica 16 bold').pack(pady=20)

        ttk.Button(master, text="Sign Up", command=self.open_signup_page).pack(pady=10)
        ttk.Button(master, text="Login", command=self.open_login_page).pack(pady=10)

    def open_signup_page(self):
        signup_window = tk.Toplevel(self.master)
        SignupPage(signup_window)

    def open_login_page(self):
        login_window = tk.Toplevel(self.master)
        LoginPage(login_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = LandingPage(root)
    root.mainloop()