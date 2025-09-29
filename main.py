from core.game import Game

def mostrar_tablero(game):
    print("\n🧩 TABLERO BACKGAMMON")
    print("ZONA SUPERIOR (24 → 13):")
    for i in range(23, 11, -1):
        punto = game.board._puntos_[i]
        contenido = "".join([f._color_[0].upper() for f in punto])
        print(f"{i:2}: {contenido:10}", end=" | ")
    print("\n" + "-"*80)
    print("ZONA INFERIOR (12 → 1):")
    for i in range(0, 12):
        punto = game.board._puntos_[i]
        contenido = "".join([f._color_[0].upper() for f in punto])
        print(f"{i:2}: {contenido:10}", end=" | ")
    print("\n")

def mostrar_estado(game):
    jugador = game.jugador_actual()
    print(f"🎲 Turno de: {jugador.nombre} ({jugador.color})")
    print(f"Último tiro: {game.last_roll}")
    print(f"Movimientos disponibles: {game.available_moves}")
    print(f"Fichas en barra: {len(game.fichas_en_barra(jugador.color))}")
    print(f"Fichas borneadas: {len(game.fichas_borneadas(jugador.color))}")
    print("-"*40)

def main():
    juego = Game()
    print("🎮 Bienvenido a Backgammon CLI")
    juego.tirar_dados()

    while True:
        mostrar_tablero(juego)
        mostrar_estado(juego)

        try:
            origen = int(input("Desde qué punto querés mover? (0–23): "))
            destino = int(input("A qué punto querés mover? (0–23): "))
        except ValueError:
            print("❌ Entrada inválida. Usá números entre 0 y 23.")
            continue

        color = juego.jugador_actual().color

        if juego.mover_ficha(origen, destino, color):
            print("✅ Movimiento realizado.")
        else:
            print("❌ Movimiento inválido.")

        ganador = juego.verificar_ganador()
        if ganador:
            print(f"🏆 ¡{ganador} ha ganado el juego!")
            break

        juego.cambiar_turno()

if __name__ == "__main__":
    main()