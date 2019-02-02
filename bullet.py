from proj import *
from drawn_object import *
from vec2 import *
from mat2 import *

# TODO: Add some form of interpolation to collision for bullets
class Bullet(Drawn_Object):

    def __init__(self, player):

        self.life = 500
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

    # Remove each piece of the object
    def __del__(self):

        del self.life
        del self.parent
        del self.velocity
        del self.center
        del self.vertices

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

    # Check for continuous collision
    def check_collision(self, asteroids):

        # Store current position for later
        temp_vertices = [Vec2(self.vertices[0].x, self.vertices[0].y),
                         Vec2(self.vertices[1].x, self.vertices[1].y)]

        # Basically extrude the bullet to its location next frame
        self.vertices[0] += self.velocity
        self.vertices[1] += self.velocity

        # Then check for collision with the extruded bullet
        for i in range(len(asteroids)):
            for vertex in self.vertices:
                if self._in_collision_distance(asteroids[i], vertex):
                    if self._run_collision_test(asteroids[i]):
                        self.vertices[0] = temp_vertices[0]
                        self.vertices[1] = temp_vertices[1]
                        if asteroids[i].life > 0:
                            return [True, i]

        # Restore the bullet to its actual state after checking collision
        self.vertices[0] = temp_vertices[0]
        self.vertices[1] = temp_vertices[1]
        return [False, 0]
