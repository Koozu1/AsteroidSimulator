"""
This project is a asteroid / gravity simulator. It runs at 100 ticks per second.
User can add asteroids by holding mouse click and dragging and releasing. It will define the starting velocity.
User can also click without dragging for 0 starting velocity.
User can add stationary objects by right clicking.

User can toggle trailing, stop the program, remove asteroids, remove stationary objects, define the mass
for asteroids and stationary objects, define trail lifetime.
I recommend messing around with the masses of both asteroids and stationary objects. Also adding more stationary
objects produce some interesting results!
Turn trailing of tho change its keepalive!
generally smaller mass numbers are better. Exceeding asteroid 5000 is not recommended. lowering is better!

Canvas dimensions can be changed!!! default is 800 x 1800. line 34

"""
import math
from tkinter import *



class Userinterface:
    '''
    Ui class, creates the mainwindow using tkinter library. Holds most variables.
    '''

    def __init__(self):
        self.__mainwindow = Tk()
        self.__canvasheight, self.__canvaswidth = 800, 1800
        self.__asteroids = []
        self.__stationary_asteroids = []
        self.__ticks = 0
        self.__x, self.__y, self.latest_click = 0, 0, self.__ticks
        self.__size_balancer = 1000
        self.trail_objects = []

        self.__mainwindow.bind("<Button-1>", self.click)
        self.__mainwindow.bind("<Button-3>", self.right_click)
        self.__mainwindow.bind("<ButtonRelease-1>", self.mouse_release)

        self.__frame1 = LabelFrame(self.__mainwindow,fg="white")
        self.__frame1.grid(row=0, column=0)

        self.__canvas = Canvas(self.__frame1, bg="white", height=self.__canvasheight,
                               width=self.__canvaswidth)
        self.__canvas.pack()

        self.__frame2 = LabelFrame(self.__mainwindow, bg="red", padx=15,
                                   pady=15)
        self.__frame2.grid(row=1, column=0)
        self.__stopbut = Button(self.__frame2, text="STOP!", command=self.stop).grid(row=0, column=1)
        self.__removebut = Button(self.__frame2, text="Remove all asteroids", command=self.remove_asteroids).grid(row=0,
                                                                                                                  column=3)
        self.__removebut2 = Button(self.__frame2, text="Remove all stationary objects",
                                   command=self.remove_stationaries).grid(row=0, column=4)

        self.__labelmass = Label(self.__frame2, text="MASS").grid(row=1, column=0)
        self.__entrymass = Entry(self.__frame2)
        self.__entrymass.grid(row=2, column=0)
        self.__entrymass.insert(END, '5000')

        self.__labelstationarymass = Label(self.__frame2, text="MASS for stationary").grid(row=1, column=1)
        self.__entrystationarymass = Entry(self.__frame2)
        self.__entrystationarymass.grid(row=2, column=1)
        self.__entrystationarymass.insert(END, '50000')

        self.__labeltrail = Label(self.__frame2, text="Trail lifetime seconds").grid(row=1, column=2)
        self.__entrytrail = Entry(self.__frame2)
        self.__entrytrail.grid(row=2, column=2)
        self.__entrytrail.insert(END, '5')

        self.__buttonswitch = Button(self.__frame2, text="Trailing: ON", command=self.switch)
        self.__buttonswitch.grid(row=0, column=0)
        self.__trailing = True

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

    def click(self, event):
        '''
        :param event: Mouse click down. Used for setting up release event
        :return: None
        '''
        self.__lastx, self.__lasty, self.latest_click = event.x, event.y, self.__ticks

    def right_click(self, event):
        '''
        :param event: Mouse right click event. Used for placing stationary objects to canvas.
        :return: None
        '''
        try:
            weight = int(self.__entrystationarymass.get())
            if weight < 0:
                raise ValueError
        except ValueError:
            weight = 50000
            self.__entrystationarymass.delete(0, END)
            self.__entrystationarymass.insert(0, "50000")



        item = self.__canvas.create_oval(event.x - weight / 10000, event.y - weight / 10000, event.x + weight / 10000,
                                         event.y + weight / 10000, fill="black")
        item = Asteroid(item, weight)
        self.__stationary_asteroids.append(item)

    def mouse_release(self, event):
        '''
        :param event: Release of mouse 1 event. Creates and launches a asteroid from event location
        :return: None
        '''

        x1, y1 = event.x, event.y
        vector = get_vector(x1, y1, self.__lastx, self.__lasty)
        if self.__ticks - self.latest_click < 20:
            vector = [0, 0]

        try:
            weight = int(self.__entrymass.get())
            if weight < 0:
                raise ValueError
        except ValueError:
            weight = 5000
            self.__entrymass.delete(0, END)
            self.__entrymass.insert(0, "5000")

        item = self.__canvas.create_oval(self.__lastx - weight / self.__size_balancer,
                                         self.__lasty - weight / self.__size_balancer,
                                         self.__lastx + weight / self.__size_balancer,
                                         self.__lasty + weight / self.__size_balancer)
        item = Asteroid(item, weight, vector[1] * -0.01, vector[0] * -0.01)
        self.__asteroids.append(item)

    def tick(self):
        '''
        Programs main tick. Updates path and moves non-stationary objects. Math for pathing is done here.
        :return: None
        '''
        if self.__trailing:
            try:
                int(self.__entrytrail.get()) * 100
                if int(self.__entrytrail.get()) < 0:
                    raise ValueError

            except ValueError:
                self.__entrytrail.delete(0, END)
                self.__entrytrail.insert(0, "5")
            trailalive = int(self.__entrytrail.get()) * 100


        g = 7.674 * (10 ** (-1))
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

            if self.__trailing and item.get_trail() > 9:
                item.set_trail(0)
                sizemanipulator = 2 * item.get_weight() / 10000
                trail = self.__canvas.create_oval(itemcoord[0] + ((itemcoord[2] - itemcoord[0]) / 2) - sizemanipulator,
                                                  itemcoord[1] + ((itemcoord[3] - itemcoord[1]) / 2) - sizemanipulator,
                                                  itemcoord[0] + ((itemcoord[2] - itemcoord[0]) / 2) + sizemanipulator,
                                                  itemcoord[1] + ((itemcoord[3] - itemcoord[1]) / 2) + sizemanipulator,
                                                  fill="gray", outline="")
                self.trail_objects.append((trail, self.__ticks))
            else:
                item.set_trail(item.get_trail() + abs(xy[0]) + abs(xy[1]))


            self.__canvas.move(item.get_item(), xy[0], xy[1])
        if self.__trailing:
            for obj in self.trail_objects:
                if self.__ticks - obj[1] > trailalive:
                    self.__canvas.delete(obj[0])
                    self.trail_objects.remove(obj)


        self.__ticks += 1
        self.__mainwindow.after(10, self.tick)

    def remove_asteroids(self):
        '''
        removes asteroids & trails from canvas & lists.
        :return: None
        '''
        for item in self.__asteroids:
            self.__canvas.delete(item.get_item())
        self.__asteroids.clear()
        for item in self.trail_objects:
            self.__canvas.delete(item[0])
        self.trail_objects.clear()

    def remove_stationaries(self):
        '''
        Removes stationary objects from canvas and list
        :return: None
        '''
        for item in self.__stationary_asteroids:
            self.__canvas.delete(item.get_item())
        self.__stationary_asteroids.clear()

    def switch(self):
        '''
        Switches trailing on / off
        :return: None
        '''
        if self.__trailing:
            self.__buttonswitch.configure(text="Trailing: OFF")
            self.__trailing = False
        else:
            self.__buttonswitch.configure(text="Trailing: ON")
            self.__trailing = True


def get_vector(ax, ay, bx, by):
    '''
    :param ax: A vector x component
    :param ay: A vector y component
    :param bx: B vector x component
    :param by: B vector y component
    :return: Tuple with x, y components
    '''
    a = bx - ax
    b = by - ay
    return a, b


class Asteroid:
    '''
    Asteroid class. Holds reference to canvas object. Stores weight, velocity components, trail utility integer.
    '''

    def __init__(self, item, weight, velY: float = 0, velX: float = 0):
        self.__weight = weight
        self.__velY = velY
        self.__velX = velX
        self.__obj = item
        self.__trailcounter = 0

    def get_item(self):
        return self.__obj

    def get_weight(self) -> int:
        return self.__weight

    def getvel(self) -> []:
        return [self.__velX, self.__velY]

    def set_vel(self, x, y):
        self.__velX, self.__velY = x, y
    def set_trail(self, amount):
        self.__trailcounter = amount
    def get_trail(self):
        return self.__trailcounter


def main():
    ui = Userinterface()
    ui.start()


if __name__ == "__main__":
    main()
