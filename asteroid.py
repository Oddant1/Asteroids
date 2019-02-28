from proj import *
from drawn_object import *

class Asteroid(Drawn_Object):

    def __init__(self):

        self.timer = 50
        self.size = 8
        self.life = 3
        self.center = self.set_center()
        self.vertices = self.set_vertices()
        self.velocity = self.set_velocity()
        Drawn_Object.__init__(self)

    # Find the center point of this asteroid
    def set_center(self):

        x = randint(0, 1)
        y = randint(0, 1)

        if x == 0:
            x = -1
        else:
            x = 1

        if y == 0:
            y = -1
        else:
            y = 1

        # Get a random point at least 100 away from the origin on both axes
        return Vec2(x * randint(100, int(width)), y * randint(100, int(height)))

    # Set the vertices of this asteroid
    def set_vertices(self):

        return [Vec2(self.center.x - self.size * self.life, self.center.y + self.size * self.life),
                Vec2(self.center.x + self.size * self.life, self.center.y + self.size * self.life),
                Vec2(self.center.x + self.size * self.life, self.center.y - self.size * self.life),
                Vec2(self.center.x - self.size * self.life, self.center.y - self.size * self.life)]

    # Set the velocity of this asteroid
    def set_velocity(self):

        x_dir = randint(0, 1)
        y_dir = randint(0, 1)

        if x_dir == 0:
            x_dir = -1
        if y_dir == 0:
            y_dir = -1

        # Generate a random vector then clamp its magnitude to 4
        velocity = Vec2(randint(1, 100) * x_dir, randint(1, 100) * y_dir)
        #return Vec2(0, 0)
        return velocity.set_magnitude(4, velocity.get_magnitude())

    # Split the asteroid
    def split(self, asteroids):

        # If the asteroid is on its last life it splits into 4 mini particles
        splits = 2
        if self.life == 1:
            splits = 4

        # Split the asteroid into multiple smaller ones
        for split in range(splits):
            asteroids.append(Asteroid())
            asteroids[-1].center = Vec2(self.center.x, self.center.y)
            asteroids[-1].life = self.life - 1
            asteroids[-1].vertices = asteroids[-1].set_vertices()

    def decrement_timer(self):
        self.timer -= self.velocity.get_magnitude()