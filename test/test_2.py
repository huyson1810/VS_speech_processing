from tkinter import *
from PIL import ImageTk

canvas = Canvas(width=1000, height=800, bg='blue')
canvas.pack(expand=YES, fill=BOTH)

image = ImageTk.PhotoImage(file="../virtual_ass.gif")
canvas.create_image(10, 10, image=image, anchor=NW)

mainloop()