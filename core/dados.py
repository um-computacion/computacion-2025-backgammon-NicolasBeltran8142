"""Módulo que contiene la clase Dice, que representa los dados del juego."""
import random


class Dice:
    """
    Clase que representa los dados del juego.

    Permite tirar los dados, obtener sus valores, detectar si se tiró doble,
    y calcular los movimientos disponibles según el resultado.
    """

    def __init__(self):
        """
        Inicializa los valores de los dados en (0, 0).
        """
        self.__values__ = (0, 0)

    def roll_dice(self):
        """
        Genera dos valores aleatorios entre 1 y 6 simulando el tiro de dados.

        Returns:
            tuple: Una tupla con los dos valores obtenidos.
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.__values__ = (die1, die2)
        return self.__values__

    def get_values(self):
        """
        Devuelve los valores actuales de los dados.

        Returns:
            tuple: Los valores del último tiro.
        """
        return self.__values__

    def is_double(self):
        """
        Verifica si los dados tienen el mismo valor (doble).

        Returns:
            bool: True si es doble, False si no.
        """
        return self.__values__[0] == self.__values__[1]

    def get_moves(self):
        """
        Calcula los movimientos disponibles según los valores de los dados.

        Returns:
            list: Lista de movimientos disponibles.
        """
        d1, d2 = self.__values__
        return [d1] * 4 if self.is_double() else [d1, d2]

    def set_values_for_test(self, val1, val2):
        """
        Establece manualmente los valores de los dados (para pruebas).

        Args:
            val1 (int): Valor del primer dado.
            val2 (int): Valor del segundo dado.
        """
        if not (1 <= val1 <= 6 and 1 <= val2 <= 6):
            raise ValueError("Los valores deben estar entre 1 y 6")
        self.__values__ = (val1, val2)
