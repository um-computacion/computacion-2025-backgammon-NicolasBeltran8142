class Casilla:
    def __init__(self, jugador=None, cantidad=0):
        self.jugador = jugador 
        self.cantidad = cantidad  

class Board:
    def __init__(self):
        self.casillas = [Casilla() for _ in range(24)]
        self.bar = {"Jugador1": [], "Jugador2": []}
        self.salidas = {"Jugador1": [], "Jugador2": []}

        self.inicializar_tablero()

    def inicializar_tablero(self):
        self.casillas[0] = Casilla("Jugador1", 2)
        self.casillas[11] = Casilla("Jugador1", 5)
        self.casillas[16] = Casilla("Jugador1", 3)
        self.casillas[18] = Casilla("Jugador1", 5)

        self.casillas[23] = Casilla("Jugador2", 2)
        self.casillas[12] = Casilla("Jugador2", 5)
        self.casillas[7] = Casilla("Jugador2", 3)
        self.casillas[5] = Casilla("Jugador2", 5)

    def mostrar_tablero(self):
        for i, casilla in enumerate(self.casillas):
            dueño = casilla.jugador if casilla.jugador else "-"
            print(f"{i:02d}: {dueño} ({casilla.cantidad})")
