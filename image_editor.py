from tkinter import *
from tkinter import  ttk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
import os

#buat display image
def displayimage(img):
    dispimage = ImageTk.PhotoImage(img)
    panel.configure(image=dispimage)
    panel.image = dispimage

#fungsi rotate kiri
def rotatel():
    global img
    img = img.rotate(22.5)
    displayimage(img)

#fungsi rotate kanan
def rotater():
    global img
    img = img.rotate(-22.5)
    displayimage(img)

#fungsi rotate 90
def rotate90():
    global img
    img = img.rotate(90)
    displayimage(img)

#fungsi rotate 180
def rotate180():
    global img
    img = img.rotate(180)
    displayimage(img)

#fungsi mirror
def mirror():
    global img
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    displayimage(img)

#fungsi brightness
def brightness_callback(brightness_pos):
	brightness_pos = float(brightness_pos)
	global outputImage
	enhancer = ImageEnhance.Brightness(img)
	outputImage = enhancer.enhance(brightness_pos)
	displayimage(outputImage)
     
#fungsi contrast
def contrast_callback(contrast_pos):
	contrast_pos = float(contrast_pos)
	global outputImage
	enhancer = ImageEnhance.Contrast(img)
	outputImage = enhancer.enhance(contrast_pos)
	displayimage(outputImage)
     
#fungsi mengganti gambar
def LoadImg():
	global img
	imgname = filedialog.askopenfilename(title="Load Image")
	if imgname:
		img = Image.open(imgname)
		img = img.resize((600, 600))
		displayimage(img)

root = Tk()
root.title("Image Editor")

space=(" ")*215
# It retrieves the screen width of the user's display
screen_width=root.winfo_screenwidth()

# It retrieves the screen height of the user's display
screen_height = root.winfo_screenheight()

#Using an f-string to construct the window size in the 
#format width x height
root.geometry(f"{screen_width}x{screen_height}")

#frame atas (tempat slider brightness & contrass, load & save img)
frame_t = Frame(root, bg='grey', width=400, height=60)
frame_t.pack(side=TOP, fill=X)

#frame atas (tempat button)
frame_l = Frame(root, bg='lightgreen', width=200, height=300)
frame_l.pack(side=LEFT, fill=Y)

#canvas yang menampilkan gambar
frame_r = Frame(root, bg='lightgrey', width=400, height=400)
frame_r.pack(side=RIGHT, fill=BOTH, expand=True)

canvas = Canvas(frame_r, cursor="cross", bg="gray")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)

#gambar awal
img = Image.open("logo.png")
img = img.resize((700, 700))
panel = Label(canvas)
panel.grid(row=0, column=0, rowspan=12, padx=300, pady=20)
displayimage(img)

#load image button
btnLoadImg = Button(frame_l, text='Load Image', width=15,command=LoadImg,bg="#1f242d",activebackground="ORANGE")
btnLoadImg.configure(font=('poppins',11,'bold'),foreground='white')
btnLoadImg.place(x=10,y=30)

root.mainloop()