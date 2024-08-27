import tkinter as tk
from tkinter import messagebox


class Car:
    def __init__(self, make, model, year, price):
        self.make = make
        self.model = model
        self.year = year
        self.price = price

    def display_info(self):
        return f"Car: {self.year} {self.make} {self.model} | Price: ${self.price:,.2f}"


class RentalCar(Car):
    def __init__(self, make, model, year, price, daily_rate):
        super().__init__(make, model, year, price)
        self.daily_rate = daily_rate

    def calculate_rental(self, days):
        total_rental = self.daily_rate * days
        return total_rental


class SoldCar(Car):
    def __init__(self, make, model, year, price):
        super().__init__(make, model, year, price)
        self.sold = False

    def sell_car(self):
        self.sold = True
        return self.price


class Showroom:
    def __init__(self):
        self.cars = []
        self.rented_cars = []
        self.sold_cars = []

    def add_car(self, car):
        self.cars.append(car)

    def rent_car(self, car, days):
        if car in self.cars:
            total_rental = car.calculate_rental(days)
            self.rented_cars.append((car, days))
            return total_rental
        else:
            return None

    def sell_car(self, car):
        if car in self.cars:
            car.sell_car()
            self.sold_cars.append(car)
            self.cars.remove(car)
        else:
            return None


class ShowroomApp:
    def __init__(self, root):
        self.showroom = Showroom()
        self.root = root
        self.root.title("Car Showroom")

        # Widgets for adding cars
        self.add_car_frame = tk.LabelFrame(root, text="Add Car", padx=10, pady=10)
        self.add_car_frame.pack(padx=10, pady=10)

        tk.Label(self.add_car_frame, text="Make:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(self.add_car_frame, text="Model:").grid(row=1, column=0, sticky=tk.W)
        tk.Label(self.add_car_frame, text="Year:").grid(row=2, column=0, sticky=tk.W)
        tk.Label(self.add_car_frame, text="Price:").grid(row=3, column=0, sticky=tk.W)
        tk.Label(self.add_car_frame, text="Daily Rate (For Rental Car):").grid(row=4, column=0, sticky=tk.W)

        self.make_entry = tk.Entry(self.add_car_frame)
        self.model_entry = tk.Entry(self.add_car_frame)
        self.year_entry = tk.Entry(self.add_car_frame)
        self.price_entry = tk.Entry(self.add_car_frame)
        self.daily_rate_entry = tk.Entry(self.add_car_frame)

        self.make_entry.grid(row=0, column=1)
        self.model_entry.grid(row=1, column=1)
        self.year_entry.grid(row=2, column=1)
        self.price_entry.grid(row=3, column=1)
        self.daily_rate_entry.grid(row=4, column=1)

        tk.Button(self.add_car_frame, text="Add Rental Car", command=self.add_rental_car).grid(row=5, column=0, pady=10)
        tk.Button(self.add_car_frame, text="Add Sold Car", command=self.add_sold_car).grid(row=5, column=1, pady=10)

        # Widgets for renting and selling cars
        self.transaction_frame = tk.LabelFrame(root, text="Transactions", padx=10, pady=10)
        self.transaction_frame.pack(padx=10, pady=10)

        tk.Label(self.transaction_frame, text="Car Index:").grid(row=0, column=0, sticky=tk.W)
        tk.Label(self.transaction_frame, text="Days (For Rental):").grid(row=1, column=0, sticky=tk.W)

        self.car_index_entry = tk.Entry(self.transaction_frame)
        self.days_entry = tk.Entry(self.transaction_frame)

        self.car_index_entry.grid(row=0, column=1)
        self.days_entry.grid(row=1, column=1)

        tk.Button(self.transaction_frame, text="Rent Car", command=self.rent_car).grid(row=2, column=0, pady=10)
        tk.Button(self.transaction_frame, text="Sell Car", command=self.sell_car).grid(row=2, column=1, pady=10)

        # Display area
        self.display_frame = tk.LabelFrame(root, text="Showroom", padx=10, pady=10)
        self.display_frame.pack(padx=10, pady=10)

        self.display_text = tk.Text(self.display_frame, height=15, width=60)
        self.display_text.pack()

        tk.Button(root, text="Display Cars", command=self.display_cars).pack(pady=10)
        tk.Button(root, text="Display Rented Cars", command=self.display_rented_cars).pack(pady=10)
        tk.Button(root, text="Display Sold Cars", command=self.display_sold_cars).pack(pady=10)

    def add_rental_car(self):
        make = self.make_entry.get()
        model = self.model_entry.get()
        year = int(self.year_entry.get())
        price = float(self.price_entry.get())
        daily_rate = float(self.daily_rate_entry.get())
        car = RentalCar(make, model, year, price, daily_rate)
        self.showroom.add_car(car)
        messagebox.showinfo("Success", f"Rental Car {make} {model} added.")

    def add_sold_car(self):
        make = self.make_entry.get()
        model = self.model_entry.get()
        year = int(self.year_entry.get())
        price = float(self.price_entry.get())
        car = SoldCar(make, model, year, price)
        self.showroom.add_car(car)
        messagebox.showinfo("Success", f"Sold Car {make} {model} added.")

    def rent_car(self):
        try:
            car_index = int(self.car_index_entry.get()) - 1
            days = int(self.days_entry.get())
            car = self.showroom.cars[car_index]
            if isinstance(car, RentalCar):
                rental_cost = self.showroom.rent_car(car, days)
                messagebox.showinfo("Success", f"Rented {car.make} {car.model} for {days} days. Total: ${rental_cost:.2f}")
            else:
                messagebox.showerror("Error", "Selected car is not available for rent.")
        except IndexError:
            messagebox.showerror("Error", "Invalid car index.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def sell_car(self):
        try:
            car_index = int(self.car_index_entry.get()) - 1
            car = self.showroom.cars[car_index]
            if isinstance(car, SoldCar):
                self.showroom.sell_car(car)
                messagebox.showinfo("Success", f"Sold {car.make} {car.model} for ${car.price:.2f}")
            else:
                messagebox.showerror("Error", "Selected car is not available for sale.")
        except IndexError:
            messagebox.showerror("Error", "Invalid car index.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def display_cars(self):
        self.display_text.delete(1.0, tk.END)
        if not self.showroom.cars:
            self.display_text.insert(tk.END, "No cars available in the showroom.\n")
        else:
            for i, car in enumerate(self.showroom.cars, 1):
                self.display_text.insert(tk.END, f"{i}. {car.display_info()}\n")

    def display_rented_cars(self):
        self.display_text.delete(1.0, tk.END)
        if not self.showroom.rented_cars:
            self.display_text.insert(tk.END, "No cars rented out.\n")
        else:
            for i, (car, days) in enumerate(self.showroom.rented_cars, 1):
                self.display_text.insert(tk.END, f"Rented: {car.display_info()} for {days} days.\n")

    def display_sold_cars(self):
        self.display_text.delete(1.0, tk.END)
        if not self.showroom.sold_cars:
            self.display_text.insert(tk.END, "No cars sold.\n")
        else:
            for i, car in enumerate(self.showroom.sold_cars, 1):
                self.display_text.insert(tk.END, f"Sold: {car.display_info()}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = ShowroomApp(root)
    root.mainloop()
