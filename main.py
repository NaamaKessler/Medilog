from tkinter import *
from tkinter import ttk
from tkinter import font as tkFont


root = Tk()
root.title('Medilog')
root.geometry("800x500")


my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=15)

x_len = 800
y_len = 500

# Define fonts
cell_font_1 = 'Helvetica 12 bold'
cell_font_2 = 'Helvetica 10'

# Define tabs background color
tab_bg = '#0066cc'

# Define tabs
assignment_table = Frame(my_notebook, width=x_len, height=y_len, bg=tab_bg)
quota_table = Frame(my_notebook, width=x_len, height=y_len, bg=tab_bg)
request_table = Frame(my_notebook, width=x_len, height=y_len, bg=tab_bg)

assignment_table.pack(fill="both", expand=1)
quota_table.pack(fill="both", expand=1)
request_table.pack(fill="both", expand=1)

my_notebook.add(assignment_table, text="Assignment Table")
my_notebook.add(quota_table, text="Quota Table")
my_notebook.add(request_table, text="Request Table")

# drop down boxes
clicked1 = StringVar()
clicked1.set("Empty")
clicked2 = StringVar()
clicked2.set("Empty")
# clicked3 = StringVar()
# clicked3.set("Empty")
# clicked4 = StringVar()
# clicked4.set("Empty")

names = ["Naama", "Sergey", "Dviva", "Dviv"]
drop1 = OptionMenu(assignment_table, clicked1, *names)
drop1.grid(row=1, column = 1)
drop2 = OptionMenu(assignment_table, clicked2, *names)
drop2.grid(row=1, column = 2)
# drop3 = OptionMenu(assignment_table, clicked2, *names)
# drop3.pack(side = "left")
# drop4 = OptionMenu(assignment_table, clicked2, *names)
# drop4.pack(side = "right")

# Days


day = Label(assignment_table, text="day", padx=20, pady=6, bg ='#0039a1', fg='#ffffff', font=cell_font_1)
day.grid(row=0,column=0,)
day1 = Label(assignment_table, text="1", padx=32, pady=6, font=cell_font_2)
day1.grid(row=1,column=0,)


class ButtonTable:
	def __init__(self, master, num_days, num_tasks):
		self.num_days = num_days
		self.num_tasks = num_tasks
		self.cat_count = 0
		self.buttons = list()

		for i in range(num_days):
			for j in range(num_tasks):
				self.buttons.append(Button(master, text="Click Me!", command=self.clicker))
				self.buttons[i*num_tasks+j].grid(row=i, column=j)

	def clicker(self):
		self.cat_count += 1
		print(self.cat_count, " cats")


s = ButtonTable(quota_table, 3, 3)


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

