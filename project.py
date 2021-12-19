"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Student Id: 150281999
Name:       Onni Pylvänen
Email:      onni.pylvanen@tuni.fi

Program description goes here...
"""
import math
from tkinter import *
from tkinter import ttk


class Userinterface:

    def __init__(self):
        self.__mainwindow = Tk()
        self.__x, self.__y = 0, 0
        self.__asteroids = []
        self.__stationary_asteroids = []

        self.__mainwindow.bind("<Motion>", self.motion)
        self.__mainwindow.bind("<Button-1>", self.click)
        self.__mainwindow.bind("<Button-3>", self.right_click)

        self.__frame1 = LabelFrame(self.__mainwindow, text="Fruit", bg="green",
                                   fg="white", padx=15, pady=15)
        self.__frame1.grid(row=0, column=0)

        self.__canvas = Canvas(self.__frame1, bg="white", height=800,
                               width=1000)
        self.__canvas.pack()
        self.__oval = self.__canvas.create_oval(60, 60, 210, 210)

        self.__frame2 = LabelFrame(self.__mainwindow, bg="red", padx=15,
                                   pady=15)
        self.__frame2.grid(row=1, column=0)
        self.__sumbut = Button(self.__frame2, text="TYUS").grid(row=0, column=0)
        self.__stopbut = Button(self.__frame2, text="STOP!", command=self.stop).grid(row=0, column=1)
        self.removebut = Button(self.__frame2, text="Remove all asteroids", command=self.remove_asteroids).grid(row=0,
                                                                                                                column=3)
        self.removebut2 = Button(self.__frame2, text="Remove all stationary objects",
                                 command=self.remove_stationaries).grid(row=0, column=4)

        self.tick()

    def stop(self):
        """
        Ends the execution of the program.
        """

        self.__mainwindow.destroy()

    def start(self):
        """
        Starts the mainloop.
        """
        self.__mainwindow.mainloop()

    def motion(self, event):
        self.__x, self.__y = event.x, event.y
        coords = self.__canvas.coords(self.__oval)
        xycoords = [(coords[0] + (coords[2] - coords[0]) / 2), coords[1] + ((coords[3] - coords[1]) / 2)]

        try:
            self.__canvas.move(self.__oval, ((self.__x - xycoords[0]) * 2) / (abs(self.__x - xycoords[0])),
                               ((self.__y - xycoords[1]) * 2) / abs(self.__y - xycoords[1]))
        except ZeroDivisionError:
            pass

    def click(self, event):
        weight = 10000
        item = self.__canvas.create_oval(event.x - weight / 1000, event.y - weight / 1000, event.x + weight / 1000,
                                         event.y + weight / 1000)
        item = Asteroid(item, weight)
        self.__asteroids.append(item)

    def right_click(self, event):
        weight = 100000
        item = self.__canvas.create_oval(event.x - weight / 10000, event.y - weight / 10000, event.x + weight / 10000,
                                         event.y + weight / 10000)
        item = Asteroid(item, weight)
        self.__stationary_asteroids.append(item)

    def tick(self):
        g = 7.674 * (10 ** (-2))
        for item in self.__asteroids:
            itemcoord = self.__canvas.coords(item.get_item())

            for otheritem in self.__asteroids:
                if item != otheritem:
                    othercoords = self.__canvas.coords(otheritem.get_item())
                    vec = get_vector(itemcoord[0], itemcoord[1], othercoords[0], othercoords[1])
                    separation = math.dist([vec[0], vec[1]], [othercoords[0], othercoords[1]])
                    force = g * ((item.get_weight() * otheritem.get_weight()) / (separation ** 2))
                    magnitude = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
                    normal = (vec[0] / magnitude, vec[1] / magnitude)
                    a = force / item.get_weight()
                    item.set_vel(item.getvel()[0] + a * normal[0], item.getvel()[1] + a * normal[1])

            for stationary in self.__stationary_asteroids:
                othercoords = self.__canvas.coords(stationary.get_item())
                vec = get_vector(itemcoord[0], itemcoord[1], othercoords[0], othercoords[1])
                separation = math.dist([vec[0], vec[1]], [othercoords[0], othercoords[1]])
                force = g * ((item.get_weight() * stationary.get_weight()) / (separation ** 2))
                magnitude = math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
                normal = (vec[0] / magnitude, vec[1] / magnitude)
                a = force / item.get_weight()
                item.set_vel(item.getvel()[0] + a * normal[0], item.getvel()[1] + a * normal[1])

            xy = [item.getvel()[0] / 2, item.getvel()[1] / 2]
            self.__canvas.move(item.get_item(), xy[0], xy[1])

        self.__mainwindow.after(10, self.tick)

    def remove_asteroids(self):
        for item in self.__asteroids:
            self.__canvas.delete(item.get_item())
        self.__asteroids.clear()

    def remove_stationaries(self):
        for item in self.__stationary_asteroids:
            self.__canvas.delete(item.get_item())
        self.__stationary_asteroids.clear()


def get_vector(ax, ay, bx, by):
    a = bx - ax
    b = by - ay
    return a, b


def normalize(x, y):
    if x < y:
        return 1, y / x
    return x / y, 1


class Asteroid:

    def __init__(self, item, weight, velY: float = 0, velX: float = 0):
        self.__weight = weight
        self.__velY = velY
        self.__velX = velX
        self.__obj = item

    def get_item(self):
        return self.__obj

    def get_weight(self) -> int:
        return self.__weight

    def getvel(self) -> []:
        return [self.__velX, self.__velY]

    def set_vel(self, x, y):
        self.__velX, self.__velY = x, y


def main():
    ui = Userinterface()
    ui.start()


if __name__ == "__main__":
    main()

'''
root = Tk()

# create canvas
myCanvas = Canvas(root, bg="white", height=300, width=500)

# draw arcs
coord = 10, 10, 300, 300
arc = myCanvas.create_arc(coord, start=0, extent=150, fill="red")
arv2 = myCanvas.create_arc(coord, start=150, extent=215, fill="green")

# add to window and show
myCanvas.pack()
root.mainloop()
'''
