from proj import *
from mat2 import *
from vec2 import *

class Drawn_Object:

    drawer = Turtle()
    drawer.hideturtle()
    drawer.pencolor('WHITE')

    # Initialize the object
    def __init__(self, collidable = True):

        self.num_vertices = len(self.vertices)
        if collidable:
            self.normal_vectors = self._map(range(self.num_vertices), self._get_normal_vectors)
            self.vertex_distances = self._map(range(self.num_vertices), self._get_vertex_distances)
            self.vertex_distances.sort(key=lambda dist: dist[1], reverse=True)

    # I just wrote this myself for the sake of it
    def _map(self, values, mapper):

        accumulator = []
        for value in values:
            accumulator.append(mapper(value))
        return accumulator

    # Find normals of all sides to be used for collision checking
    def _get_normal_vectors(self, i):

        next_i = i + 1
        if i  == self.num_vertices - 1:
            next_i = 0
            temp = self.vertices[next_i] - self.vertices[i]
        temp = self.vertices[next_i] - self.vertices[i]
        return temp.get_normal()

    # Get distance from center to each vertex to be used to determine if collision
    # needs to be checked
    def _get_vertex_distances(self, i):
        return (i, (self.center - self.vertices[i]).get_magnitude())

    # Draws the object
    def draw_object(self, enclosed=True):

        # Draw all edges aside from the last
        for i in range(self.num_vertices - 1):
            self.draw_line(self.vertices[i], self.vertices[i + 1])

        # Draw the closing edge if needed
        if enclosed:
            self.draw_line(self.vertices[-1], self.vertices[0])

    # Draw a line between two vertices
    def draw_line(self, start, end):

        self.drawer.penup()
        self.drawer.goto(start.x, start.y)
        self.drawer.pendown()
        self.drawer.goto(end.x, end.y)

    def move_object(self):

        vertices_out = 0

        # Move the vertices and the center of the object
        for vertex in self.vertices:
            vertex += self.velocity
            # Check for edge clipping
            vertices_out += self.check_edge(vertex)
        self.center += self.velocity

        # If all the vertices are off the screen move the object
        if vertices_out == self.num_vertices:
            if self.center.x < 0:
                self._move_to_opposite('x', 1)
            else:
                self._move_to_opposite('x', -1)
        elif vertices_out == -self.num_vertices:
            if self.center.y < 0:
                self._move_to_opposite('y', 1)
            else:
                self._move_to_opposite('y', -1)

    def rotate_object(self, dir):

        if dir == 'd':
            spin_dir = -360
        else:
            spin_dir = 360

        rotation = radians(spin_dir * frame)
        rot_matrix = Mat2(cos(rotation), sin(rotation),
                          -sin(rotation), cos(rotation))

        for vertex in self.vertices:
            vertex -= self.center
            vertex *= rot_matrix
            vertex += self.center

        # If the object rotated its normals must be recalculated
        self.normal_vectors = self._map(range(self.num_vertices),
                                        self._get_normal_vectors)

    # Add velocity to the object
    def accelerate_object(self):

        self.velocity += ((self.vertices[1] - self.center) * 2) * frame
        self.velocity.clamp_magnitude(8)

    # Remove velocity from the object
    def decelerate_object(self):

        current_speed = self.velocity.get_magnitude()
        if 0 <= current_speed <= (4 * frame):
            self.velocity = Vec2(0, 0)
        else:
            self.velocity.clamp_magnitude(current_speed - (4 * frame))

    # Check if the vertex has gone off the screen
    def check_edge(self, vertex):

        if abs(vertex.x) >= width:
            return 1
        if abs(vertex.y) >= height:
            return -1

        return 0

    # Move the object to the other side of the screen if it has clipped
    def _move_to_opposite(self, axis, direction):

        # If it clipped off the x axis flip it there
        if axis == 'x':
            move = Vec2((width * 2 + 30) * direction, 0)
        # Otherwise flip it on the y
        else:
            move = Vec2(0, (height * 2 + 30) * direction)

        # Add the flipping vector to the vertices
        for vertex in self.vertices:
            vertex += move

        # Move the center as well
        self.center += move

    # Check for continuous collision
    def continuous_collision_check(self, collidables, collidables_list=True):

        # Store current position for later
        temp_vertices = [Vec2(self.vertices[0].x, self.vertices[0].y),
                         Vec2(self.vertices[1].x, self.vertices[1].y)]

        # Basically extrude the bullet to its location next frame
        self.vertices[0] += self.velocity
        self.vertices[1] += self.velocity

        collision_data = self.collision_testing(collidables)

        self.vertices[0] = temp_vertices[0]
        self.vertices[1] = temp_vertices[1]
        return collision_data

    # Check for collision with collidables
    def collision_testing(self, collidables, collidables_list=True):

        # If we are checking for collision with multiple objects
        if collidables_list:
            for i in range(len(collidables)):
                for vertex in self.vertices:
                    if self._in_collision_distance(collidables[i], vertex):
                        if self._run_collision_test(collidables[i]):
                            return [True, i]
            return [False, None]

        # If we were only passed a single object
        for vertex in self.vertices:
            if self._in_collision_distance(collidables, vertex):
                if self._run_collision_test(collidables):
                    return True
        return False

    # Check if there is any possibility of collision
    def _in_collision_distance(self, collidable, vertex):

        # See if the collider vertex is closer to the collidable center than the collidable vertex
        if (collidable.center - vertex).get_magnitude() <= collidable.vertex_distances[0][1]:
            return True
        return False

    def _run_collision_test(self, collidable):

        # Get all the axes we need to check
        axes = self.normal_vectors + collidable.normal_vectors

        # Loop through the axes
        for axis in axes:

            # Get the min and max projections on the axis
            s_min, s_max = self._get_projections(axis)
            c_min, c_max = collidable._get_projections(axis)

            # If the projections do not overlap return False
            if (s_min < c_min and s_max < c_min) or (s_max > c_max and s_min > c_max):
                return False

        # Return True if no non overlapping axis was found
        return True

    def _get_projections(self, axis):

        # Get placeholders for projections
        min_proj = self.vertices[0].dot_product(axis)
        max_proj = min_proj

        # Loop through all vertices finding min and max projections along axis
        for vertex in self.vertices[1:]:
            dot = vertex.dot_product(axis)
            if dot < min_proj:
                min_proj = dot
            elif dot > max_proj:
                max_proj = dot

        # Return projections
        return min_proj, max_proj
