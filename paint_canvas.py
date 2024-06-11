from tkinter import *
from tkinter import colorchooser, ttk
from tkinter import filedialog
from PIL import ImageTk, Image, ImageEnhance, ImageFilter
import os

#fungsi untuk editing

class main:
    def __init__(self, master):
        self.master = master
        self.color_fg = 'Black'
        self.color_bg = 'white'
        self.old_x = None
        self.old_y = None
        self.pen_width = 5
        self.is_eraser = False  # Track whether the eraser mode is active
        self.drawWidgets()
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def paint(self, e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width = self.pen_width, fill = self.color_fg, capstyle='round', smooth = True)
        self.old_x = e.x
        self.old_y = e.y

    def reset(self, e):
        self.old_x = None
        self.old_y = None
    
    def changedW(self, width):
        self.pen_width = width
    
    def clearcanvas(self):
        self.c.delete(ALL)
    
    def change_fg(self):
        self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]
    
    def change_bg(self):
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg'] = self.color_bg
    
    def use_eraser(self):
        self.is_eraser = True
    
    def use_pen(self):
        self.is_eraser = False

    def drawWidgets(self):
        self.controls = Frame(self.master, padx=5, pady=5)
        textpw = Label(self.controls, text='Pen Width', font='Georgia 16')
        textpw.grid(row=0, column=0)
        self.slider = ttk.Scale(self.controls, from_=5, to=100, command=self.changedW, orient='vertical')
        self.slider.set(self.pen_width)
        self.slider.grid(row=0, column=1)
        self.controls.pack(side="left")

        # Button to activate eraser
        eraser_button = Button(self.controls, text='Eraser', command=self.use_eraser)
        eraser_button.grid(row=1, column=0)

        # Button to activate pen
        pen_button = Button(self.controls, text='Pen', command=self.use_pen)
        pen_button.grid(row=1, column=1)

        self.c = Canvas(self.master, width=500, height=400, bg=self.color_bg)
        self.c.pack(fill=BOTH, expand=True)

        menu = Menu(self.master)
        self.master.config(menu=menu)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Menu', menu=optionmenu)
        optionmenu.add_command(label='Brush Color', command=self.change_fg)
        optionmenu.add_command(label='Background Color', command=self.change_bg)
        optionmenu.add_command(label='Clear Canvas', command=self.clearcanvas)
        optionmenu.add_command(label='Exit', command=self.master.destroy)    


root = Tk()
root.title('Software Editing')
main(root)
      
root.mainloop()