from tkinter import *
from PIL import Image, ImageColor
import os
from random import randint
import io

colors = [
    ImageColor.getrgb("red"),
    ImageColor.getrgb("blue"),
    ImageColor.getrgb("green"),
    ImageColor.getrgb("yellow"),
    ImageColor.getrgb("purple"),
    ImageColor.getrgb("white"),
    ImageColor.getrgb("cyan"),
    ImageColor.getrgb("orange"),
]

def generateBytes(color_index=None):
    # For debuging. Creates an image with a chosen color and returns the byte str.
    # Leave color_index none to get random color.
    # Index is the index of the above color array.
    img = createImage(color_index)
    return getByteArray(img)


def changeColor(img, nc=None):
    new_image = []
    # Picks a random color is nc is None
    new_color = colors[randint(0, len(colors)-1)] if not nc else colors[nc]
    data = img.getdata()

    for i in data:
        # No change on transparent pixels
        if not i[-1]:
            new_image.append(i)
        else:
            new_image.append(new_color+(255,))

    img.putdata(new_image)

def createImage(color_index=None):
    path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(path, "dvd.png")
    image = Image.open(image_path)
    changeColor(image, color_index)
    return image

def getByteArray(image):
    byte_arr = io.BytesIO()
    image.save(byte_arr, format="PNG")
    return byte_arr.getvalue()

def loadImage(byte_arr):
    return Image.open(io.BytesIO(byte_arr))