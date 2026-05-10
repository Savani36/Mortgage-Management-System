import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta 
import subprocess

#product details form
class MortgageManager:

    def open_new_python_file(self):
        subprocess.Popen(['python', 'loan_det_form (1).py'])

    def __init__(self, root):
        self.root = root
        root.title("Mortgage Management System")
        root.geometry("800x500+0+0")

        self.name, self.date, self.product_name, self.product_weight = (tk.StringVar() for _ in range(4))

        title = tk.Label(root, text="Product Details", font=("Arial", 20), bd=10, bg='seagreen', fg='white')
        title.pack(side=tk.TOP, fill=tk.X)

        input_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg='white')
        input_frame.place(x=10, y=70, width=980, height=250)

        labels = ["Name", "Date", "Product Name", "Product Weight"]

        for i, label in enumerate(labels):
            lbl = tk.Label(input_frame, text=label, font=("Comic Sans MS", 10))
            lbl.grid(row=i, column=0, pady=10, padx=20, sticky="w")

        entries = [tk.Entry(input_frame, font=("Comic Sans MS", 10), bd=3, textvariable=var) for var in
                   [self.name, self.date, self.product_name, self.product_weight]]

        for i, entry in enumerate(entries):
            entry.grid(row=i, column=1, pady=10, padx=10, sticky="w")

        self.date_entry = DateEntry(input_frame, font=("Comic Sans MS", 10), bd=3, textvariable=self.date, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        btn_frame = tk.Frame(root, bd=5, relief=tk.RIDGE)
        btn_frame.place(x=1170, y=250, width=150, height=270)  # Adjusted position and size

        buttons = [
            tk.Button(btn_frame, text=label, font='arial 10 bold', bg='seagreen', fg='white', width=15, command=command)
            for label, command in [
                ('Save Product', self.save_product),
                ('View Products', self.view_products),
                ('Delete Product', self.delete_product),
                ('Update Product', self.update_product),
                ('Next', self.open_new_python_file)  # Added "Next" button
            ]
        ]

        for i, button in enumerate(buttons):
            button.grid(row=i, column=0, pady=10)

        # Create Treeview for displaying products with a vertical scrollbar
        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Date", "Product Name", "Product Weight"), show="headings")
        self.tree.place(x=10, y=330, width=980, height=400)  # Increase the height

        for col in ("ID", "Name", "Date", "Product Name", "Product Weight"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Create and set up the vertical scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=969, y=330, height=400)

        self.tree.configure(yscrollcommand=scrollbar.set)

        # Create and set up the database table
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect("mortgage_database.db")
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                product_name TEXT NOT NULL,
                product_weight REAL NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def validate_inputs(self):
        name = self.name.get()
        date = self.date.get()
        product_name = self.product_name.get()
        product_weight = self.product_weight.get()

        # Validate name: Allow only alphabetic characters
        if not name.isalpha():
            messagebox.showwarning("Input Error", "Invalid input for name. Only alphabetic characters are allowed.")
            return False

        # Validate date: Allow only the current date and not older than 1 year
        current_date = datetime.now().date()
        selected_date = self.date_entry.get_date()

        if selected_date > current_date or selected_date < current_date:
            messagebox.showwarning("Input Error", "Invalid input for date. Please select current day as date.")
            return False

        # Validate product weight: Allow only float or integer
        try:
            product_weight = float(product_weight)
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid input. Please enter a valid numeric value for product weight.")
            return False

        return True

    def save_product(self):
        if not self.validate_inputs():
            return

        name = self.name.get()
        date = self.date.get()
        product_name = self.product_name.get()
        product_weight = float(self.product_weight.get())

        conn = sqlite3.connect("mortgage_database.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO products (name, date, product_name, product_weight)
            VALUES (?, ?, ?, ?)
        ''', (name, date, product_name, product_weight))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Product details saved successfully.")

    def view_products(self):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect("mortgage_database.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM products
        ''')

        for row in cursor.fetchall():
            self.tree.insert("", "end", values=row)

        conn.close()

    def delete_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")
            return

        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this product?")
        if confirmation:
            conn = sqlite3.connect("mortgage_database.db")
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM products WHERE id=?
            ''', (self.tree.item(selected_item, "values")[0],))

            conn.commit()
            conn.close()

            self.view_products()  # Refresh the Treeview after deletion
            messagebox.showinfo("Success", "Product deleted successfully.")

    def update_product(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a product to update.")
            return

        # Get the existing values from the selected item
        existing_values = self.tree.item(selected_item, "values")

        # Set the entry values to the existing values for editing
        self.name.set(existing_values[1])
        self.date.set(existing_values[2])
        self.product_name.set(existing_values[3])
        self.product_weight.set(existing_values[4])

        # Call the save_product method to update the record
        self.save_product()

    def show_loan_manager(self):
        self.root.iconify()  # Minimize the main window
        nroot = Toplevel(self.root)
        nroot.protocol("WM_DELETE_WINDOW", lambda: self.on_loan_manager_close(nroot))
        CustomerRegistration(nroot) # type: ignore

    def on_loan_manager_close(self, nroot):
        # This function is called when the LoanManager window is closed
        self.root.deiconify()  # Restore the minimized main window
        nroot.destroy()  # Destroy the Toplevel window

def show_product_form(root):
    nroot = Toplevel(root)
    MortgageManager(nroot)

root = Tk()
show_product_form(root)
root.mainloop()