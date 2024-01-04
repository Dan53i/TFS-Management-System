import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


class VehicleSpareManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Spare Parts Management System")

        # Database connection
        self.conn = sqlite3.connect("spare_parts_database.db")
        self.create_spare_parts_table()

        # Input fields
        self.name_label = ttk.Label(root, text="Part Name:")
        self.name_entry = ttk.Entry(root)

        self.brand_label = ttk.Label(root, text="Part Brand:")
        self.brand_entry = ttk.Entry(root)

        self.quantity_label = ttk.Label(root, text="Quantity:")
        self.quantity_entry = ttk.Entry(root)

        self.price_label = ttk.Label(root, text="Price:")
        self.price_entry = ttk.Entry(root)

        # Buttons
        self.add_button = ttk.Button(root, text="Add", command=self.add_spare_part_record)
        self.update_button = ttk.Button(root, text="Update", command=self.update_spare_part_record)
        self.delete_button = ttk.Button(root, text="Delete", command=self.delete_spare_part_record)
        self.search_button = ttk.Button(root, text="Search", command=self.search_spare_parts)

        # Treeview (to display records)
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Brand", "Quantity", "Price"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Part Name")
        self.tree.heading("Brand", text="Part Brand")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")

        self.tree.bind("<ButtonRelease-1>", self.select_spare_part_record)

        # Grid layout
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.brand_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.brand_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.price_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.price_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.add_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.update_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.delete_button.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.search_button.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        self.tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        self.load_spare_parts()

    def create_spare_parts_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS SpareParts (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    Brand TEXT,
                    Quantity INTEGER,
                    Price REAL
                )
            """)

    def add_spare_part_record(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO SpareParts (Name, Brand, Quantity, Price)
                VALUES (?, ?, ?, ?)
            """, (self.name_entry.get(), self.brand_entry.get(), int(self.quantity_entry.get()), float(self.price_entry.get())))

        self.clear_spare_part_inputs()
        self.load_spare_parts()

    def update_spare_part_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            part_id = self.tree.item(selected_item, "values")[0]
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE SpareParts
                    SET Name=?, Brand=?, Quantity=?, Price=?
                    WHERE ID=?
                """, (self.name_entry.get(), self.brand_entry.get(),
                      int(self.quantity_entry.get()), float(self.price_entry.get()), part_id))

            self.clear_spare_part_inputs()
            self.load_spare_parts()

    def delete_spare_part_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            part_id = self.tree.item(selected_item, "values")[0]
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM SpareParts WHERE ID=?", (part_id,))

            self.load_spare_parts()

    def search_spare_parts(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM SpareParts
                WHERE Name LIKE ? OR Brand LIKE ? OR Price LIKE ?
            """, ("%" + self.name_entry.get() + "%", "%" + self.brand_entry.get() + "%", "%" + self.price_entry.get() + "%"))

            records = cursor.fetchall()
            self.display_spare_parts(records)

    def load_spare_parts(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM SpareParts")
            records = cursor.fetchall()
            self.display_spare_parts(records)

    def display_spare_parts(self, records):
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert("", "end", values=record)

    def select_spare_part_record(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, values[1])

            self.brand_entry.delete(0, "end")
            self.brand_entry.insert(0, values[2])

            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, values[3])

            self.price_entry.delete(0, "end")
            self.price_entry.insert(0, values[4])

    def clear_spare_part_inputs(self):
        self.name_entry.delete(0, "end")
        self.brand_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.price_entry.delete(0, "end")


if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleSpareManagementApp(root)
    root.mainloop()
