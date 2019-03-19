from proj import *
from mat2 import *

class Vec2():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __div__(self, other):
        return Vec2(self.x / other, self.y / other)

    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self

    def __mul__(self, other):
        return Vec2(self.x * other, self.y * other)

    def __imul__(self, other):
        if type(other) == Mat2:
            temp = self.x
            self.x = (self.x * other.x1 + self.y * other.x2)
            self.y = (temp * other.y1 + self.y * other.y2)
        elif type(other) == 'int' or type(other) == 'float':
            self.x *= other
            self.y *= other
        return self

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __str__(self):
        return f'{self.x}, {self.y}'

    def clamp_magnitude(self, max_magnitude):

        # If the magnitude is greater than the max set it to the max
        current_magnitude = self.get_magnitude()
        if current_magnitude > max_magnitude:
            self.set_magnitude(max_magnitude, current_magnitude)

        return self

    def set_magnitude(self, max_magnitude, current_magnitude=None):

        if current_magnitude == None:
            current_magnitude = self.get_magnitude()

        self.x = (self.x / current_magnitude) * max_magnitude
        self.y = (self.y / current_magnitude) * max_magnitude
        return self

    def get_magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y

    def get_normal(self):
        return Vec2(-self.y, self.x)
