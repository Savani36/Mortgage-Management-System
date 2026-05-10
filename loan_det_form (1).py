from tkinter import *
from tkinter import ttk, messagebox
from tkinter import filedialog
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar
import sqlite3
import subprocess
import re

class LoanDetails:
    def __init__(self, root):
        root.title("Loan Management System")
        root.geometry("1100x600+0+0")

        title = Label(root, text="Mortgage Details", font=("Arial", 20), bd=10, bg='seagreen', fg='white')
        title.pack(side=TOP, fill=X)

        self.CustomerId, self.Products, self.Weight, self.Description, self.Document, self.Amount, self.MonthlyRate, self.MonthlyPayment, self.Balance, self.PayDate = (
            StringVar() for _ in range(10)
        )
        self.ModeOfPayment = StringVar()  # Variable to store the selected mode of payment

        Detail_F = Frame(root, bd=4, relief=RIDGE, bg='white')
        Detail_F.place(x=10, y=90, width=500, height=500)

        labels = ["Customer Id", "Products", "Weight", "Amount", "Monthly Rate", "Monthly Payment", "Balance", "Pay Date", "Mode of Payment"]

        for i, label in enumerate(labels):
            lbl = Label(Detail_F, text=label, font=("Comic Sans MS", 10))
            lbl.grid(row=i, column=0, pady=10, padx=20, sticky="w")

        self.description_button = Button(Detail_F, text="Upload Description", command=self.upload_description)
        self.description_button.grid(row=3, column=1, pady=10, sticky="w")

        self.document_button = Button(Detail_F, text="Upload Document", command=self.upload_document)
        self.document_button.grid(row=4, column=1, pady=5, sticky="w")

        entries = [
            Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=var) for var in
            [self.CustomerId, self.Products, self.Weight, self.Amount, self.MonthlyRate, self.MonthlyPayment, self.Balance]
        ]

        for i, entry in enumerate(entries):
            entry.grid(row=i, column=1, pady=10, sticky="w")

        # Combobox for Mode of Payment
        mode_of_payment_combo = ttk.Combobox(Detail_F, textvariable=self.ModeOfPayment, values=["Cash", "Credit/Debit", "Online Banking"], font=("Comic Sans MS", 10))
        mode_of_payment_combo.grid(row=8, column=1, pady=10, sticky="w")
        mode_of_payment_combo.current(0)  # Set the default selection to the first option ("Cash")

        # Date picker for Pay Date
        self.pay_date_picker = DateEntry(Detail_F, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.pay_date_picker.grid(row=7, column=1, padx=20, pady=10, sticky="w")

        btnFrame = Frame(root, bd=5, relief=RIDGE)
        btnFrame.place(x=780, y=580, width=550, height=60)

        buttons = [
            Button(btnFrame, text=label, font='arial 10 bold', bg='seagreen', fg='white', width=10, command=command)
            for label, command in [
                ('Add Record', self.addrecord),
                ('Update', self.update),
                ('Delete', self.delete),
                ('Reset', self.reset),
                ('Next', self.open_new_python_file)  # Add 'Next' button
            ]
        ]

        for i, button in enumerate(buttons):
            button.grid(row=0, column=i, padx=8, pady=10)

        # Create product_details table if not exists
        self.create_table()

        # Create Treeview for displaying records
        self.tree = ttk.Treeview(root, columns=labels, show='headings', height=20)

        for col in labels:
            self.tree.heading(col, text=col)

        self.tree.place(x=520, y=90)

        # Fetch data and populate Treeview
        self.fetch_data()

    def create_table(self):
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS product_details (
                        CustomerId TEXT PRIMARY KEY,
                        Products TEXT,
                        Weight REAL,
                        Description TEXT,
                        Document TEXT,
                        Amount REAL,
                        MonthlyRate REAL,
                        MonthlyPayment REAL,
                        Balance REAL,
                        PayDate TEXT,
                        ModeOfPayment TEXT
                    )''')
        con.commit()
        con.close()

    def total(self):
        # Calculate monthly payment based on simple interest formula
        p, r = map(float, (self.Amount.get(), self.MonthlyRate.get()))
        m = (p * (1 + (r / 100)))  # Monthly payment formula
        self.MonthlyPayment.set(str(round(m, 2)))

    def addrecord(self):
        if any(not var.get() for var in (self.CustomerId, self.Products, self.Weight, self.Amount, self.MonthlyRate)):
            messagebox.showerror('Error', 'Please enter details.')
        elif not re.match(r'^[0-9]+$', self.CustomerId.get()):
            messagebox.showerror('Error', 'Customer ID must contain only numeric characters.')
        elif not re.match(r'^[0-9]+$', self.Weight.get()):
            messagebox.showerror('Error', 'Weight must be a numeric value.')
        elif not re.match(r'^[0-9]+(?:\.[0-9]+)?$', self.Amount.get()):
            messagebox.showerror('Error', 'Amount must be a numeric value.')
        elif not re.match(r'^[0-9]+(?:\.[0-9]+)?$', self.MonthlyRate.get()):
            messagebox.showerror('Error', 'Monthly Rate must be a numeric value.')
        else:
            self.total()
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            try:
                cur.execute("INSERT INTO product_details VALUES (?,?,?,?,?,?,?,?,?,?,?)", (                self.CustomerId.get(), self.Products.get(), float(self.Weight.get()), self.Description.get(), self.Document.get(),
                float(self.Amount.get()), float(self.MonthlyRate.get()), float(self.MonthlyPayment.get()), float(self.Balance.get()),
                self.pay_date_picker.get(), self.ModeOfPayment.get()
            ))
                con.commit()
                messagebox.showinfo("Success", "Record added successfully")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Duplicate Customer ID found")
            con.close()
            self.fetch_data()

    def upload_description(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                description_text = file.read()
            self.Description.set(description_text)

    def upload_document(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                document_data = file.read()
            # Save or process document_data as needed
            # For example, you can insert it into the Document field

    def fetch_data(self):
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute("SELECT * FROM product_details")
        rows = cur.fetchall()
        con.close()

        # Clear existing items in Treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Insert fetched data into Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def update(self):
        if self.CustomerId.get() == '':
            messagebox.showerror('Error', 'Select a record to update!')
        else:
            self.total()
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute("UPDATE product_details SET Products=?, Weight=?, Description=?, Document=?, Amount=?, MonthlyRate=?, MonthlyPayment=?, Balance=?, PayDate=?, ModeOfPayment=? WHERE CustomerId=?", (
                self.Products.get(), float(self.Weight.get()), self.Description.get(), self.Document.get(),
                float(self.Amount.get()), float(self.MonthlyRate.get()), float(self.MonthlyPayment.get()), float(self.Balance.get()),
                self.pay_date_picker.get(), self.ModeOfPayment.get(), self.CustomerId.get()
            ))
            con.commit()
            con.close()
            messagebox.showinfo('Info', 'Record updated successfully')
            self.reset()
            self.fetch_data()

    def delete(self):
        if self.CustomerId.get() == '':
            messagebox.showerror('Error', 'Enter customer ID to delete the records')
        else:
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute("DELETE FROM product_details WHERE CustomerId=?", (self.CustomerId.get(),))
            con.commit()
            con.close()
            messagebox.showinfo('Info', 'Record deleted successfully')
            self.reset()
            self.fetch_data()

    def reset(self):
        self.CustomerId.set('')
        self.Products.set('')
        self.Weight.set('')
        self.Description.delete(1.0, END)
        self.Document.set('')
        self.Amount.set('')
        self.MonthlyRate.set('')
        self.MonthlyPayment.set('')
        self.Balance.set('')
        self.pay_date_picker.set_date('')  # Reset date picker
        self.ModeOfPayment.set('')

    def open_new_python_file(self):
        subprocess.Popen(['python', 'Transaction_Details.py'])

root = Tk()
app = LoanDetails(root)
root.mainloop()

                   
