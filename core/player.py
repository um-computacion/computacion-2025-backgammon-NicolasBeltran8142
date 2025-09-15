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