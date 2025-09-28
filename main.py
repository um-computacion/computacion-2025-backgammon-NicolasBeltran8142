from core.board import Board
from core.player import Jugador

class TurnManager:
    def __init__(self, jugador1, jugador2):
        self.jugadores = [jugador1, jugador2]
        self.indice_actual = 0

    def jugador_actual(self):
        return self.jugadores[self.indice_actual]

    def siguiente_turno(self):
        self.indice_actual = (self.indice_actual + 1) % 2

    def mostrar_turno(self):
        jugador = self.jugador_actual()
        print(f"\n🎲 Turno de: {jugador.nombre} ({jugador.color})")

def iniciar_juego():
    jugador1 = Jugador("Jugador 1", "blanco")
    jugador2 = Jugador("Jugador 2", "negro")
    tablero = Board()
    tablero.inicializar_fichas()
    turnos = TurnManager(jugador1, jugador2)

    print("🎮 Jugadores:")
    print(jugador1)
    print(jugador2)

    while True:
        tablero.mostrar_tablero()
        turnos.mostrar_turno()
        jugador = turnos.jugador_actual()

        puede_reingresar = tablero.intentar_reingreso(jugador.color)

        if not puede_reingresar:
            print("⏭️ Turno perdido: no puede reingresar ninguna ficha")
            turnos.siguiente_turno()
            continue

        print("🟢 Listo para mover ficha (simulado)")

        turnos.siguiente_turno()

def main():
    iniciar_juego()

if __name__ == "__main__":
    main()
