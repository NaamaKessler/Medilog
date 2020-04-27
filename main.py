from tkinter import *

root = Tk()

# Creating label widget
# myLabel1 = Label(root, text="Hello World!")
# myLabel2 = Label(root, text="Goodbye World")

def myClick():
	myLabel = Label(root, text="Look! I clicked a buttion!!")
	myLabel.pack()


myButton = Button(root, text="Click Me!", command=myClick)

# Shoving it onto the screen

myButton.pack()
# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=1)

root.mainloop()

