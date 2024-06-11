from tkinter import *
from tkinter import colorchooser, ttk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
import os

#buat display image
def displayimage(img):
    dispimage = ImageTk.PhotoImage(img)
    panel.configure(image=dispimage)
    panel.image = dispimage

#fungsi rotate
def rotatel():
    global img
    img = img.rotate(22.5)
    displayimage(img)

def rotater():
    global img
    img = img.rotate(-22.5)
    displayimage(img)

def rotate90():
    global img
    img = img.rotate(90)
    displayimage(img)

def rotate180():
    global img
    img = img.rotate(180)
    displayimage(img)

#fungsi mirror
def mirror():
    global img
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    displayimage(img)

root = Tk()
root.title("Image Editor")



root.mainloop()