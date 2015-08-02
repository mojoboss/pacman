__author__ = 'starlord'
import math

class Vector2D(object):
    def __init__(self, x=0.0, y=0.0):
        if isinstance(x, tuple) or isinstance(x, list):
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)

    def toTuple(self):
        '''Returns the vector as a tuple'''
        return (self.x, self.y)

    @staticmethod
    def deg_to_rad(degree):
        '''Convert degree to radians'''
        return degree * math.pi / 180.0

    @staticmethod
    def rad_to_deg(radian):
        '''Convert radians to degree'''
        return radian * 180.0 / math.pi

    @staticmethod
    def from_points(P1, P2):
        '''Create a Vector2D object from two points'''
        return Vector2D(P2[0] - P1[0], P2[1] - P1[1])

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        '''Turn vector into a unit vector'''
        magnitude = self.magnitude()
        try:
            xnorm = self.x / magnitude
        except ZeroDivisionError:
            xnorm = 0.0
        try:
            ynorm = self.y / magnitude
        except ZeroDivisionError:
            ynorm = 0.0

        return Vector2D(xnorm, ynorm)

    def xcomp(self):
        '''Return the x component of this vector'''
        return Vector2D(self.x, 0)

    def ycomp(self):
        '''Return the y component of this vector'''
        return Vector2D(0, self.y)

    def rhnorm(self):
        '''Returns a vector right-hand normal (cw) to self'''
        return Vector2D(self.y, -self.x)

    def lhnorm(self):
        '''Return a vector left-hand normal (ccw) to self'''
        return Vector2D(-self.y, self.x)

    def __add__(self, rhs):
        return Vector2D(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector2D(self.x - rhs.x, self.y - rhs.y)

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector2D(self.x /scalar, self.y / scalar)

    def __eq__(self, other):
        '''Return True if other has same elements as self'''
        if self.x == other.x and self.y == other.y:
            return True
        return False

    def get_distance_to(self, p):
        '''Return the distance to a point.  Input is type Vector2D'''
        dx = self.x - p.x
        dy = self.y - p.y
        return math.sqrt(dx*dx + dy*dy)

    def dotpro(self, rhs):
        '''Return the dot product of two vectors (a scalar)'''
        return self.x*rhs.x + self.y*rhs.y

    def projection(self, vec):
        '''Project input vector onto self'''
        dp = self.dotpro(vec)
        mag = self.magnitude()
        projx = (dp / mag**2) * self.x
        projy = (dp / mag**2) * self.y
        return Vector2D(projx, projy)

    def angle(self, vec):
        '''Get angle between self and input vector in radians'''
        anorm = self.normalize()
        bnorm = vec.normalize()
        dp = anorm.dotpro(bnorm)
        return math.acos(dp)

    def rotate(self, angle):
        '''Rotate self by given angle, magnitude stays the same
        if angle > 0 cw rotation, angle < 0 ccw rotation'''
        rad = self.deg_to_rad(angle)
        x = self.x * math.cos(rad) - self.y * math.sin(rad)
        y = self.x * math.sin(rad) + self.y * math.cos(rad)
        self.x = x
        self.y = y

    def crossproduct(self, vec):
        '''Get cross product between two 2D vectors, only care
        about sign'''
        return self.x*vec.y - self.y*vec.x

