# core/dados.py
class Dice:
    def __init__(self):
        self.__values__ = (0, 0)

    def roll_dice(self):
        import random
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.__values__ = (die1, die2)
        return self.__values__

    def get_values(self):
        return self.__values__

    def is_double(self):
        return self.__values__[0] == self.__values__[1]

    def set_values_for_test(self, val1, val2):
        self.__values__ = (val1, val2)
