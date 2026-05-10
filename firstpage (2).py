from tkinter import *
import tkinter as tk
from tkinter import ttk
import subprocess  # Import subprocess module to open another Python script

def show_tab(tab_name):
    tab_control.select(tab_name)

def show_eligibility_form(filename):
    subprocess.Popen(['python', filename])  # Open the provided Python script

def login_action(filename):
   subprocess.Popen(['python', filename]) # Here you can define the action upon pressing the login button
    
def search_form(filename):
    subprocess.Popen(['python', filename]) # Here you can define the action upon pressing the search button   

root = Tk()
root.geometry('1250x700+210+100')
root.title('Splash Form')
root.config(background='seagreen')
framebg="#EDEDED"
framefg="#06283D"

# Create tab control
tab_control = ttk.Notebook(root)

# Top frame
Label(root,text="Welcome to SBS Management System!!!",width=9,height=3,bg="#c36464",fg='#fff',font='arial 20 bold').pack(side=TOP,fill=X)

# Adding button to redirect to dashboard
redirect_tab = ttk.Frame(tab_control)
tab_control.add(redirect_tab, text='LOGIN')

# Add content to each tab
tk.Label(redirect_tab, text="LOGIN").pack()

# Create buttons to switch between tabs 
redirect_tab_button = tk.Button(root, text="LOGIN", width=15, command=lambda: login_action('regform.py'))
redirect_tab_button.pack(side=tk.TOP, padx=10, pady=5)  # Add padding

# Adding "Check Eligibility" button
check_eligibility_button = tk.Button(root, text="Check Eligibility", width=15, command=lambda: show_eligibility_form('loaneligible.py'))
check_eligibility_button.pack(side=tk.TOP, padx=10, pady=5)  # Add padding

# Adding "Search" button
search_button = tk.Button(root, text="Search", width=15, command=lambda: search_form('fin search.py'))
search_button.pack(side=tk.TOP, padx=10, pady=5)  # Add padding

# Middle text
Label(root,text="Address: Shop No 11, Service Road, Jogeshwari East, Mumbai- 400060.",width=3,height=2,bg="#c36464",fg='#fff',font='arial 15 bold').pack(side=BOTTOM,fill=X)
Label(root,text="Contact: +91-0123456789                Email: sbsmanage@gmail.com",width=3,height=2,bg="#f0687c",fg='#fff',font='arial 15 bold', anchor='center').pack(side=BOTTOM,fill=X)

# Adding image
image = tk.PhotoImage(file="lmsback.png") 
image_label = tk.Label(root, image=image)
image_label.pack()
root.mainloop()






"""from tkinter import *
import tkinter as tk
from tkinter import ttk
import subprocess  # Import subprocess module to open another Python script

def show_tab(tab_name):
    tab_control.select(tab_name)

def show_eligibility_form(filename):
    subprocess.Popen(['python', filename])  # Open the provided Python script

root = Tk()
root.geometry('1250x700+210+100')
root.title('Splash Form')
root.config(background='seagreen')
framebg="#EDEDED"
framefg="#06283D"

# Create tab control
tab_control = ttk.Notebook(root)

# Top frame
Label(root,text="Welcome to SBS Management System!!!",width=9,height=3,bg="#c36464",fg='#fff',font='arial 20 bold').pack(side=TOP,fill=X)

# Adding button to redirect to dashboard
redirect_tab = ttk.Frame(tab_control)
tab_control.add(redirect_tab, text='LOGIN')

# Add content to each tab
tk.Label(redirect_tab, text="LOGIN").pack()

# Create buttons to switch between tabs 
redirect_tab_button = tk.Button(root, text="LOGIN", width=15, command=lambda: show_tab(redirect_tab))
redirect_tab_button.pack(side=tk.TOP, padx=10, pady=5)  # Add padding

# Adding "Check Eligibility" button
check_eligibility_button = tk.Button(root, text="Check Eligibility", width=15, command=lambda: show_eligibility_form('loaneligible.py'))
check_eligibility_button.pack(side=tk.TOP, padx=10, pady=5)  # Add padding

# Adding "Search" button
search_button = tk.Button(root, text="Search", width=15)
search_button.pack(side=tk.TOP, padx=10, pady=5)  # Add padding

# Middle text
Label(root,text="Address: Shop No 11, Service Road, Jogeshwari East, Mumbai- 400060.",width=3,height=2,bg="#c36464",fg='#fff',font='arial 15 bold').pack(side=BOTTOM,fill=X)
Label(root,text="Contact: +91-0123456789                Email: sbsmanage@gmail.com",width=3,height=2,bg="#f0687c",fg='#fff',font='arial 15 bold', anchor='center').pack(side=BOTTOM,fill=X)

# Adding image
image = tk.PhotoImage(file="lmsback.png") 
image_label = tk.Label(root, image=image)
image_label.pack()
root.mainloop()"""






"""from tkinter import *
import tkinter as tk
from tkinter import ttk

def show_tab(tab_name):
    tab_control.select(tab_name)

root = Tk()
root.geometry('1250x700+210+100')
root.title('Splash Form')
root.config(background='seagreen')
framebg="#EDEDED"
framefg="#06283D"

# Create tab control
tab_control = ttk.Notebook(root)


#top frame
Label(root,text="Welcome to SBS Management System!!!",width=9,height=3,bg="#c36464",fg='#fff',font='arial 20 bold').pack(side=TOP,fill=X)


#adding button to redirect to dashboard
redirect_tab = ttk.Frame(tab_control)

tab_control.add(redirect_tab, text='LOGIN')

# Add content to each tab
tk.Label(redirect_tab, text="LOGIN").pack()

# Create buttons to switch between tabs 
redirect_tab_button = tk.Button(root, text="LOGIN" ,width=15, command=lambda: show_tab(redirect_tab))
redirect_tab_button.pack(side=tk.TOP)


#middle text
Label(root,text="Address: Shop No 11, Service Road, Jogeshwari East, Mumbai- 400060.",width=3,height=2,bg="#c36464",fg='#fff',font='arial 15 bold').pack(side=BOTTOM,fill=X)
Label(root,text="Contact: +91-0123456789                Email: sbsmanage@gmail.com",width=3,height=2,bg="#f0687c",fg='#fff',font='arial 15 bold', anchor='center').pack(side=BOTTOM,fill=X)


# Adding image
image = tk.PhotoImage(file="lmsback.png") 
image_label = tk.Label(root, image=image)
image_label.pack()
root.mainloop()"""
