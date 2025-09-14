from core.board import Board

def main():
    print("Bienvenido a Backgammon Computacion 2025\n")

    tablero = Board()
    tablero.mostrar_tablero()

    jugador_actual = "Jugador1"
    print("\nTurno de:", jugador_actual)

if __name__ == "__main__":
    main()
