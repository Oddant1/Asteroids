class Mat2():

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __mul__(self, other):
        self.x1 *= other
        self.y1 *= other
        self.x2 *= other
        self.y2 *= other
        return self
