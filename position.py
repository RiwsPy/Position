"""
    Use to manage tuple of positions

    >>> from position import Position
    >>> a = Position((1, 2, 3))
    >>> b = (3, 4, 7)
    >>> a = a+b+a
    >>> a
    (5, 8, 13)

    >>> from position import Position
    >>> a = Position((1, 7, 3))
    >>> b = (3, 4)
    >>> a = a+b
    >>> a
    (4, 11, 3)
"""

from itertools import zip_longest

POSITION_TYPE = tuple

class Position(POSITION_TYPE):
    def __new__(cls, pos):
        return super().__new__(cls, pos)

    def __add__(self, value):
        """
            Return self+value

            *param value: iterable with integer
            *rtype: tuple
        """
        return self.__class__([i + j for i, j in zip_longest(self, value, fillvalue=0)])
    __radd__ = __add__

    def __sub__(self, value): # position - (x, y) or position - position
        """
            Return self - value

            *param value: iterable with integer
        """
        return self.__class__([i - j for i, j in zip_longest(self, value, fillvalue=0)])

    def __rsub__(self, value): # (x, y) - Position
        """
            Return value - self

            *param value: iterable with integer
        """
        return self.__class__([j - i for i, j in zip_longest(self, value, fillvalue=0)])

    def __neg__(self):
        """
            Return -Position

            *rtype: POSITION_TYPE
        """
        return self.__class__([-i for i in self])

    def move(self, direction):
        """
            self.position += direction

            *param direction: iterable
            *rtype: None
        """
        self += direction
        return self

    def iset(self, new_position):
        """
            Erase and return the object position by ``new_position``

            *type new_position: iterable
            *rtype: POSITION_TYPE
        """
        return self.__class__(new_position)

    def square_dist(self, target) ->  int:
        """
            Return the square distance between self and target

            *type target: tuple, list or position.Position
            *rtype: int
        """
        return sum([(a - b)*(a - b) for a, b in zip_longest(self, target, fillvalue=0)])

"""
# set(Position)
# + connecteur logique (or xor and)
class Positions:
    def __init__(self, *args):
        self.get = set()
        for arg in args:
            if type(arg) is tuple:
                self.get.add(arg)
            elif type(arg) is set:
                self.get = self.get.union(arg)

    def __add__(self, value: tuple):
        # ne modifie pas le set d'origine
        retour = type(self)(self.get)
        retour.get.add(value)
        return retour

    def __sub__(self, value: tuple):
        retour = type(self)(self.get)
        retour.get.discard(value)
        return retour

"""


if __name__ == "__main__":
    a = Position((1, 2, 3))
    print(a + (1, 2, 3))
    print(a.move((1, 2, 3)))
    import doctest
    doctest.testmod()

