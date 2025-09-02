import random

class Dice:
    """Clase que representa los dados del Backgammon."""

    def __init__(self):
        self.__values__ = (0, 0)

    def roll_dice(self):
        """Lanza dos dados y guarda los resultados.
        
        Returns:
            tuple: Dos enteros entre 1 y 6 representando los valores de los dados.
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.__values__ = (die1, die2)
        return self.__values__

    def get_values(self):
        """Devuelve el último resultado de los dados."""
        return self.__values__

    def is_double(self):
        """Verifica si la tirada es un doble (ambos dados iguales)."""
        return self.__values__[0] == self.__values__[1]
    