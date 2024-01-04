import tkinter as tk
from tkinter import messagebox
from fuel_database import FuelManagementApp
from vehicle_database import VehicleDatabaseApp
from spare_database import VehicleSpareManagementApp


class LandingPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Landing Page")
        self.master.geometry("300x200")

        self.create_widgets()

    def create_widgets(self):
        self.vehicle_button = tk.Button(self.master, text="Vehicle DataBase", command=self.open_vehicle_database)
        self.vehicle_button.pack(pady=20)

        self.fuel_button = tk.Button(self.master, text="Fuel DataBase", command=self.open_fuel_database)
        self.fuel_button.pack(pady=20)

        self.spare_button = tk.Button(self.master, text="Spare Database", command=self.open_spare_database)
        self.spare_button.pack(pady=20)

    def open_vehicle_database(self):
        vehicle_window = tk.Toplevel(self.master)
        vehicle_page = VehicleDatabaseApp(vehicle_window)

    def open_fuel_database(self):
        fuel_window = tk.Toplevel(self.master)
        fuel_page = FuelManagementApp(fuel_window)

    def open_spare_database(self):
        spare_window = tk.Toplevel(self.master)
        spare_page = VehicleSpareManagementApp(spare_window)


if __name__ == "__main__":
    root = tk.Tk()
    landing_page = LandingPage(root)
    root.mainloop()

