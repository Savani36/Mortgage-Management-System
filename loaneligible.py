import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import ttk

class LoanEligibilityForm:
    def __init__(self, root):
        self.root = root
        root.title("Loan Eligibility Form")
        root.geometry("1500x850+0+0")

        self.counter = 0  # Counter for generating ID

        self.loan_on, self.purpose, self.gold_type, self.product_weight, self.date, self.age = (tk.StringVar() for _ in range(6))

        title = tk.Label(root, text="Loan Eligibility", font=("Arial", 20), bd=10, bg='seagreen', fg='white')
        title.pack(side=tk.TOP, fill=tk.X)

        input_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg='white')
        input_frame.place(x=550, y=70, width=500, height=420)

        labels = ["Loan On (product)", "Purpose of Loan", "Gold Type", "Product Weight (in grams)", "Date of Birth", "Age"]

        self.entry_fields = []

        for i, label in enumerate(labels):
            lbl = tk.Label(input_frame, text=label, font=("Comic Sans MS", 10))
            lbl.grid(row=i, column=0, pady=10, padx=20, sticky="w")

        # Dropdown options for Loan On (product)
        loan_options = ["Earrings", "Bangles", "Necklace", "Gold Biscuit", "Chain"]
        self.loan_on.set(loan_options[0])  # Set default value

        loan_dropdown = tk.OptionMenu(input_frame, self.loan_on, *loan_options)
        loan_dropdown.config(font=("Comic Sans MS", 10), bd=3)
        loan_dropdown.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        self.entry_fields.append(self.loan_on)

        # Dropdown options for Purpose of Loan
        purpose_options = ["Home", "Car", "Education", "Medical", "Wedding"]
        self.purpose.set(purpose_options[0])  # Set default value

        purpose_dropdown = tk.OptionMenu(input_frame, self.purpose, *purpose_options)
        purpose_dropdown.config(font=("Comic Sans MS", 10), bd=3)
        purpose_dropdown.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        self.entry_fields.append(self.purpose)

        # Dropdown options for Gold Type
        gold_type_options = ["With Stone", "Solid", "With Meena"]
        self.gold_type.set(gold_type_options[0])  # Set default value

        gold_type_dropdown = tk.OptionMenu(input_frame, self.gold_type, *gold_type_options)
        gold_type_dropdown.config(font=("Comic Sans MS", 10), bd=3)
        gold_type_dropdown.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        self.entry_fields.append(self.gold_type)

        # Entry field for Product Weight
        self.product_weight_entry = tk.Entry(input_frame, font=("Comic Sans MS", 10), bd=3, textvariable=self.product_weight, width=15)
        self.product_weight_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        self.entry_fields.append(self.product_weight)

        # Date of Birth Entry field
        self.date_entry = DateEntry(input_frame, font=("Comic Sans MS", 10), bd=3, textvariable=self.date, date_pattern='yyyy-mm-dd', 
                                     command=self.calculate_age)
        self.date_entry.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        self.entry_fields.append(self.date)

        # Label for displaying age
        self.age_label = tk.Label(input_frame, font=("Comic Sans MS", 10), bd=3)
        self.age_label.grid(row=5, column=1, pady=10, padx=10, sticky="w")

        # Note at the footer of the form
        note_label = tk.Label(root, text="Note: It should be noted that the final gold loan eligibility value will be arrived at only after a detailed in-house evaluation of the gold by our finance’s experienced team. Apart from the weight of the gold, the purity of the gold and the rate of gold on a particular day is also taken into consideration for calculating one’s eligibility.", font=("Arial", 9), wraplength=780, justify="left", bd=10)
        note_label.place(x=425, y=600)

        # Frame for submit button
        submit_frame = tk.Frame(root, bg='white')
        submit_frame.place(x=550, y=520, width=500, height=30)

        submit_button = tk.Button(submit_frame, text="Submit Record", command=self.submit_form, font='arial 10 bold', bg='seagreen', fg='white')
        submit_button.pack(side=tk.TOP, pady=5, padx=10)


    def calculate_age(self, event=None):
        date_of_birth = self.date_entry.get_date()
        if date_of_birth:
            today = datetime.today()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            self.age.set(str(age))
            self.age_label.config(text=str(age))

    def submit_form(self):
        # Calculate age if not calculated
        self.calculate_age()

        # Validation for Loan On (product)
        if not self.loan_on.get():
            messagebox.showerror("Error", "Please select a valid option from Loan On (product)")
            return

        # Validation for all fields
        for field in self.entry_fields:
            if isinstance(field, tk.StringVar) and not field.get():
                messagebox.showerror("Error", "Please fill in all the fields")
                return

        # Validation for Product Weight
        product_weight = self.product_weight.get()
        try:
            float(product_weight)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for product weight. Only numeric input is allowed.")
            return

        # Validation for Age
        age = self.age_label.cget("text")
        if not age:
            messagebox.showerror("Error", "Please calculate age before submitting the form")
            return
        if int(age) < 20:
            messagebox.showerror("Error", "Sorry, you need to be at least 20 years old to be eligible for a loan.")
            return

        # Popup message for successful submission
        messagebox.showinfo("Success", "You are eligible for loan!")

        # Clearing input fields
        for field in self.entry_fields:
            if isinstance(field, tk.StringVar):
                field.set("")
            elif isinstance(field, DateEntry):
                field.delete(0, tk.END)
        self.age.set("")  # Clear age after submission

        # Close the window after successful submission
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    loan_eligibility_form = LoanEligibilityForm(root)
    root.mainloop()
