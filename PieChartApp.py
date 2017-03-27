from kivy.app import App

from kivy.graphics import Ellipse, Color, Rectangle
from kivy.vector import Vector

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.label import Label
from kivy.uix.button import Button

from random import random
from math import atan2, sqrt, pow, degrees, sin, cos, radians


class MainWindow(GridLayout):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        in_data = {"Opera": 350,
                   "Steam": 234,
                   "Overwatch": 532,
                   "PyCharm": 485,
                   "YouTube": 221}
        position = (100, 100)
        size = (250, 250)
        button = Button(text="text", width=300)
        self.add_widget(button)
        chart = PieChart(data=in_data, position=position, size=size, legend_enable=True)
        self.add_widget(chart)


class PieChart(GridLayout):
    def __init__(self, data, position, size, legend_enable=True, **kwargs):
        super(PieChart, self).__init__(**kwargs)

        # main layout parameters
        self.position = position
        self.size_mine = size
        self.col_default_width = 100
        self.data = {}
        self.cols = 2
        self.rows = 1
        self.col_force_default = True
        self.col_default_width = 300
        self.row_force_default = True
        self.row_default_height = 250
        self.size_hint_y = None
        self.size = (600, 450)
        self.temp = []

        for key, value in data.items():
            percentage = (value / sum(data.values()) * 100)
            color = [random(), random(), random(), 1]
            self.data[key] = [value, percentage, color]

        self.pie = Pie(self.data, self.position, self.size_mine)
        self.add_widget(self.pie)

        if legend_enable:
            self.legend = LegendTree(self.data, self.position, self.size_mine)
            self.add_widget(self.legend)

        self.bind(size=self._update_pie, pos=self._update_pie)

        # yellow background to check widgets size and position
        # with self.canvas:
        #    Rectangle(pos=self.pos, size=self.size, color=Color(1, 1, 0, 0.5))

    def _update_pie(self, instance, value):
        self.legend.pos = (instance.parent.pos[0], instance.parent.pos[1])
        self.pie.pos = (instance.pos[0], instance.pos[1])


class LegendTree(GridLayout):
    def __init__(self, data, position, size, **kwargs):
        super(LegendTree, self).__init__(**kwargs)

        # Legend layout parameters.
        # Initial rows is 1, then for each next data entry new one is added.
        self.cols = 1
        self.rows = 1
        self.position = position
        self.size = size
        self.row_default_height = 50
        self.spacing = 5

        count = 0
        for key, value in data.items():
            percentage = value[1]
            color = value[2]
            # add legend (rectangle and text)
            self.legend = Legend(pos=(self.position[0], self.position[1] - count * self.size[1] * 0.15),
                                 size=self.size,
                                 color=color,
                                 name=key,
                                 value=percentage)
            self.add_widget(self.legend)
            self.rows += 1
            count += 1

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.legend.pos = (instance.parent.pos[0], instance.parent.pos[1])
        self.pos = (instance.parent.pos[0] + 260, instance.parent.pos[1])


# Class for creating Legend
class Legend(FloatLayout):
    def __init__(self, pos, size, color, name, value, **kwargs):
        super(Legend, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.size_hint_x = 200
        self.size_hint_y = 50
        self.name = name
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=(pos[0] + size[0] * 1.3, pos[1] + size[1] * 0.9),
                                  size=(size[0] * 0.1, size[1] * 0.1))
            self.label = Label(text=str("%.2f" % value + "% - " + name),
                               pos=(pos[0] + size[0] * 1.3 + size[0]*0.5, pos[1] + size[1] * 0.9 - 30),
                               halign='left',
                               text_size=(size[1], size[1] * 0.1))

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = (instance.pos[0] + 100, instance.pos[1] + 100)
        self.label.pos = (instance.pos[0] + 220, instance.pos[1] + 65)


class Pie(FloatLayout):
    def __init__(self, data, position, size, **kwargs):
        super(Pie, self).__init__(**kwargs)
        self.position = position
        self.size = size
        angle_start = 0
        count = 0
        self.temp = []
        for key, value in data.items():
            percentage = value[1]
            angle_end = angle_start + 3.6 * percentage
            color = value[2]
            # add part of Pie
            self.temp.append(PieSlice(pos=self.position, size=self.size,
                                      angle_start=angle_start,
                                      angle_end=angle_end, color=color, name=key))
            self.add_widget(self.temp[count])
            angle_start = angle_end
            count += 1
        self.bind(size=self._update_temp, pos=self._update_temp)

    def _update_temp(self, instance, value):
        for i in self.temp:
            i.pos = (instance.parent.pos[0] + 55, instance.parent.pos[1] + 60)


# Class for making one part of Pie
# Main functions for handling move out/in and click inside area recognition
class PieSlice(FloatLayout):
    def __init__(self, pos, color, size, angle_start, angle_end, name, **kwargs):
        super(PieSlice, self).__init__(**kwargs)
        self.moved = False
        self.angle = 0
        self.name = name
        with self.canvas.before:
            Color(*color)
            self.slice = Ellipse(pos=pos, size=size,
                                 angle_start=angle_start,
                                 angle_end=angle_end)
        self.bind(size=self._update_slice, pos=self._update_slice)

    def _update_slice(self, instance, value):
        self.slice.pos = (instance.pos[0], instance.pos[1])

    # Function for moving part of pie outside of circle
    def move_pie_out(self):
        ang = self.slice.angle_start + (self.slice.angle_end - self.slice.angle_start) / 2
        vector_x = cos(radians(ang - 90)) * 50
        vector_y = sin(radians(ang + 90)) * 50
        if not self.moved:
            self.slice.pos = Vector(vector_x, vector_y) + self.slice.pos
            self.moved = True
        else:
            self.slice.pos = Vector(-vector_x, -vector_y) + self.slice.pos
            self.moved = False

    # Function for moving part of pie inside of circle
    def move_pie_in(self):
        ang = self.slice.angle_start + (self.slice.angle_end - self.slice.angle_start) / 2
        vector_x = cos(radians(ang - 90)) * 50
        vector_y = sin(radians(ang + 90)) * 50
        if self.moved:
            self.slice.pos = Vector(-vector_x, -vector_y) + self.slice.pos
            self.moved = False

    # Click handler on Pie Part
    # If click is inside Pie Part, move it out
    def on_touch_down(self, touch):
        if self.is_inside_pie(*touch.pos):
            self.move_pie_out()

    # Function for checking if click is inside Pie Slice
    def is_inside_pie(self, *touch_pos):
        y_pos = touch_pos[1] - self.slice.pos[1] - self.slice.size[1] / 2
        x_pos = touch_pos[0] - self.slice.pos[0] - self.slice.size[0] / 2
        angle = degrees(1.5707963268 - atan2(y_pos, x_pos))
        if angle < 0:
            angle += 360
        self.angle = angle
        radius = sqrt(pow(x_pos, 2) + pow(y_pos, 2))
        if self.slice.angle_start < angle < self.slice.angle_end:
            return radius < self.slice.size[0] / 2


class PieChartApp(App):
    def build(self):
        return MainWindow()


if __name__ == '__main__':
    PieChartApp().run()
