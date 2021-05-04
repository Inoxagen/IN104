from math import sqrt


class VectorError(Exception):
    pass


class Vector:
    def __init__(self, dim):
        self.dim = dim
        self._values = [0 for i in range(dim)]

    def sqrnorm(self):
        sqr_values = [x*x for x in self._values]
        return sum(sqr_values)

    def norm(self):
        return sqrt(self.sqrnorm())

    def __str__(self):
        return "(%s)" % (", ".join([str(x) for x in self._values]))

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return self.dim

    def __getitem__(self, key):
        return self._values.__getitem__(key)

    def __setitem__(self, key, value):
        return self._values.__setitem__(key, value)

    # region Unary Operators

    # this is called to compute expressions of the form `-a`
    # where a is a Vector
    def __neg__(self):
        result = self.__class__(self.dim)
        for i in range(self.dim):
            result[i] = -self[i]
        return result

    # this is called to compute expressions of the form `abs(a)`
    # where a is a Vector
    def __abs__(self):
        return self.norm()

    # endregion

    # region Binary Operators

    # this is called to compute expressions of the form `a + b`
    # where a is a Vector

    # a = Vector(0, 0)
    # b = "salut"
    # a + b
    # ==> a.__add__(b)
    def __add__(self, other):
        if isinstance(other, Vector):
            if (self.dim != other.dim):
                raise VectorError("Cannot add vectors of dim %d and %d" % (
                    self.dim, other.dim))

            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] + other[i]
            return result
        else:
            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] + other
            return result

    def __radd__(self,other):
        return self + other

    # this is called to compute expressions of the form `a - b`
    # where a is a Vector
    def __sub__(self, other):
        if isinstance(other, Vector):
            if (self.dim != other.dim):
                raise VectorError("Cannot subtract vectors of dim %d and %d" % (
                    self.dim, other.dim))

            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] - other[i]
            return result
        else:
            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] - other
            return result







    # this is called to compute expressions of the form `a * b`
    # where a is a Vector
    def __mul__(self, other):
        if isinstance(other, Vector):
            if (self.dim != other.dim):
                raise VectorError("Cannot multiply vectors of dim %d and %d" % (
                    self.dim, other.dim))

            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] * other[i]
            return result
        else:
            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] * other
            return result

    # this is called to compute expressions of the form `a * b`
    # where b is a Vector
    def __rmul__(self, other): return self.__mul__(other)

    # this is called to compute expressions of the form `a / b`
    # where a is a Vector
    def __truediv__(self, other):
        if isinstance(other, Vector):
            return NotImplemented
        else:
            result = self.__class__(self.dim)
            for i in range(self.dim):
                result[i] = self[i] / other
            return result

    # endregion


class Vector2(Vector):
    def __init__(self, x=0, y=0):
        super().__init__(2)
        self[0] = x
        self[1] = y

    def get_x(self): return self[0]
    def get_y(self): return self[1]

    def set_x(self, value): self[0] = value
    def set_y(self, value): self[1] = value
