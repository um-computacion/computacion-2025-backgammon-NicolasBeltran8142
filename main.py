from core.board import Board
from core.player import Jugador

def iniciar_juego():
    jugador1 = Jugador("Jugador 1", "blanco")
    jugador2 = Jugador("Jugador 2", "negro")

    print("🎮 Jugadores:")
    print(jugador1)
    print(jugador2)

    tablero = Board()
    tablero.inicializar_fichas()
    tablero.mostrar_tablero()

    print(f"\nTurno de: {jugador1.nombre}")

def main():
    tablero = Board()
    tablero.mostrar_tablero()

    jugador_actual = "Jugador1"
    print("\nTurno de:", jugador_actual)

if __name__ == "__main__":
    main()
