from tkinter import *
from tkinter import  ttk
from tkinter import filedialog
from tkinter.colorchooser import askcolor
import numpy as np
import numpy as np
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
import os

current_brightness = 1.0
current_contrast = 1.0
current_scale = 1.0

#fungsi mengganti gambar

def update_image_dimensions(img):
    width, height = img.size
    img_dimensions_label.config(text=f"Dimensions: {width} x {height}")


def apply_enhancements():
    global img, ori_img, cropped_img, current_brightness, current_contrast, current_scale

    if cropped_img:
        outputImage = cropped_img.copy()
    else:
        outputImage = img.copy()

    # Apply scaling
    width = int(ori_img.width * current_scale)
    height = int(ori_img.height * current_scale)
    outputImage = outputImage.resize((width, height))

    # Apply brightness enhancement
    enhancer = ImageEnhance.Brightness(outputImage)
    outputImage = enhancer.enhance(current_brightness)

    # Apply contrast enhancement
    enhancer = ImageEnhance.Contrast(outputImage)
    outputImage = enhancer.enhance(current_contrast)

    displayimage(outputImage)



def LoadImg():
    global img, ori_img
    imgname = filedialog.askopenfilename(title="Load Image")
    if imgname:
        img = Image.open(imgname)
        img = img.resize((800, 700))
        ori_img = img.copy()  # Simpan gambar asli
        displayimage(img)
        update_image_dimensions(img)
        

#buat display image
def displayimage(img):
    dispimage = ImageTk.PhotoImage(img)
    panel.configure(image=dispimage)
    panel.image = dispimage

#fungsi brightness
def brightness_callback(brightness_pos):
    global current_brightness
    current_brightness = float(brightness_pos)
    apply_enhancements()
     
#fungsi contrast
def contrast_callback(contrast_pos):
    global current_contrast
    current_contrast = float(contrast_pos)
    apply_enhancements()

# fungsi scaling image
def scale_image(scaling_pos):
    global current_scale
    current_scale = float(scaling_pos)
    apply_enhancements()

# fungsi rotasi
def rotate_image(direction):
    global img
    if img is not None:
        if direction == 'Rotate Left':
            img = img.rotate(90, expand=True)
        elif direction == 'Rotate Right':
            img = img.rotate(-90, expand=True)
        elif direction == 'Rotate 90':
            img = img.rotate(90, expand=True)
        elif direction == 'Rotate 180':
            img = img.rotate(180, expand=True)
        displayimage(img)


#fungsi mirror
def mirror():
    global img
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    displayimage(img)

#fungsi translasi
def translate_image(F, gy, gx):
    tinggi, lebar = F.shape[:2]
    G = np.zeros_like(F)
    
    for y in range(tinggi):
        for x in range(lebar):
            if (y + gy >= 0) and (y + gy < tinggi) and (x + gx >= 0) and (x + gx < lebar):
                G[y + gy, x + gx] = F[y, x]
    
    return G

def translate_callback():
    global img, ori_img
    gy = int(gy_entry.get())
    gx = int(gx_entry.get())
    img_array = np.array(img)
    translated_img_array = translate_image(img_array, gy, gx)
    translated_img = Image.fromarray(translated_img_array)
    displayimage(translated_img)

# fungsi reset image
def reset_image():
    global img, ori_img, current_brightness, current_contrast, current_scale, cropped_img
    img = ori_img.copy()  # Reset image to the original
    current_brightness = 1.0
    current_contrast = 1.0
    current_scale = 1.0
    brightnessSlider.set(current_brightness)  # Reset slider to default value
    contrastSlider.set(current_contrast)  # Reset slider to default value
    scalingSlider.set(current_scale)  # Reset slider to default value
    cropped_img = None  # Clear cropped image
    displayimage(img)
    update_image_dimensions(img)

# fungsi menyimpan gambar
def save():
    global img
    if img:
        filename = filedialog.asksaveasfilename(defaultextension=".png", 
        filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), 
        ("All files", ".")])
        if filename:
            img.save(filename)

# kelas untuk fitur paint
class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self, root):
        self.root = root

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=1)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=2)

        self.clear_button = Button(self.root, text="Clear Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=0, column=3)

        self.choose_size_button = Scale(self.root, from_=1, to=10, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=600, height=600)
        self.c.grid(row=1, columnspan=6)

        self.setup()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def clear_canvas(self):
        self.c.delete("all")

    def reset(self, event):
        self.old_x, self.old_y = None, None

def open_paint_app():
    paint_window = Toplevel(root)
    Paint(paint_window)

if __name__ == '__main__':

# MAIN LOOP 
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

def crop_image():
    global img, cropped_img, ori_img

    # Get user-entered coordinates
    x1 = int(x1_entry.get())
    y1 = int(y1_entry.get())
    x2 = int(x2_entry.get())
    y2 = int(y2_entry.get())

    # Ensure coordinates are within the image boundaries
    if (x1 >= 0 and y1 >= 0 and x2 > x1 and y2 > y1 and 
        x2 <= ori_img.width and y2 <= ori_img.height):
        
        # Crop the image from the original image
        cropped_img = ori_img.crop((x1, y1, x2, y2))
        
        # Update the displayed image
        displayimage(cropped_img)
        update_image_dimensions(cropped_img)
    else:
        print("Invalid crop coordinates. Please ensure they are within image boundaries.")



# Function to clear crop entry fields after successful crop
def clear_crop_entries():
  x1_entry.delete(0, END)
  y1_entry.delete(0, END)
  x2_entry.delete(0, END)
  y2_entry.delete(0, END)

#frame atas (tempat button)
frame_l = Frame(root, bg='white', width=350, height=300)
frame_l.pack(side=LEFT, fill=Y)

#canvas yang menampilkan gambar
frame_r = Frame(root, bg='lightgrey', width=400, height=400)
frame_r.pack(side=RIGHT, fill=BOTH, expand=True)

canvas = Canvas(frame_r, cursor="cross", bg="gray")
canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)

#gambar awal
img = Image.open("logo.png")
img = img.resize((700, 700))
ori_img = img.copy()
panel = Label(canvas)
panel.grid(row=0, column=0, rowspan=12, padx=300, pady=20)
displayimage(img)

#load image button
btnLoadImg = Button(frame_t, text='Load Image', width=15, command=LoadImg, bg="#939393",activebackground="LIGHTBLUE")
btnLoadImg.configure(font=('poppins',11,'bold'),foreground='white')
btnLoadImg.place(x=10,y=15)

img_dimensions_label = Label(frame_t, text="Dimensions: N/A", bg='grey', fg='white')
img_dimensions_label.place(x=600, y=15)

# button reset image
btnResetImg = Button(frame_t, text='Reset Image', width=15, command=reset_image, bg="#939393",activebackground="LIGHTBLUE")
btnResetImg.configure(font=('poppins', 11, 'bold'), foreground='white')
btnResetImg.place(x=180, y=15)

# button reset image
btnResetImg = Button(frame_t, text='Save', width=15, command=save, bg="#939393",activebackground="LIGHTBLUE")
btnResetImg.configure(font=('poppins', 11, 'bold'), foreground='white')
btnResetImg.place(x=350, y=15)

btncrop = Button(frame_l, text='Crop', width=10, command=crop_image)
btncrop.pack(padx=10, pady=10)

# Add labels and entry fields for crop coordinates
x1_label = Label(frame_l, text="X1:")
x1_label.pack(padx=10, pady=5)
x1_entry = Entry(frame_l)
x1_entry.pack(padx=10, pady=5)

y1_label = Label(frame_l, text="Y1:")
y1_label.pack(padx=10, pady=5)
y1_entry = Entry(frame_l)
y1_entry.pack(padx=10, pady=5)

x2_label = Label(frame_l, text="X2:")
x2_label.pack(padx=10, pady=5)
x2_entry = Entry(frame_l)
x2_entry.pack(padx=10, pady=5)

y2_label = Label(frame_l, text="Y2:")
y2_label.pack(padx=10, pady=5)
y2_entry = Entry(frame_l)
y2_entry.pack(padx=10, pady=5)

#slider untuk brightness
brightnessSlider = Scale(frame_t, label="Brightness", from_=0, to=2, orient=HORIZONTAL, length=200,
                        resolution=0.1, command=brightness_callback, bg="#616E7C")
brightnessSlider.set(1)
brightnessSlider.configure(foreground='white')
brightnessSlider.place(x=1300, y=1)

#slider untuk contrast
contrastSlider = Scale(frame_t, label="Contrast", from_=0, to=2, orient=HORIZONTAL, length=200,
                      resolution=0.1, command=contrast_callback, bg="#616E7C")
contrastSlider.set(1)
contrastSlider.configure(foreground='white')
contrastSlider.place(x=1070, y=1)

# slider untuk scaling image
scalingSlider = Scale(frame_t, label="Scale", from_=0, to=2, orient=HORIZONTAL, length=200,
                      resolution=0.1, command=scale_image, bg="#616E7C")
scalingSlider.set(current_scale)  # Set to current scaling value
scalingSlider.configure(foreground='white')
scalingSlider.place(x=840, y=1)

#dropdown rotasi
rotation_options = ["Rotate Left", "Rotate Right", "Rotate 90", "Rotate 180"]
selected_rotation = StringVar(frame_l)
selected_rotation.set('Rotation')  # default value
rotation_menu = OptionMenu(frame_l, selected_rotation, *rotation_options, command=rotate_image)
rotation_menu.configure(font=('poppins', 11))
rotation_menu.pack(padx=10, pady=10)

#button mirror
btnmirror = Button(frame_l, text='Mirror', width=10, command=mirror)
btnmirror.configure(font=('poppins', 11))
btnmirror.pack(padx=10, pady=10)

#button untuk pop up fitur paint
open_paint_button = Button(frame_l, text="Paint", width=10, command=open_paint_app)
open_paint_button.configure(font=('poppins', 11))
open_paint_button.pack(pady=20)


# Add input fields for gy and gx
gy_label = Label(frame_l, text="Vertical Shift (gy):")
gy_label.pack(padx=10, pady=5)
gy_entry = Entry(frame_l)
gy_entry.pack(padx=10, pady=5)

gx_label = Label(frame_l, text="Horizontal Shift (gx):")
gx_label.pack(padx=10, pady=5)
gx_entry = Entry(frame_l)
gx_entry.pack(padx=10, pady=5)

# button translasi
btnTranslateImg = Button(frame_l, text='Translate Image', width=15, command=translate_callback)
btnTranslateImg.pack(padx=10, pady=10)

root.mainloop()