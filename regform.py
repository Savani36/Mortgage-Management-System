import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import subprocess

class LoginForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Form")

        # Username and password labels and entry fields
        tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Login button
        tk.Button(root, text="Login", command=self.login).grid(row=2, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "root":
            self.root.destroy()
            # Open registration form
            root = tk.Tk()
            app = RegistrationForm(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form")
        
        # Connect to SQLite database
        self.conn = sqlite3.connect('loanDetails.db')
        self.cur = self.conn.cursor()

        # Main frame to hold form and treeview
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header frame
        header_frame = tk.Frame(main_frame, bg="seagreen")
        header_frame.pack(fill=tk.X)

        # Header label
        header_label = tk.Label(header_frame, text="Customer Registration", font=("Arial", 16, "bold"), fg="white", bg="seagreen")
        header_label.pack(padx=10, pady=10)

        # Form frame
        form_frame = tk.Frame(main_frame)
        form_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Create labels and entry fields
        fields = ["Loan ID", "Name", "Address", "Pincode", "Phone Number"]
        self.entries = {}
        self.validations = {
            "Loan ID": self.validate_loan_id,
            "Name": self.validate_name,
            "Address": self.validate_address,
            "Pincode": self.validate_pincode,
            "Phone Number": self.validate_phone
        }
        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, font=("Arial", 12))
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(form_frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        # Create buttons frame
        btn_frame = tk.Frame(form_frame)
        btn_frame.grid(row=len(fields), columnspan=2, pady=10)

        # Create buttons
        btn_add = tk.Button(btn_frame, text="Add", command=self.add_data, font=("Arial", 12))
        btn_add.grid(row=0, column=0, padx=5)
        btn_update = tk.Button(btn_frame, text="Update", command=self.update_data, font=("Arial", 12))
        btn_update.grid(row=0, column=1, padx=5)
        btn_delete = tk.Button(btn_frame, text="Delete", command=self.delete_data, font=("Arial", 12))
        btn_delete.grid(row=0, column=2, padx=5)
        btn_next = tk.Button(btn_frame, text="Next", command=self.open_next_window, font=("Arial", 12))
        btn_next.grid(row=0, column=3, padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Treeview to display data
        self.tree = ttk.Treeview(tree_frame, columns=fields, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        for field in fields:
            self.tree.heading(field, text=field)
        self.display_data()

    def add_data(self):
        # Validate entry fields
        if not self.validate_entries():
            return

        # Retrieve data from entry fields
        loan_id = self.entries["Loan ID"].get()
        name = self.entries["Name"].get()
        address = self.entries["Address"].get()
        pincode = self.entries["Pincode"].get()
        phone = self.entries["Phone Number"].get()

        # Insert data into database
        self.cur.execute("INSERT INTO customers (LoanID, Name, Address, Pincode, Phone) VALUES (?, ?, ?, ?, ?)",
                         (loan_id, name, address, pincode, phone))
        self.conn.commit()
        messagebox.showinfo("Success", "Data added successfully.")
        self.display_data()

    def update_data(self):
        # Validate entry fields
        if not self.validate_entries():
            return

        # Retrieve data from entry fields
        loan_id = self.entries["Loan ID"].get()
        name = self.entries["Name"].get()
        address = self.entries["Address"].get()
        pincode = self.entries["Pincode"].get()
        phone = self.entries["Phone Number"].get()

        # Update data in database
        self.cur.execute("UPDATE customers SET Name=?, Address=?, Pincode=?, Phone=? WHERE LoanID=?",
                         (name, address, pincode, phone, loan_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Data updated successfully.")
        self.display_data()

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.")
            return
        loan_id = self.tree.item(selected_item, 'values')[0]
        confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete the record with Loan ID {loan_id}?")
        if confirmation:
            self.cur.execute("DELETE FROM customers WHERE LoanID=?", (loan_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully.")
            self.display_data()

    def display_data(self):
        # Clear previous data
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Fetch data from database and display in Treeview
        self.cur.execute("SELECT * FROM customers")
        rows = self.cur.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def validate_entries(self):
        for field, entry in self.entries.items():
            validation_func = self.validations.get(field)
            if validation_func and not validation_func(entry.get()):
                messagebox.showerror("Validation Error", f"Invalid value for {field}")
                return False
        return True

    def validate_loan_id(self, value):
        return value.isdigit() and len(value) == 3

    def validate_name(self, value):
        return all(char.isalpha() or char.isspace() for char in value)

    def validate_address(self, value):
        return True

    def validate_pincode(self, value):
        return value.isdigit() and len(value) == 6

    def validate_phone(self, value):
        return value.isdigit() and len(value) == 10
    
    def validate_aadharcard(self, value):
        return value.isdigit() and len(value) == 12
    
    def open_next_window(self):
        subprocess.run(["python", "product try1 (1).py"])

if __name__ == "__main__":
    # Create the customers table if not exists
    conn = sqlite3.connect('loanDetails.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS customers (
                   LoanID TEXT PRIMARY KEY,
                   Name TEXT,
                   Address TEXT,
                   Pincode TEXT,
                   Phone TEXT)''')
    conn.commit()

    # Create and run the login application
    login_root = tk.Tk()
    login_app = LoginForm(login_root)
    login_root.mainloop()
