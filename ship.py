from proj import *
from drawn_object import *
from bullet import *
from vec2 import *
from mat2 import *

# Class for the player ship
class Ship(Drawn_Object):

    def __init__(self):

        # Set initial ship variables
        self.center = Vec2(0, 0)
        self.vertices = [Vec2(-10, -15), Vec2(0, 15), Vec2(10, -15)]
        self.velocity = Vec2(0, 0)
        self.lives = 3
        self.respawning = False
        self.respawn_counter = 0
        self.max_bullets = 4
        self.shot_last_frame = False
        self.frames_shot = 0
        self.queued_shots = 0
        self.score = 0
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
        # If space was not held last frame then fire
        else:
            if len(bullets) < self.max_bullets:
                bullets.append(Bullet(self))
                self.frames_shot = 0

    # Increase the score by the appropriate amount
    def increase_score(self, points, hud):

        self.score += points
        hud.set_score()

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

    digits = [[[-width + 10, height - 10],
               [-width + 20, height - 10],
               [-width + 20, height - 30],
               [-width + 10, height - 30],
               [-width + 10, height - 10]],
              [[-width + 10, height - 10],
               [-width + 15, height - 10],
               [-width + 15, height - 30],
               [-width + 10, height - 30],
               [-width + 20, height - 30]],
              [[-width + 10, height - 10],
               [-width + 20, height - 10],
               [-width + 20, height - 20],
               [-width + 10, height - 20],
               [-width + 10, height - 30],
               [-width + 20, height - 30]],
              [[-width + 10, height - 10],
               [-width + 20, height - 10],
               [-width + 20, height - 20],
               [-width + 10, height - 20],
               [-width + 20, height - 20],
               [-width + 20, height - 30],
               [-width + 10, height - 30]],
              [[-width + 10, height - 10],
               [-width + 10, height - 20],
               [-width + 20, height - 20],
               [-width + 20, height - 10],
               [-width + 20, height - 30]],
              [[-width + 20, height - 10],
               [-width + 10, height - 10],
               [-width + 10, height - 20],
               [-width + 20, height - 20],
               [-width + 20, height - 30],
               [-width + 10, height - 30]],
              [[-width + 20, height - 10],
               [-width + 10, height - 10],
               [-width + 10, height - 30],
               [-width + 20, height - 30],
               [-width + 20, height - 20],
               [-width + 10, height - 20]],
              [[-width + 10, height - 10],
               [-width + 20, height - 10],
               [-width + 10, height - 30]],
              [[-width + 10, height - 10],
               [-width + 10, height - 30],
               [-width + 20, height - 30],
               [-width + 20, height - 10],
               [-width + 10, height - 10],
               [-width + 10, height - 20],
               [-width + 20, height - 20]],
              [[-width + 10, height - 30],
               [-width + 20, height - 30],
               [-width + 20, height - 10],
               [-width + 10, height - 10],
               [-width + 10, height - 20],
               [-width + 20, height - 20]]]


    def __init__(self, player):

        # Get the player info for the HUD
        self.parent = player
        self.score_vertices = []
        self.lives_vertices = []
        self.set_score()

        # Set up the lives to be drawn
        for i in range(self.parent.lives):
            self.lives_vertices.append([Vec2(-width + 10 + (15 * i), height - 60),
                                        Vec2(-width + 15 + (15 * i), height - 40),
                                        Vec2(-width + 20 + (15 * i), height - 60),
                                        Vec2(-width + 10 + (15 * i), height - 60)])

    # Draw the HUD
    def draw_object(self):

        for element in self.lives_vertices + self.score_vertices:
            for i in range(len(element) - 1):
                self.draw_line(element[i], element[i + 1])

    # Remove a life from the HUD
    def remove_life(self):
        self.lives_vertices = self.lives_vertices[:-1]

    # Turn the score digit into a list of digit vertices
    def set_score(self):

        # Extract the digits of the score
        score_digits = extract_digits(self.parent.score)
        self.score_vertices = []

        # Loop through the digits
        for i in range(len(score_digits)):
            self.score_vertices.append([])
            # Populate this sublist with the vertices for that number
            for vertex in self.digits[score_digits[i]]:
                # The + (15 * i) is to ensure the numbers are offset appropriately
                self.score_vertices[i].append(Vec2(vertex[0] + (15 * i), vertex[1]))
