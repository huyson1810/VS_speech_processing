import tkinter as tk
from PIL import Image, ImageTk
from tkinter import Canvas, YES, BOTH, NW

root = tk.Tk()
# file="../giphy (1).gif"
file="../virtual_ass.gif"
info = Image.open(file)

frames = info.n_frames  # gives total number of frames that gif contains

# creating list of PhotoImage objects for each frames
im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]

count = 0
anim = None
def animation(count):
    global anim
    im2 = im[count]

    gif_label.configure(image=im2)
    canvas.create_image(10, 10, image=im2, anchor=NW)
    count += 1
    if count == frames:
        count = 0
    anim = root.after(50,lambda :animation(count))

def stop_animation():
    root.after_cancel(anim)

canvas = tk.Canvas(width=700, height=600, bg='blue')
canvas.pack(expand=YES, fill=BOTH)

gif_label = tk.Label(root,image="")
gif_label.pack()

start = tk.Button(root,text="start",command=lambda :animation(count))
start.pack()

stop = tk.Button(root,text="stop",command=stop_animation)
stop.pack()

# image = ImageTk.PhotoImage(file="../virtual_ass.gif")
# canvas.create_image(10, 10, image=image, anchor=NW)

root.mainloop()