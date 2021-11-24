from tkinter import *
from reduce import *

WIDTH = 500
HEIGHT = 500

MX = 0
MY = 0

DEBUG = False

AMP = 10

dots = []
r = Reduce(dots, AMP)

def click(event):
    global c, dots

    X = event.x
    Y = event.y

    dots.append([X, Y])

    draw()

def draw():
    global c, dots

    c.delete("all")

    c.create_text(
        10,20,
        text="%d, %d" % (MX, MY),
        fill="grey",
        anchor=SW
    )

    if len(dots) == 0: return

    f = dots[0]
    dot(f[0], f[1])

    for i in range(len(dots) - 1):
        d1 = dots[i]
        d2 = dots[i+1]

        dot(d2[0], d2[1])

        c.create_line(d1[0], d1[1], d2[0], d2[1])

    if DEBUG:
        draw_debug()

def letsReduceIt(ev):
    global c, dots

    r.reduce()

    draw()

def clearArray(ev):
    global dots, r

    dots = []
    r = Reduce(dots, AMP)
    draw()

def dot(x, y):
    global c
    DR = 2 # Dot radius
    
    c.create_oval(
        x-DR, y-DR, 
        x+DR, y+DR, 
        fill="black"
    )

def dotD(x, y):
    global c

    c.create_oval(
        x-AMP, y-AMP, 
        x+AMP, y+AMP, 
        outline="red"
    )

def move(ev):
    global MX, MY

    MX = ev.x
    MY = ev.y
    
    draw()

def draw_debug():
    global c, r

    f = dots[0]
    dotD(f[0], f[1])
    
    for i in range(len(dots) - 1):
        d1 = dots[i]
        d2 = dots[i+1]

        dotD(d2[0], d2[1])

    areas = r.getDebugDots()

    for area in areas:
        c.create_line(area[0][0], area[0][1], area[1][0], area[1][1])
        c.create_line(area[1][0], area[1][1], area[2][0], area[2][1])
        c.create_line(area[2][0], area[2][1], area[3][0], area[3][1])
        c.create_line(area[3][0], area[3][1], area[0][0], area[0][1])

def debug(ev):
    global DEBUG
    DEBUG = not DEBUG

    draw()

root = Tk()

root.title("Dots & lines")
root.geometry("%dx%d+300+300" % (WIDTH, HEIGHT))

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
c.pack()

c.bind("<Button-1>", click)
root.bind("<Motion>", move)
root.bind("<r>", letsReduceIt)
root.bind("<d>", debug)
root.bind("<c>", clearArray)

root.mainloop()