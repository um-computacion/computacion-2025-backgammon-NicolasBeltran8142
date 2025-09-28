from core.checker import Checker

class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.puntos = 0
        self.fichas_fuera = 0
        self.fichas = [Checker(color, None) for _ in range(15)]

    def __str__(self):
        return f"{self.nombre} juega con fichas {self.color}"

    def sumar_puntos(self, cantidad):
        self.puntos += cantidad
        print(f"{self.nombre} suma {cantidad} puntos. Total: {self.puntos}")

    def sacar_ficha(self):
        self.fichas_fuera += 1
        print(f"{self.nombre} ha sacado una ficha. Total fuera: {self.fichas_fuera}")

    def ha_ganado(self):
        return self.fichas_fuera >= 15


class TurnManager:
    def __init__(self, jugador1, jugador2):
        self.jugadores = [jugador1, jugador2]
        self.indice_actual = 0

    def jugador_actual(self):
        return self.jugadores[self.indice_actual]

    def siguiente_turno(self):  # ← Este es el método correcto
        self.indice_actual = (self.indice_actual + 1) % 2

    def mostrar_turno(self):
        jugador = self.jugador_actual()
        print(f"\n🎲 Turno de: {jugador.nombre} ({jugador.color})")