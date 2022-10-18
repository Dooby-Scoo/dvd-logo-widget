import time
from tkinter import *
from screeninfo import get_monitors
from lib.bouncy_boi import *
import argparse
from lib.save_parser import SaveParser

IMAGE_W = int(339)
IMAGE_H = int(149)

parser = argparse.ArgumentParser(description='DVD Logo GUI')

parser.add_argument('--num',    type=int, default=1,  help='Number of DVD Logos')
parser.add_argument("--button", action="store_true",  help="Adds button to screen to add more DVD Logos")
parser.add_argument("--auto",   action="store_true",  help="Auto save feature")
parser.add_argument("--save",   type=str, default="", help="Path to save dir")
parser.add_argument("--load",   type=str, default="", help="Path to save dir")

args = parser.parse_args()

def generateDVDs(num):
    global dvds
    dvds = [BouncyBoi(canvas,           \
        5 * (1 if randint(0,1) else -1), \
        5 * (1 if randint(0,1) else -1),  \
        randint(int(IMAGE_W/2),            \
        primary.width - int(IMAGE_W/2)),    \
        randint(int(IMAGE_H/2),              \
        primary.height - int(IMAGE_H/2)),     \
        createImage())                         \
        for i in range(num)]

# Gets the primary monitor to size the window
for m in get_monitors():
    if m.is_primary:
        primary = m

dvds = [] # List of all dvd logo objects
q = 0     # For the quit button

widget = Tk()

widget.config(width=primary.width, height=primary.height)
widget.overrideredirect(True)
widget.config(bg = '#add123')

# -transparentcolor doesn't work on linux either. '-alpha', can be used instead.
widget.wm_attributes('-transparentcolor','#add123')
widget.attributes('-topmost',True)


canvas = Canvas(widget, width=primary.width, height=primary.height, highlightthickness=0)

# Makes the canvas transparent. This shit doesn't work on linux :(
# I currently do not have a solution for this. Good luck.
canvas.config(bg = '#add123')

canvas.pack()

# Generate logos, or load saved logos
if not args.load:
    generateDVDs(args.num)
else:
    lfile = SaveParser(args.load)
    dvd_data = lfile.load()
    # If load fails, just randomly generate logos. Will only create one if --num is not set.
    if dvd_data is None:
        generateDVDs(args.num)
    else:
        for d in dvd_data:
            dvds.append(
                BouncyBoi(canvas=canvas,
                vx=d["vx"],
                vy=d["vy"],
                x=d["x"],
                y=d["y"],
                image=loadImage(d.get("bin")))
            )

def addNew():
    global dvds
    dvds.append(BouncyBoi(canvas,   \
    5 * (1 if randint(0,1) else -1), \
    5 * (1 if randint(0,1) else -1),  \
    randint(int(IMAGE_W/2),            \
    primary.width - int(IMAGE_W/2)),    \
    randint(int(IMAGE_H/2),              \
    primary.height - int(IMAGE_H/2)),     \
    createImage()))
    updateNum()


def remove():
    global dvds
    if len(dvds) > 0:
        dvds[0].destroy()
        dvds.pop(0)
        updateNum()

def saveQuit():
    global q
    q = 1
    if args.save:
        SaveParser(args.save).save(dvds)
    widget.destroy()

# If --button is set, create buttons and a number tracker in the top left corner.
if args.button:
    exit_butt = Button(widget, width=1, height=1, text="x", command=saveQuit, bg="black", fg="white")
    butt1 = Button(widget, width=1, height=1, text="+", command=addNew, bg="black", fg="green")
    butt2 = Button(widget, width=1, height=1, text="-", command=remove, bg="black", fg="red")
    labl = Label(widget, width=2, height=1, text=f"{len(dvds)}", bg="black", fg="white")
    button1_window = canvas.create_window(0, 0, anchor=NW, window=butt1)
    button2_window = canvas.create_window(15, 0, anchor=NW, window=butt2)
    quit_window = canvas.create_window(75, 0, anchor=NW, window=exit_butt)
    labl_window = canvas.create_window(45, 0, anchor=NW, window=labl)

# Update the number of tracked logos
def updateNum():
    global labl
    labl.config(text=f"{len(dvds)}")

save_time = time.time()
while not q:
    for dvd in dvds:
        dvd.move()
    widget.update()

    # Autosave if --auto is set.
    if args.save and time.time() - save_time >= (60) and args.auto:
        save_time = time.time()
        SaveParser(args.save).save(dvds)
        print("Saved to saves\\" + args.save)
    time.sleep(0.01)

widget.mainloop()