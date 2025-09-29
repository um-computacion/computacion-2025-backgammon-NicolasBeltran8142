from core.game import Game

def main():
    juego = Game()
    print("🎮 Bienvenido a Backgammon CLI")

    while True:
        jugador = juego.jugador_actual()
        print(f"\n🎲 Turno de: {jugador.nombre} ({jugador.color})")

        input("Presioná Enter para tirar los dados...")
        dados = juego.tirar_dados()
        print(f"🧮 Dados: {dados}")
        print(f"Movimientos disponibles: {juego.available_moves}")

        continuar = input("¿Querés seguir al siguiente turno? (s/n): ")
        if continuar.lower() != "s":
            break

        juego.cambiar_turno()

if __name__ == "__main__":
    main()
