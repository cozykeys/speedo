#!/usr/bin/env python

import math

float_format = '.3f'


def format_float(f):
    return '{f:.3f}'.format(f=f)


class Point:
    x = 0
    y = 0

    def __init__(self):
        pass

    def to_string(self):
        return '({x}, {y})'.format(
            x=format_float(self.x),
            y=format_float(self.y)
        )


class Square:
    position = Point()
    radius = 0
    angle = 0

    def __init__(self):
        pass

    def to_string(self):
        tokens = [
            'Square',
            'Position = {0}'.format(self.position.to_string()),
            'radius = {0}'.format(self.radius),
            'angle = {0}'.format(self.angle)
        ]

        return '\n\t'.join(tokens)

    def get_adjusted(self):
        radians = math.radians(self.angle)

        diameter = self.radius * 2
        adjusted_diameter = diameter * (math.sin(radians) + math.cos(radians))
        adjusted_radius = adjusted_diameter / 2

        adjusted_position = Point()
        adjusted_position.x = self.position.x - adjusted_radius
        adjusted_position.y = self.position.y - adjusted_radius

        square = Square()
        square.angle = self.angle
        square.radius = adjusted_radius
        square.position = adjusted_position

        return square


class Circle:
    position = Point()
    radius = 0

    def __init__(self):
        pass

    def get_point(self, angle):
        radians = math.radians(angle)

        x = self.radius * math.cos(radians)
        y = self.radius * math.sin(radians)

        if (x < 0.00001):
            x = 0
        if (y < 0.00001):
            y = 0

        point = Point()
        point.x = x + self.position.x
        point.y = y + self.position.y
        return point
