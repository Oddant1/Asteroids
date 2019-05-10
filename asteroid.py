from proj import *
from drawn_object import *

class Asteroid(Drawn_Object):

    def __init__(self, size=8, life=3, center=None, player_center=None):

        self.size = size
        self.life = life
        self.points = (100, 50, 20)[self.life - 1]
        self.center = center if center else self.set_center(player_center)
        self.vertices = self.set_vertices()
        self.velocity = self.set_velocity()
        Drawn_Object.__init__(self)

    # Find the center point of this asteroid
    def set_center(self, player_center):

        # Get the quadrant the asteroid will be in
        x = (-1, 1)[randint(0, 1)]
        y = (-1, 1)[randint(0, 1)]

        # Get a random point at least 100 away from the player on both axes
        return Vec2(x * uniform(player_center.x + 100, width),
                    y * uniform(player_center.y + 100, height))

    # Set the vertices of this asteroid
    def set_vertices(self):

        return [Vec2(self.center.x - self.size * self.life, self.center.y + self.size * self.life),
                Vec2(self.center.x + self.size * self.life, self.center.y + self.size * self.life),
                Vec2(self.center.x + self.size * self.life, self.center.y - self.size * self.life),
                Vec2(self.center.x - self.size * self.life, self.center.y - self.size * self.life)]

    # Set the velocity of this asteroid
    def set_velocity(self):

        # Get the direction of the velocity
        x_dir = (-1, 1)[randint(0, 1)]
        y_dir = (-1, 1)[randint(0, 1)]

        # Generate a random vector then clamp its magnitude to 4
        velocity = Vec2(randint(1, 100) * x_dir, randint(1, 100) * y_dir)
        return velocity.set_magnitude(4, velocity.get_magnitude())

    # Split the asteroid
    def split(self, asteroids, fragments):

        # Produce fragments from the asteroid
        for i in range(4):
            fragments.append(Fragment(self.center))

        # Split the asteroid into 2 smaller ones
        if self.life > 1:
            for i in range(2):
                asteroids.append(Asteroid(self.size - 1, self.life - 1,
                                 Vec2(self.center.x, self.center.y)))

# This is placed in the same file as asteroid to avoid circular importing
class Fragment(Asteroid):

    def __init__(self, center):

        self.timer = 50
        self.size = 0
        self.life = 0
        self.center = Vec2(center.x, center.y)
        self.vertices = self.set_vertices()
        self.velocity = self.set_velocity()
        self.speed = self.velocity.get_magnitude()
        Drawn_Object.__init__(self, False)

    def decrement_timer(self):
        self.timer -= self.speed
