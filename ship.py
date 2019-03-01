from proj import *
from drawn_object import *
from bullet import *
from vec2 import *
from mat2 import *

# Class for the player ship
class Ship(Drawn_Object):

    # Set initial ship variables
    lives = 3
    respawned = False
    center = Vec2(0, 0)
    vertices = [Vec2(-10, -15), Vec2(0, 15), Vec2(10, -15)]
    velocity = Vec2(0, 0)

    def __init__(self):
        Drawn_Object.__init__(self)

    # Add velocity to the ship
    def accelerate_ship(self):

        self.velocity += ((self.vertices[1] - self.center) * 2) * frame
        self.velocity.clamp_magnitude(8)

    # Remove velocity from the ship
    def decelerate_ship(self):

        current_speed = self.velocity.get_magnitude()
        if 0 <= current_speed <= (4 * frame):
            self.velocity = Vec2(0, 0)
        else:
            self.velocity.clamp_magnitude(current_speed - (4 * frame))

    # Fire a bullet
    def shoot(self, bullets):
        bullets.append(Bullet(self))
