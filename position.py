"""
objectif : pouvoir gérer de façon simple et intuitive des positions en 3 (ou X) dimensions
possibilités : ajout de position : a = position(X, Y, Z) + (A, B, C) - (3, 1, 2)
a.get renvoie les nouvelles coordonnées
a.x, a.y, a.z renvoie les coordonnées individuelles
a.get = (2, 9, 1) fonctionnel

ajout de tuple dans un set : a = Positions() + (X, Y, Z) - (A, B, C)
a.get renvoie le nouveau set de coordonnées
a = {(3, 2, 0), (9, 6, 3)} à paramétrer ?
> pour l'instant ça passe par a = Positions((3, 2, 0), (9, 6, 3))

Position.is_temp must be deleted ??
"""

from copy import deepcopy

POSITION_TYPE = tuple

class Position:
    # ne prend que du tuple en entrée ou en sortie
    def __init__(self, position: tuple, is_temp=False):
        self.is_temp = is_temp
        self._get = position
        # if is_temp is True, this Position can be modified or deleted

    def __add__(self, value):
        return self.set(POSITION_TYPE([i + j for i, j in zip(self, value)]))
    __radd__ = __add__

    def __sub__(self, value): # position - (x, y) or position - position
        return self.set(POSITION_TYPE([i - j for i, j in zip(self, value)]))

    def __rsub__(self, value): # (x, y) - Position
        return self.set(POSITION_TYPE([j - i for i, j in zip(self, value)]))

    def __iter__(self):
        yield from (i for i in self._get)

    def set_temp(self, bool):
        self.is_temp = bool

    def temp_copy(self):
        if self.is_temp:
            return self
        self = deepcopy(self)
        self.is_temp = True
        return self

    def __getitem__(self, value):
        return self._get[value]

    # temporary Position
    # Position = -Position or Position.get = -Position
    def __neg__(self):
        self.set(POSITION_TYPE([-value for value in self]))
        return self

    @property
    def get(self):
        return self._get

    def set(self, value):
        if not self.is_temp:
            self = deepcopy(self)
            self.is_temp = True
        self._get = value
        return self

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    # item.position == item2.position or tuple == position or position == tuple
    def __eq__(self, value):
        return getattr(self, "get", self) == getattr(value, "get", value)

    def move(self, direction: tuple):
        # certitude que self est une position non temporaire et que celle-ci sera écrasée
        # si cette certitude n'est plus, conditionner les is_temp
        self.is_temp = True
        self + direction # because the new position is saved in self
        self.is_temp = False

    def teleport(self, new_position: tuple):
        # certitude que self est une position non temporaire et que celle-ci sera écrasée
        # si cette certitude n'est plus, conditionner les is_temp
        self.is_temp = True
        self.set(new_position)
        self.is_temp = False

def sub_pos_sq(self, target):
    yield from ((a - b)**2 for a, b in zip(self, target))

def dist(self, target):
    result = 0
    for point in sub_pos_sq(self, target):
        result += point
    return result**0.5

def in_range(self, target, dist):
    return dist(self, target) <= dist

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
