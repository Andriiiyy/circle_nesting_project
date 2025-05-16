import math

# === Клас кола ===
class Circle:
    def __init__(self, id, x, y, r):
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.area = math.pi * r ** 2
        self.children = []
        self.parent = None

    def distance_to(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def is_inside(self, other):
        return self.distance_to(other) + self.r < other.r
