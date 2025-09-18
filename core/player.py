class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.puntos = 0
        self.fichas_fuera = 0

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
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.current_index = 0

    def current_player(self):
        return self.players[self.current_index]

    def next_turn(self):
        self.current_index = (self.current_index + 1) % 2

    def show_turn(self):
        print(f"\n🎲 Turn: {self.current_player().name} ({self.current_player().color})")
