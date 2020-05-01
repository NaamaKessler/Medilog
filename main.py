from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Medilog')
root.geometry("800x500")

my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=15)

x_len = 800
y_len = 500

assignment_table = Frame(my_notebook, width=x_len, height=500, bg='#0099cc')
quota_table = Frame(my_notebook, width=x_len, height=500, bg='#0066cc')
request_table = Frame(my_notebook, width=x_len, height=500, bg='#6699ff')

assignment_table.pack(fill="both", expand=1)
quota_table.pack(fill="both", expand=1)
request_table.pack(fill="both", expand=1)

my_notebook.add(assignment_table, text="Assignment Table")
my_notebook.add(quota_table, text="Quota Table")
my_notebook.add(request_table, text="Request Table")

# Creating label widget
# myLabel1 = Label(root, text="Hello World!")
# myLabel2 = Label(root, text="Goodbye World")

# def myClick():
# 	myLabel = Label(root, text="Look! I clicked a buttion!!")
# 	myLabel.pack()


# myButton = Button(root, text="Click Me!", command=myClick)

# Shoving it onto the screen

# myButton.pack()
# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=1)

root.mainloop()

