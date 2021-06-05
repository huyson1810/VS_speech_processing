from tkinter import *

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('800x800')

canvas = Canvas(window, width=800, height=600, bg='black')
canvas.grid(column=0,row =0)

lbl = Label(window, text="Hello")

lbl.grid(column=0, row=0)

btn = Button(window, text="Click Me")

btn.grid(column=1, row=0)

btn1 = Button(window, text='Start', width=20, bg='#5C85FB')
btn1.config(font=("Courier", 12))
btn1.grid(column=1, row=0)

window.mainloop()