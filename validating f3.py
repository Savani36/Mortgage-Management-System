import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import re
from datetime import datetime
from datetime import timedelta

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3
import re
from datetime import datetime
from datetime import timedelta

class LoanManager:
    def __init__(self, root):
        root.title("Loan Management System")
        root.geometry("1100x600+0+0")

        # Create the database table
        self.create_database()

        title = tk.Label(root, text="Loan Management System", font=("Arial", 20), bd=10, bg='seagreen', fg='white')
        title.pack(side=tk.TOP, fill=tk.X)

        self.TransactionId, self.CustomerId, self.InstallmentDate, self.PaymentDate, self.Principal, self.Interest, self.Total, self.Status = (
            tk.StringVar() for _ in range(8)
        )

        Detail_F = tk.Frame(root, bd=4, relief=tk.RIDGE, bg='white')
        Detail_F.place(x=10, y=90, width=500, height=500)

        labels = ["Transaction ID", "Customer ID", "Installment Date", "Payment Date", "Principal", "Interest",
                  "Total", "Status"]

        for i, label in enumerate(labels):
            lbl = tk.Label(Detail_F, text=label, font=("Comic Sans MS", 10))
            lbl.grid(row=i, column=0, pady=10, padx=20, sticky="w")

        entries = [
            tk.Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=var) for var in
            [self.TransactionId, self.CustomerId, self.Principal, self.Interest, self.Total, self.Status]
        ]  

        for i, entry in enumerate(entries):
            entry.grid(row=i, column=1, pady=10, sticky="w")


        self.installment_date_picker = DateEntry(Detail_F, width=12, background='darkblue', foreground='white',
                                                  borderwidth=2, date_pattern='yyyy-mm-dd', textvariable=self.InstallmentDate)
        self.installment_date_picker.grid(row=2, column=1, pady=10, sticky="w")

        self.interest_entry = tk.Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.Interest)
        self.interest_entry.grid(row=5, column=1, pady=10, sticky="w")

        self.payment_date_picker = DateEntry(Detail_F, width=12, background='darkblue', foreground='white',
                                              borderwidth=2, date_pattern='yyyy-mm-dd', textvariable=self.PaymentDate)
        self.payment_date_picker.grid(row=3, column=1, pady=10, sticky="w")

        self.principal_var = tk.StringVar()  # Separate StringVar for Principal
        self.principal_entry = tk.Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.principal_var)
        self.principal_entry.grid(row=4, column=1, pady=10, sticky="w")

        self.total_var = tk.StringVar()  # Separate StringVar for Total
        self.total_entry = tk.Entry(Detail_F, font=("Comic Sans MS", 10), bd=3, textvariable=self.total_var)
        self.total_entry.grid(row=6, column=1, pady=10, sticky="w")

        status_values = ['paid', 'ongoing']
        self.StatusCombo = ttk.Combobox(Detail_F, values=status_values, textvariable=self.Status, state='readonly', width=15)
        self.StatusCombo.grid(row=len(labels)-1, column=1, pady=10, sticky="w")

        btnFrame = tk.Frame(root, bd=5, relief=tk.RIDGE)
        btnFrame.place(x=10, y=630, width=500, height=60)

        buttons = [
            tk.Button(btnFrame, text=label, font='arial 10 bold', bg='seagreen', fg='white', width=10, command=command)
            for label, command in [
                ('Add Record', self.add_record),
                ('Update', self.update),
                ('Delete', self.delete),
                ('Reset', self.reset)
            ]
        ]

        for i, button in enumerate(buttons):
            button.grid(row=0, column=i, padx=8, pady=10)

        # Data Grid
        self.tree_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
        self.tree_frame.place(x=520, y=90, width=950, height=500)

        self.tree_scroll_y = ttk.Scrollbar(self.tree_frame, orient=tk.VERTICAL)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = ttk.Scrollbar(self.tree_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.tree = ttk.Treeview(self.tree_frame, column=("Transaction ID", "Customer ID", "Installment Date", "Payment Date", "Principal", "Interest", "Total", "Status"), yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree.heading("#0", text="ID")
        self.tree.heading("#1", text="Transaction ID")
        self.tree.heading("#2", text="Customer ID")
        self.tree.heading("#3", text="Installment Date")
        self.tree.heading("#4", text="Payment Date")
        self.tree.heading("#5", text="Principal")
        self.tree.heading("#6", text="Interest")
        self.tree.heading("#7", text="Total")
        self.tree.heading("#8", text="Status")
        self.tree.pack(fill=tk.BOTH, expand=1)

        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # Fetch and display data
        self.fetch_data()

        # Note above buttons
        self.note_label = tk.Label(root, text=" NOTE : EMI charges are changed on a daily basis as per the current day's gold rate.", font=("Arial", 10), bd=5, bg='seagreen', fg='white')
        self.note_label.place(x=560, y=660, anchor='w')

    def create_database(self):
        try:
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS transactionDetails (
                            TransactionId INTEGER PRIMARY KEY,
                            CustomerId INTEGER,
                            InstallmentDate DATE,
                            PaymentDate DATE,
                            Principal REAL,
                            Interest REAL,
                            Total REAL,
                            Status TEXT
                        )''')
            con.commit()
        except Exception as e:
            messagebox.showerror('Error', f'Error creating database: {str(e)}')
        finally:
            if con:
                con.close()

    def is_valid_customer_id(self, customer_id):
        return customer_id.isdigit() and len(customer_id) == 3

    def is_valid_transaction_id(self, transaction_id):
        return transaction_id.isdigit() and len(transaction_id) == 3

    def is_valid_amount(self, amount):
        return re.match(r'^\d*\.?\d*$', amount) is not None

    def is_valid_date(self, date_str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert to date object
            return True, date_obj
        except ValueError:
            return False, None


    def add_record(self):
    # Check if any fields are empty
        if any(not var.get() for var in (self.TransactionId, self.CustomerId, self.principal_var, self.Interest, self.total_var, self.Status)):
            messagebox.showerror('Error', 'Please enter all details.')
            return

        # Check if Customer ID and Transaction ID are numeric
        if not self.is_valid_transaction_id(self.TransactionId.get()):
            messagebox.showerror('Error', 'Invalid Transaction ID. Please enter a valid numeric value.')
            return

        if not self.is_valid_customer_id(self.CustomerId.get()):
            messagebox.showerror('Error', 'Invalid Customer ID. Please enter a valid numeric value.')
            return
        
        # Check if Principal, Interest, and Total are numeric
        if not self.is_valid_amount(self.Interest.get()) or not self.is_valid_amount(self.total_var.get()) or not self.is_valid_amount(self.principal_var.get()):
            messagebox.showerror('Error', 'Invalid amount. Please enter numeric value.')
            return

        # Check if Installment Date is valid
        valid_installment, installment_date = self.is_valid_date(self.InstallmentDate.get())
        if not valid_installment:
            messagebox.showerror('Error', 'Invalid Installment Date format. Please enter date in YYYY-MM-DD format.')
            return

        # Check if Payment Date is valid and after Installment Date by at least three days
        valid_payment, payment_date = self.is_valid_date(self.PaymentDate.get())
        if not valid_payment:
            messagebox.showerror('Error', 'Invalid Payment Date format. Please enter date in YYYY-MM-DD format.')
            return

        # Convert Installment Date and Payment Date strings to datetime objects
        installment_date = datetime.strptime(self.InstallmentDate.get(), '%Y-%m-%d').date()
        payment_date = datetime.strptime(self.PaymentDate.get(), '%Y-%m-%d').date()

        # Calculate the minimum allowed Payment Date (three days after Installment Date)
        min_allowed_payment_date = installment_date + timedelta(days=3)

        if payment_date < min_allowed_payment_date:
            messagebox.showerror('Error', 'Payment Date must be at least three days after Installment Date.')
            return


        # If all validations pass, proceed with database insertion
        con = sqlite3.connect('loanDetails.db')
        cur = con.cursor()
        cur.execute("INSERT INTO transactionDetails (TransactionId, CustomerId, InstallmentDate, PaymentDate, Principal, Interest, Total, Status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (self.TransactionId.get(), self.CustomerId.get(), self.InstallmentDate.get(), self.PaymentDate.get(), 
                 self.principal_var.get(), self.Interest.get(), self.total_var.get(), self.Status.get()))
        con.commit()
        con.close()
        messagebox.showinfo('Success', 'Record added successfully.')
        self.fetch_data()
        con.close()

    def update(self):
        if not self.TransactionId.get():
            messagebox.showerror('Error', 'Select a record to update!')
        elif not self.is_valid_customer_id(self.CustomerId.get()):
            messagebox.showerror('Error', 'Invalid Customer ID. Please enter a valid numeric value.')
        elif not self.is_valid_amount(self.Interest.get()) or not self.is_valid_amount(self.total_var.get()) or not self.is_valid_amount(self.principal_var.get()):
            messagebox.showerror('Error', 'Invalid amount. Please enter numeric value.')
        elif not self.is_valid_date(self.InstallmentDate.get()) or not self.is_valid_date(self.PaymentDate.get()):
            messagebox.showerror('Error', 'Invalid date format or date cannot be in the future.')
        else:
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute("UPDATE transactionDetails SET CustomerId=?, InstallmentDate=?, PaymentDate=?, Principal=?, Interest=?, Total=?, Status=? WHERE TransactionId=?",
                        (self.CustomerId.get(), self.InstallmentDate.get(), self.PaymentDate.get(), 
                         self.principal_var.get(), self.Interest.get(), self.total_var.get(), self.Status.get(), self.TransactionId.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Record updated successfully.')
            self.fetch_data()
            self.reset()

    def delete(self):
        if not self.TransactionId.get():
            messagebox.showerror('Error', 'Select a record to delete!')
        else:
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute("DELETE FROM transactionDetails WHERE TransactionId=?", (self.TransactionId.get(),))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Record deleted successfully.')
            self.fetch_data()
            self.reset()

    def reset(self):
        self.TransactionId.set('')
        self.CustomerId.set('')
        self.InstallmentDate.set('')
        self.PaymentDate.set('')
        self.Principal.set('')
        self.Interest.set('')
        self.total_var.set('')
        self.Status.set('')
        self.principal_var.set('')

    def fetch_data(self):
        try:
            con = sqlite3.connect('loanDetails.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM transactionDetails")
            rows = cur.fetchall()
            for row in rows:
                self.tree.insert('', 'end', text=row[0], values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        except Exception as e:
            messagebox.showerror('Error', f'Error fetching data: {str(e)}')
        finally:
            if con:
                con.close()

root = tk.Tk()
app = LoanManager(root)
root.mainloop()
