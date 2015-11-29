
import math


class Vector2(object):

    def normalized(self):
        return self * (1.0 / self.size)

    def rotated(self, angle):
        new_angle = angle + self.angle
        return self.size * Vector2(math.cos(new_angle),
                                   math.sin(new_angle))

    def dot(self, other):
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        else:
            raise TypeError("can only dot two vectors together")

    @property
    def size(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def size_squared(self):
        return self.x ** 2 + self.y ** 2

    @size.setter
    def size(self, value):
        new_v = self.normalized() * value
        self.x = new_v.x
        self.y = new_v.y

    @property
    def angle(self):
        return math.atan2(self.y, self.x)

    @angle.setter
    def angle(self, value):
        new_v = self.rotated(value - self.angle)
        self.x = new_v.x
        self.y = new_v.y

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __add__(self, other):
        if not isinstance(other, Vector2):
            raise TypeError("unsupported operand types for +: 'Vector2' and "
                            "'{0}'".format(other.__class__.__name__))
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if (isinstance(other, int) or isinstance(other, float)):
            return Vector2(self.x * other, self.y * other)
        else:
            raise TypeError("unsupported operand types for *: 'Vector2' and "
                            "'{0}'".format(other.__class__.__name__))

    def __rmul__(self, other):
        return self * other

    def __len__(self):
        return 2

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("index out of range")

    def __eq__(self, other):
        aeq = lambda x, y: abs(x - y) < 10 ** -5
        return aeq(self.x, other.x) and aeq(self.y, other.y)

    def __repr__(self):
        return 'Vector2(%.3f,%.3f)' % (self.x, self.y)

    def __str__(self):
        return '<%.3f,%.3f>' % (self.x, self.y)
