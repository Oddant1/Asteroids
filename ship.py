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
    lives = 3
    respawning = False
    respawn_counter = 0
    max_bullets = 4
    shot_last_frame = False
    frames_shot = 0
    queued_shots = 0
    score = 1234567890

    def __init__(self):
        Drawn_Object.__init__(self)

    # Draw the ship unless it is respawning
    def draw_object(self):

        # If the player is respawning only draw them every other frame
        if not self.respawning or self.respawn_counter % 2 == 0:
            Drawn_Object.draw_object(self)
        if self.respawning:
            self.respawn_counter -= 1
            if self.respawn_counter == 0:
                self.respawning = False

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
            # This should not be hard coded, but for now it will be until I clean
            # up the code and come up with a better way of making it not like this
            if self.frames_shot > 0 and self.frames_shot % 25 == 0:
                self.queued_shots = self.max_bullets
        # If space was not held last frame the fire
        else:
            if len(bullets) < self.max_bullets:
                bullets.append(Bullet(self))
                self.frames_shot = 0

    # Respawn the ship
    def respawn(self, hud):

        # Remove a life and exit if out of lives
        self.lives -= 1
        hud.remove_life()
        #if self.lives == 0:
           #exit()

        # re-initialize ship variables
        self.center = Vec2(0, 0)
        self.vertices = [Vec2(-10, -15), Vec2(0, 15), Vec2(10, -15)]
        self.velocity = Vec2(0, 0)
        self.shot_last_frame = False
        self.frames_shot = 0
        self.queued_shots = 0
        self.respawning = True
        self.respawn_counter = 30

# This is in ship.py to prevent circular imports
class HUD(Drawn_Object):

    def __init__(self, player):

        # Get the player info for the HUD
        self.parent = player
        self.score = []
        self.lives = []

        # Set up the lives to be drawn
        for i in range(self.parent.lives):
            self. lives.append([Vec2(-width + 10 + (15 * i), height - 30),
                                Vec2(-width + 15 + (15 * i), height - 15),
                                Vec2(-width + 20 + (15 * i), height - 30)])

    # Draw the HUD
    def draw_object(self):

        for i in range(len(self.lives)):
            for j in range(len(self.lives[i]) -1):
                self.draw_line(self.lives[i][j], self.lives[i][j + 1])
            self.draw_line(self.lives[i][-1], self.lives[i][0])

    # Remove a life from the HUD
    def remove_life(self):
        self.lives = self.lives[:-1]
