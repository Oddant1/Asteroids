from proj import *
from drawn_object import *

class Asteroid(Drawn_Object):

    def __init__(self, size=8, life=3):

        self.size = size
        self.life = life
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
        return velocity.set_magnitude(4, velocity.get_magnitude())

    # Split the asteroid
    def split(self, asteroids):

        # If the asteroid is on its last life split into four fragments
        if self.life == 1:
            fragments = []
            for i in range(4):
                fragments.append(Fragment(self.center))
            return fragments

        # Split the asteroid into 2 smaller ones
        # Just doing this twice not in a loop is probably a tiny micro-optimization
        # since we know how many times it will run each time
        for i in range(2):
            asteroids.append(Asteroid())
            asteroids[-1].center = Vec2(self.center.x, self.center.y)
            asteroids[-1].life = self.life - 1
            asteroids[-1].vertices = asteroids[-1].set_vertices()


# This is placed in the same file as asteroid to avoid circular importing
class Fragment(Asteroid):

    def __init__(self, center):

        self.timer = 50
        self.size = 0
        self.life = 0
        self.center = Vec2(center.x, center.y)
        self.vertices = self.set_vertices()
        self.velocity = self.set_velocity()
        Drawn_Object.__init__(self)

    def decrement_timer(self):
        self.timer -= self.velocity.get_magnitude()
