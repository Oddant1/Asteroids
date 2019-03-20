from turtle import *
from time import *
from math import *
from keyboard import *
from random import *

frame = 1/30
width = window_width() / 2
height = window_height() / 2

def extract_digits(number):

    digits = []
    while number >= 1:
        [int(number % 10)] + digits
        number = number // 10

    return digits