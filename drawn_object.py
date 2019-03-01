from proj import *
from mat2 import *
from vec2 import *

class Drawn_Object:

    drawer = Turtle()
    drawer.hideturtle()
    drawer.pencolor('WHITE')

    # Initialize the object
    def __init__(self):

        self.num_vertices = len(self.vertices)
        self.normal_vectors = self._map(range(self.num_vertices), self._get_normal_vectors)
        self.vertex_distances = self._map(range(self.num_vertices), self._get_vertex_distances)
        self.vertex_distances.sort(key=lambda dist: dist[1], reverse=True)

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
        # Make a get_normal method in Vec2
        return Vec2(-temp.y, temp.x)

    # Get distance from center to each vertex to be used to determing if collision
    # needs to be checked
    def _get_vertex_distances(self, i):
        return (i, (self.center - self.vertices[i]).get_magnitude())

    def draw_object(self):

        # Draw all edges aside from the last
        for i in range(self.num_vertices - 1):
            self.draw_line(self.vertices[i], self.vertices[i + 1])

        # Draw the last edge
        self.draw_line(self.vertices[-1], self.vertices[0])
        self.normal_vectors = self._map(range(self.num_vertices), self._get_normal_vectors)

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
                self.move_to_opposite('x', 1)
            else:
                self.move_to_opposite('x', -1)
        elif vertices_out == -self.num_vertices:
            if self.center.y < 0:
                self.move_to_opposite('y', 1)
            else:
                self.move_to_opposite('y', -1)

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

    # Check if the vertex has gone off the screen
    def check_edge(self, vertex):

        if abs(vertex.x) >= width:
            return 1
        if abs(vertex.y) >= height:
            return -1

        return 0

    # Move the object to the other side of the screen if it has clipped
    def move_to_opposite(self, axis, direction):

        # If it clipped off the x axis flip it there
        if axis == 'x':
            move = Vec2((width * 2 + 30) * direction, 0)
        # Otherwise flip it on the y
        else:
            move = Vec2(0, (height * 2 + 30) * direction)

        # Add the flipping vector the vertices
        for vertex in self.vertices:
            vertex += move

        # Move the center as well
        self.center += move

    # Check for collision with asteroids
    def collision_testing(self, asteroids):

        for i in range(len(asteroids)):
            for vertex in self.vertices:
                if self._in_collision_distance(asteroids[i], vertex):
                    if self._run_collision_test(asteroids[i]):
                        return [True, i]
        return [False, None]

    # Check if there is any possibility of collision
    def _in_collision_distance(self, asteroid, vertex):

        # See if the collider vertex is closer to the asteroid center than the asteroid vertex
        if (asteroid.center - vertex).get_magnitude() <= asteroid.vertex_distances[0][1]:
            return True
        return False

    def _run_collision_test(self, asteroid):

        # Get all the axes we need to check
        axes = self.normal_vectors + asteroid.normal_vectors

        # Loop through the axes
        for axis in axes:

            # Get the min and max ship projection on the axis
            s_min = self.vertices[0].dot_product(axis)
            s_max = s_min
            for s_vertex in self.vertices[1:]:
                s_dot = s_vertex.dot_product(axis)
                if s_dot < s_min:
                    s_min = s_dot
                elif s_dot > s_max:
                    s_max = s_dot

            # Get the min and max asteroid projection on the axis
            a_min = asteroid.vertices[0].dot_product(axis)
            a_max = a_min
            for a_vertex in asteroid.vertices[1:]:
                a_dot = a_vertex.dot_product(axis)
                if a_dot < a_min:
                    a_min = a_dot
                elif a_dot > a_max:
                    a_max = a_dot

            # If the projections do not overlap return False
            if (s_min < a_min and s_max < a_min) or (s_max > a_max and s_min > a_max):
                return False

        # Return True if no non overlapping axis was found
        return True
