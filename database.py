# database.py

import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("user_data.db")
        self.create_user_table()

    def create_user_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Users (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FirstName TEXT,
                    LastName TEXT,
                    Email TEXT UNIQUE,
                    Password TEXT
                )
            """)

    def insert_user(self, first_name, last_name, email, password):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Users (FirstName, LastName, Email, Password)
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, email, password))

    def get_user_by_email_password(self, email, password):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Users WHERE Email=? AND Password=?", (email, password))
            return cursor.fetchone()

