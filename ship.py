from proj import *
from drawn_object import *
from bullet import *
from vec2 import *
from mat2 import *

# Class for the player ship
class Ship(Drawn_Object):

    # Set initial ship variables
    center = Vec2(0, 0)
    vertices = [Vec2(-10, -15), Vec2(0, 15), Vec2(10, -15)]
    velocity = Vec2(0, 0)
    max_bullets = 4
    shot_last_frame = False
    frames_shot = 0
    queued_shots = 0

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

        # Count number of frames fire button is held
        self.frames_shot += 1
        # If there are shots queued fire them
        if self.queued_shots > 0:
            self.queued_shots -= 1
            bullets.append(Bullet(self))
            self.frames_shot = 0
            return
        # If space was pressed last frame increment the counter
        elif self.shot_last_frame:
            # This is % 25 because that's how many frames the bullets are alive
            if self.frames_shot > 0 and self.frames_shot % 25 == 0:
                self.queued_shots = self.max_bullets
        # If space was not held last frame the fire
        else:
            if len(bullets) < self.max_bullets:
                bullets.append(Bullet(self))
                self.frames_shot = 0
