import tkinter as tk
from tkinter import ttk
import sqlite3


class VehicleDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Database")

        # Database connection
        self.conn = sqlite3.connect("vehicles_database.db")
        self.create_table()

        # Input fields
        self.name_label = ttk.Label(root, text="Vehicle Name:")
        self.name_entry = ttk.Entry(root)

        self.brand_label = ttk.Label(root, text="Vehicle Brand:")
        self.brand_entry = ttk.Entry(root)

        self.tires_label = ttk.Label(root, text="Number of Tires:")
        self.tires_entry = ttk.Entry(root)

        self.plate_label = ttk.Label(root, text="Plate Number:")
        self.plate_entry = ttk.Entry(root)

        self.thread_label = ttk.Label(root, text="Thread Depth:")
        self.thread_entry = ttk.Entry(root)

        # Buttons
        self.add_button = ttk.Button(root, text="Add", command=self.add_record)
        self.update_button = ttk.Button(root, text="Update", command=self.update_record)
        self.delete_button = ttk.Button(root, text="Delete", command=self.delete_record)
        self.search_button = ttk.Button(root, text="Search", command=self.search_records)

        # Treeview (to display records)
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Brand", "Tires", "Plate Number", "Thread Depth"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Vehicle Name")
        self.tree.heading("Brand", text="Vehicle Brand")
        self.tree.heading("Tires", text="Number of Tires")
        self.tree.heading("Plate Number", text="Plate Number")
        self.tree.heading("Thread Depth", text="Thread Depth")

        self.tree.bind("<ButtonRelease-1>", self.select_record)

        # Grid layout
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.brand_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.brand_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.tires_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.tires_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.plate_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.plate_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.thread_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.thread_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.add_button.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.update_button.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.delete_button.grid(row=5, column=2, padx=10, pady=5, sticky="w")
        self.search_button.grid(row=5, column=3, padx=10, pady=5, sticky="w")

        self.tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        self.load_records()

    def create_table(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Vehicles (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT,
                    Brand TEXT,
                    Tires INTEGER,
                    PlateNumber TEXT,
                    ThreadDepth TEXT
                )
            """)

    def add_record(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Vehicles (Name, Brand, Tires, PlateNumber, ThreadDepth)
                VALUES (?, ?, ?, ?, ?)
            """, (self.name_entry.get(), self.brand_entry.get(), self.tires_entry.get(),
                  self.plate_entry.get(), self.thread_entry.get()))

        self.clear_inputs()
        self.load_records()

    def update_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            vehicle_id = self.tree.item(selected_item, "values")[0]
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("""
                    UPDATE Vehicles
                    SET Name=?, Brand=?, Tires=?, PlateNumber=?, ThreadDepth=?
                    WHERE ID=?
                """, (self.name_entry.get(), self.brand_entry.get(), self.tires_entry.get(),
                      self.plate_entry.get(), self.thread_entry.get(), vehicle_id))

            self.clear_inputs()
            self.load_records()

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            vehicle_id = self.tree.item(selected_item, "values")[0]
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM Vehicles WHERE ID=?", (vehicle_id,))

            self.load_records()

    def search_records(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Vehicles
                WHERE Name LIKE ? OR Brand LIKE ? OR PlateNumber LIKE ?
            """, ("%" + self.name_entry.get() + "%", "%" + self.brand_entry.get() + "%", "%" + self.plate_entry.get() + "%"))

            records = cursor.fetchall()
            self.display_records(records)

    def load_records(self):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Vehicles")
            records = cursor.fetchall()
            self.display_records(records)

    def display_records(self, records):
        self.tree.delete(*self.tree.get_children())
        for record in records:
            self.tree.insert("", "end", values=record)

    def select_record(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            self.name_entry.delete(0, "end")
            self.name_entry.insert(0, values[1])

            self.brand_entry.delete(0, "end")
            self.brand_entry.insert(0, values[2])

            self.tires_entry.delete(0, "end")
            self.tires_entry.insert(0, values[3])

            self.plate_entry.delete(0, "end")
            self.plate_entry.insert(0, values[4])

            self.thread_entry.delete(0, "end")
            self.thread_entry.insert(0, values[5])

    def clear_inputs(self):
        self.name_entry.delete(0, "end")
        self.brand_entry.delete(0, "end")
        self.tires_entry.delete(0, "end")
        self.plate_entry.delete(0, "end")
        self.thread_entry.delete(0, "end")


if __name__ == "__main__":
    root = tk.Tk()
    vehicle_page = VehicleDatabaseApp(root)
    # app = VehicleDatabaseApp(root)
    root.mainloop()



