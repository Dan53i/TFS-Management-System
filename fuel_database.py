import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox


class FuelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fuel Management System")

        # Database connection
        self.conn = sqlite3.connect("fuel_database.db")
        self.create_fuel_table()

        # Input fields
        self.vehicle_label = ttk.Label(root, text="Vehicle:")
        self.vehicle_entry = ttk.Entry(root)

        self.fuel_type_label = ttk.Label(root, text="Fuel Type:")
        self.fuel_type_entry = ttk.Entry(root)

        self.quantity_label = ttk.Label(root, text="Quantity (Liters):")
        self.quantity_entry = ttk.Entry(root)

        self.date_label = ttk.Label(root, text="Date:")
        self.date_entry = ttk.Entry(root)

        # Buttons
        self.add_button = ttk.Button(root, text="Add", command=self.add_fuel_record)
        self.update_button = ttk.Button(root, text="Update", command=self.update_fuel_record)
        self.delete_button = ttk.Button(root, text="Delete", command=self.delete_fuel_record)
        self.search_button = ttk.Button(root, text="Search", command=self.search_fuel_records)

        # Treeview (to display records)
        self.tree = ttk.Treeview(root, columns=("ID", "Vehicle", "Fuel Type", "Quantity", "Date"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Vehicle", text="Vehicle")
        self.tree.heading("Fuel Type", text="Fuel Type")
        self.tree.heading("Quantity", text="Quantity (Liters)")
        self.tree.heading("Date", text="Date")

        self.tree.bind("<ButtonRelease-1>", self.select_fuel_record)

        # Grid layout
        self.vehicle_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.vehicle_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.fuel_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.fuel_type_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.date_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.date_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.add_button.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.update_button.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.delete_button.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.search_button.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        self.tree.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        self.load_fuel_records()

    def create_fuel_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS FuelRecords (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Vehicle TEXT,
                    FuelType TEXT,
                    Quantity REAL,
                    Date TEXT
                )
            """)

    def add_fuel_record(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO FuelRecords (Vehicle, FuelType, Quantity, Date)
                VALUES (?, ?, ?, ?)
            """, (self.vehicle_entry.get(), self.fuel_type_entry.get(), float(self.quantity_entry.get()), self.date_entry.get()))

        self.clear_fuel_inputs()
        self.load_fuel_records()

    def update_fuel_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            fuel_id = self.tree.item(selected_item, "values")[0]
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE FuelRecords
                    SET Vehicle=?, FuelType=?, Quantity=?, Date=?
                    WHERE ID=?
                """, (self.vehicle_entry.get(), self.fuel_type_entry.get(),
                      float(self.quantity_entry.get()), self.date_entry.get(), fuel_id))

            self.clear_fuel_inputs()
            self.load_fuel_records()

    def delete_fuel_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            fuel_id = self.tree.item(selected_item, "values")[0]
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM FuelRecords WHERE ID=?", (fuel_id,))

            self.load_fuel_records()

    def search_fuel_records(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM FuelRecords
                WHERE Vehicle LIKE ? OR FuelType LIKE ? OR Date LIKE ?
            """, ("%" + self.vehicle_entry.get() + "%", "%" + self.fuel_type_entry.get() + "%", "%" + self.date_entry.get() + "%"))

            records = cursor.fetchall()
            self.display_fuel_records(records)

    def load_fuel_records(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM FuelRecords")
            records = cursor.fetchall()
            self.display_fuel_records(records)

    def display_fuel_records(self, records):
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert("", "end", values=record)

    def select_fuel_record(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.vehicle_entry.delete(0, "end")
            self.vehicle_entry.insert(0, values[1])

            self.fuel_type_entry.delete(0, "end")
            self.fuel_type_entry.insert(0, values[2])

            self.quantity_entry.delete(0, "end")
            self.quantity_entry.insert(0, values[3])

            self.date_entry.delete(0, "end")
            self.date_entry.insert(0, values[4])

    def clear_fuel_inputs(self):
        self.vehicle_entry.delete(0, "end")
        self.fuel_type_entry.delete(0, "end")
        self.quantity_entry.delete(0, "end")
        self.date_entry.delete(0, "end")


if __name__ == "__main__":
    root = tk.Tk()
    app = FuelManagementApp(root)
    root.mainloop()
