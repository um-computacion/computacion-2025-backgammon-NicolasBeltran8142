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
    turnos = TurnManager(jugador1, jugador2)

    tablero.inicializar_fichas()

    print("🎮 Jugadores:")
    print(f"{jugador1.nombre} ({jugador1.color})")
    print(f"{jugador2.nombre} ({jugador2.color})")

    while True:
        tablero.mostrar_tablero()
        turnos.mostrar_turno()
        jugador = turnos.jugador_actual()

        tiene_en_barra = any(f._position_ == "bar" for f in jugador.fichas)
        if tiene_en_barra:
            puede_reingresar = tablero.intentar_reingreso(jugador.color)
            if not puede_reingresar:
                print("⏭️ Turno perdido: no puede reingresar ninguna ficha")
                turnos.siguiente_turno()
                continue
            else:
                print("🔁 Reingresó una ficha desde la barra")
        else:
            print("🟢 Listo para mover ficha (simulado)")
            # Acá podrías pedir origen/destino y usar tablero.mover_ficha()

        turnos.siguiente_turno()

def main():
    try:
        iniciar_juego()
    except KeyboardInterrupt:
        print("\n👋 Juego terminado por el usuario.")

if __name__ == "__main__":
    main()
