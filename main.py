from tkinter import *

WIDTH = 500
HEIGHT = 500
DR = 2 # Dot radius

dots = []

def click(event):
    global c, dots

    X = event.x
    Y = event.y

    dots.append([X, Y])

    draw()

def draw():
    global c, dots

    c.delete("all")

    for i in range(len(dots) - 1):
        d1 = dots[i]
        d2 = dots[i+1]

        c.create_oval(
            d1[0]-DR, d1[1]-DR, 
            d1[0]+DR, d1[1]+DR, 
            fill="black"
        )

        c.create_oval(
            d2[0]-DR, d2[1]-DR, 
            d2[0]+DR, d2[1]+DR, 
            fill="black"
        )

        c.create_line(d1[0], d1[1], d2[0], d2[1])

    l = dots[len(dots) - 1]
    c.create_oval(
        l[0]-DR, l[1]-DR, 
        l[0]+DR, l[1]+DR, 
        fill="black"
    )

def printDots(ev):
    global c, dots
    for d in dots:
        print(d)


root = Tk()

root.title("Dots & lines")
root.geometry("%dx%d+300+300" % (WIDTH, HEIGHT))

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
c.pack()

c.bind("<Button-1>", click)
c.bind("<p>", printDots)

c.focus_set()

root.mainloop()