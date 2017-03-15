from kivy.app import App

from kivy.graphics import Ellipse, Color, Rectangle
from kivy.vector import Vector

from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label

from random import random
from math import atan2, sqrt, pow, degrees, sin, cos, radians


class MainWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        in_data = {"Opera": 350,
                   "Steam": 234,
                   "Overwatch": 532,
                   "PyCharm": 485,
                   "YouTube": 221}
        position = (100, 100)
        size = (200, 200)
        chart = PieChart(data=in_data, position=position, size=size)
        self.add_widget(chart)



class PieChart(GridLayout):
    def __init__(self, data, position, size, **kwargs):
        super(PieChart, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.position = position
        self.size = size
        angle_start = 0
        count = 0
        for key, value in data.items():
            percentage = (value / sum(data.values()) * 100)
            angle_end = angle_start + 3.6 * percentage
            color = [random(), random(), random(), 1]
            # add part of Pie
            temp = PiePart(pos=self.position, size=self.size,
                           angle_start=angle_start,
                           angle_end=angle_end, color=color, name=key)
            self.add_widget(temp)
            angle_start = angle_end
            # add legend (rectangle and text)
            legend = Legend(pos=(self.position[0], self.position[1] - count * self.size[1] * 0.12),
                            size=self.size,
                            color=color,
                            name=key,
                            value=percentage)
            self.add_widget(legend)
            self.canvas.ask_update()
            self.rows += 1
            count += 1


# Class for making one part of Pie
# Main functions for handling move out/in and click inside area recognition
class PiePart(Widget):
    def __init__(self, pos, color, size, angle_start, angle_end, name, **kwargs):
        super(PiePart, self).__init__(**kwargs)
        # Window.bind(mouse_pos=self.on_mouse_pos)
        self.moved = False
        self.angle = 0
        self.name = name
        with self.canvas:
            Color(*color)
            self.c = Ellipse(pos=pos, size=size,
                             angle_start=angle_start,
                             angle_end=angle_end)

    # Function for moving part of pie outside of circle
    def move_pie_out(self):
        ang = self.c.angle_start + (self.c.angle_end - self.c.angle_start) / 2
        vector_x = cos(radians(ang - 90)) * 50
        vector_y = sin(radians(ang + 90)) * 50
        if not self.moved:
            self.c.pos = Vector(vector_x, vector_y) + self.c.pos
            self.canvas.ask_update()
            self.moved = True
        else:
            self.c.pos = Vector(-vector_x, -vector_y) + self.c.pos
            self.canvas.ask_update()
            self.moved = False

    # Function for moving part of pie inside of circle
    def move_pie_in(self):
        ang = self.c.angle_start + (self.c.angle_end - self.c.angle_start) / 2
        vector_x = cos(radians(ang - 90)) * 50
        vector_y = sin(radians(ang + 90)) * 50
        if self.moved:
            self.c.pos = Vector(-vector_x, -vector_y) + self.c.pos
            self.canvas.ask_update()
            self.moved = False

    # Click handler on Pie Part
    # If click is inside Pie Part, move it out
    def on_touch_down(self, touch):
        if self.is_inside_pie(*touch.pos):
            self.move_pie_out()

    # Function for checking if click is inside Pie Part
    def is_inside_pie(self, *touch_pos):
        y_pos = touch_pos[1] - self.c.pos[1] - self.c.size[1] / 2
        x_pos = touch_pos[0] - self.c.pos[0] - self.c.size[0] / 2
        angle = degrees(1.5707963268 - atan2(y_pos, x_pos))
        if angle < 0:
            angle += 360
        self.angle = angle
        radius = sqrt(pow(x_pos, 2) + pow(y_pos, 2))
        if self.c.angle_start < angle < self.c.angle_end:
            return radius < self.c.size[0] / 2


# Class for creating Legend
class Legend(Widget):
    def __init__(self, pos, size, color, name, value, **kwargs):
        super(Legend, self).__init__(**kwargs)
        self.name = name
        with self.canvas:
            Color(*color)
            Rectangle(pos=(pos[0] + size[0] * 1.3, pos[1] + size[1] * 0.9),
                      size=(size[0] * 0.1, size[1] * 0.1))
            self.label = Label(text=str("%.2f" % value + "% - " + name),
                               pos=(pos[0] + size[0] * 1.7, pos[1] + size[1] * 0.7),
                               halign='left',
                               text_size=(size[1], size[1] * 0.1))


class PieChartApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    PieChartApp().run()
