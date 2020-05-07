from tkinter import *
from tkinter import ttk


root = Tk()
root.title('Medilog')
root.geometry("1300x800")

my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=15)

x_len = 1300
y_len = 800

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


num_days = 30
num_tasks = 25

# my_boxes = []
# def read_names():
# 	boxes_list = ''
# 	for boxes in my_boxes:
# 		boxes_list = boxes_list + str(boxes.get()) + '\n'
# 		my_label.config(text=boxes_list)

names = ["", "Naama", "Sergey", "Dviva", "Dviv"]
for i in range(num_tasks):
	for j in range(num_days):
		comboExample = ttk.Combobox(assignment_table, values=names, width=6)
		comboExample.grid(row=j+1, column = i+1)
		# my_boxes.append(comboExample)

# Days
day = Label(assignment_table, text="day", padx=30, bg ='#0039a1', fg='#ffffff', font=cell_font_1)
day.grid(row=0,column=0)
for i in range(num_days):
	if i < 9:
		padding = 40.45
	else:
		padding = 36.5

	day = Label(assignment_table, text=str(i+1), padx=padding, font=cell_font_2)
	day.grid(row=1+i,column=0,)

# day = Label(assignment_table, text="day", padx=30, bg ='#0039a1', fg='#ffffff', font=cell_font_1)
# day.grid(row=0,column=0,)
# day1 = Label(assignment_table, text="1", padx=40, font=cell_font_2)
# day1.grid(row=1,column=0,)

# my_button = Button(assignment_table, text="click me", command=read_names)
# my_button.grid(row=2, column=0)
# my_label = Label(assignment_table, text='')
# my_label.grid(row=3,column=0)
# class ButtonTable:
# 	def __init__(self, master, num_days, num_tasks):
# 		self.num_days = num_days
# 		self.num_tasks = num_tasks
# 		self.cat_count = 0
# 		self.buttons = list()

# 		for i in range(num_days):
# 			for j in range(num_tasks):
# 				self.buttons.append(Button(master, text="Click Me!", command=self.clicker))
# 				self.buttons[i*num_tasks+j].grid(row=i, column=j)

# 	def clicker(self):
# 		self.cat_count += 1
# 		print(self.cat_count, " cats")



# s = ButtonTable(quota_table, 10, 10)



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

