from turtle import *
from time import *
from math import *
from keyboard import *
from random import *

frame = 1/30
width = window_width() / 2
height = window_height() / 2

# This returns the digits of the passed number
def extract_digits(number):

    digits = []
    while number >= 10:
        digits.append(number % 10)
        number //= 10
    digits.append(number)
    digits.reverse()
    return digits
