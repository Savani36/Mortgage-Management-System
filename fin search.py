import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta 
from prettytable import PrettyTable


class SearchForm:
    def __init__(self, root):
        self.root = root
        root.title("Search Customer")
        root.geometry("400x200+300+200")

        self.search_query = tk.StringVar()

        title = tk.Label(root, text="Search Details", font=("Arial", 20), bd=10, bg='seagreen', fg='white')
        title.pack(side=tk.TOP, fill=tk.X)

        search_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg='white')
        search_frame.pack(pady=20)

        lbl = tk.Label(search_frame, text="Search by Name:", font=("Comic Sans MS", 10))
        lbl.grid(row=0, column=0, padx=10, sticky="w")

        entry = tk.Entry(search_frame, font=("Comic Sans MS", 10), bd=3, textvariable=self.search_query)
        entry.grid(row=0, column=1, padx=10, sticky="w")

        btn_search = tk.Button(search_frame, text="Search", font='arial 10 bold', bg='seagreen', fg='white',
                               width=10, command=self.search_customer)
        btn_search.grid(row=0, column=2, padx=10)

        # Create Treeview for displaying search results with a vertical scrollbar
        self.tree = ttk.Treeview(root, columns=("Loan Id", "Name", "MobileNumber", "AadharNumber", "Address", "Pincode", "Amount", "Year", "Rate", "Monthly Payment", "Total Payment"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in ("Loan Id", "Name", "MobileNumber", "AadharNumber", "Address", "Pincode", "Amount", "Year", "Rate", "Monthly Payment", "Total Payment"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        # Create and set up the vertical scrollbar
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=scrollbar.set)

    def search_customer(self):
        query = self.search_query.get()

        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        conn = sqlite3.connect("loanDetails (1).db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM customer WHERE name LIKE ?
        ''', ('%' + query + '%',))
        rows = cursor.fetchall()

        if not rows:
           messagebox.showinfo("Search Result", "No customer found with the given name.")
        else:
          for row in rows:
           self.tree.insert("", "end", values=row)       

        conn.close()   


root = tk.Tk()
SearchForm(root)
root.mainloop()
