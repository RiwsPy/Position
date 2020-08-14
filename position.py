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

DIM_NAME = ['_x', '_y', '_z']
NB_DIMENSION = len(DIM_NAME)
POSITION_TYPE = tuple

class Position:
    # ne prend que du tuple en entrée ou en sortie
    def __init__(self, position: tuple, is_temp=False):
        self._is_temp = is_temp
        self.get = position
        # if is_temp is True, this Position can be modified or deleted

    def __add__(self, value):
        if self.is_temp:
            result = self
        elif type(value) is type(self) and value.is_temp:
            self, value = value, self # possible because a+b == b+a
            result = self
        else:
            result = self.temp_copy()
        # here, result is a temp Position with self.get position

        lst = []
        for index in range(NB_DIMENSION):
            lst.append(result[index]+value[index]) # value can be tuple or Position
        result.get = POSITION_TYPE(lst)
        return result

    def __sub__(self, value):
        if type(value) is POSITION_TYPE:
            value = type(self)(value, is_temp=True)

        return self + (-value)  # go __add__

    def temp_copy(self):
        return type(self)(self.get, is_temp=True)

    def __getitem__(self, value):
        return getattr(self, DIM_NAME[value], 0)

    # temporary Position
    # Position = -Position or Position.get = -Position
    def __neg__(self):
        if not self.is_temp:
            self = self.temp_copy()
        self.get = POSITION_TYPE([-i for i in self.get])
        # opti but not clear
        #self.get = POSITION_TYPE([-getattr(self, i, 0) for i in DIM_NAME])
        return self

    @property
    def is_temp(self):
        return self._is_temp

    @property
    # test : len(Position.get) == NB_DIMENSION
    def get(self):
        # too heavy ?
        return POSITION_TYPE([getattr(self, i) for i in DIM_NAME])

    @get.setter
    # objet.position.get = (0, 1, 0)
    def get(self, value) -> None:
        for index, name in enumerate(DIM_NAME):
            setattr(self, name, value[index])

    @property
    def x(self):
        return getattr(self, DIM_NAME[0], 0)

    @property
    def y(self):
        return getattr(self, DIM_NAME[1], 0)

    @property
    def z(self):
        return getattr(self, DIM_NAME[2], 0)

    # new possible case : item.position == item2.position
    # instead of : item.position.get == item2.position.get
    def __eq__(self, value):
        if type(self) is type(value): # comparaison between Position and Position
            return self.get == value.get
        elif type(value) is POSITION_TYPE: # comparaison between Position and tuple
            return self.get == value
        return False

    def move(self, direction: tuple):
        self.get += direction

    def teleport(self, new_position: tuple):
        self.get = new_position

    def range(self, target):
        if type(self) is type(target):
            result = 0
            new_position = self - target
            for name in DIM_NAME:
                result += getattr(new_position, name, 0)**2
            return result**0.5

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

# tests

a = Position((0, 0, 0))
b = a + (0, 1, 3) + (0, 3, 1) - (9, 3, 1)
print(b.get)