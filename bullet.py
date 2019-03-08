from proj import *
from drawn_object import *
from vec2 import *
from mat2 import *

# TODO: Add some form of interpolation to collision for bullets
class Bullet(Drawn_Object):

    def __init__(self, player):

        self.timer = 500
        self.parent = player
        # Calculate velocity in same direction as player
        self.velocity = self._get_velocity()
        self.speed = self.velocity.get_magnitude()
        # Calculate center as point of player ship
        self.center = Vec2(self.parent.vertices[1].x, self.parent.vertices[1].y)
        # Get the vertices based on the center
        self.vertices = self._get_vertices()
        # Draw the object
        Drawn_Object.__init__(self)

    # Get the velocity of the bullet
    def _get_velocity(self):
        # Calculate in same manner as player velocity but make it faster
        return((self.parent.vertices[1] - self.parent.center).set_magnitude(20))

    # Get the center of the bullet
    def _get_center(self):
        return Vec2(self.parent.vertices[1].x, self.parent.vertices[1].y)

    # Get the vertices of the bullet
    def _get_vertices(self):

        return [self.center + Vec2(-1, 1),
                self.center + Vec2(1, 1),
                self.center + Vec2(1, -1),
                self.center + Vec2(-1, -1)]

    def decrement_timer(self):
        self.timer -= self.speed