from random import randint

class Star:
    def __init__(self, pos):
        self.pos = pos
        self.size = randint(1, 3)