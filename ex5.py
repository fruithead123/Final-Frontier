from tkinter import *
import sys


root = Tk()
root.geometry("200x75+0+0")
name = StringVar()
User_input = Entry(root,textvariable = name,width=50)


    
User_input.pack()
user_problem  = User_input.get()
work = Button(root,text="Enter",width = 10,command=root.destroy).place(x=72,y=20)
root.mainloop()



