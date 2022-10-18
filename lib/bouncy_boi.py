from lib.image.img import *
from tkinter import *
from PIL import ImageTk

class BouncyBoi():
    def __init__(self, canvas: Canvas, vx: int, vy: int, x, y, image) -> None:
        self.canvas = canvas
        self.image_size = image.size
        self.i = ImageTk.PhotoImage(image)
        canvas.image = image
        self.image = canvas.create_image(x, y, image=self.i)
        self.vx = int(vx)
        self.vy = int(vy)
        self.x = x
        self.y = y
        self.bytes = getByteArray(image)
        self.debug_image = loadImage(self.bytes)
        
    def destroy(self):
        self.canvas.delete(self.image)

    def move(self):
        coords = self.canvas.coords(self.image)
        h = self.canvas.winfo_height()
        w = self.canvas.winfo_width()
        img_w, img_h = self.image_size
        if (coords[0] + (img_w/2) >= w or coords[0] - (img_w/2) < 0):
            self.vx *= -1
        if (coords[1] + (img_h/2) >= h or coords[1] - (img_h/2) < 0):
            self.vy *= -1
        self.canvas.move(self.image, self.vx, self.vy)
        self.x, self.y = self.canvas.coords(self.image)
