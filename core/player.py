from core.checker import Checker

class Jugador:
    """
    Representa a un jugador del Backgammon.
    Maneja nombre, color, fichas, puntos y estado de victoria.
    """

    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.puntos = 0
        self.fichas_fuera = 0
        self.fichas = [Checker(color, None) for _ in range(15)]

    def __str__(self):
        return f"{self.nombre} juega con fichas {self.color}"

    def sumar_puntos(self, cantidad, verbose=True):
        self.puntos += cantidad
        if verbose:
            print(f"{self.nombre} suma {cantidad} puntos. Total: {self.puntos}")

    def sacar_ficha(self, verbose=True):
        self.fichas_fuera += 1
        if verbose:
            print(f"{self.nombre} ha sacado una ficha. Total fuera: {self.fichas_fuera}")

    def ha_ganado(self):
        return all(f._position_ == "off" for f in self.fichas)

    def fichas_en_estado(self, estado):
        return [f for f in self.fichas if f._position_ == estado]

    def fichas_en_punto(self, punto):
        return [f for f in self.fichas if f._position_ == punto]


class TurnManager:
    """
    Administra el turno entre dos jugadores.
    """

    def __init__(self, jugador1, jugador2):
        self.jugadores = [jugador1, jugador2]
        self.indice_actual = 0

    def jugador_actual(self):
        return self.jugadores[self.indice_actual]

    def siguiente_turno(self):
        self.indice_actual = (self.indice_actual + 1) % len(self.jugadores)

    def mostrar_turno(self, verbose=True):
        if verbose:
            jugador = self.jugador_actual()
            print(f"\nTurno de: {jugador.nombre} ({jugador.color})")
