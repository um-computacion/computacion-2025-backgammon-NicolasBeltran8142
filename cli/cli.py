from core.game import Game

def mostrar_tablero(juego):
    print("\n📦 Estado del tablero:")
    for i in range(24):
        fichas = juego.board._puntos_[i]
        contenido = "".join([f._color_[0].upper() for f in fichas])
        print(f"Punto {i:2}: {contenido or '-'}")
    print("-" * 30)

def mostrar_estado(juego):
    """
    Muestra el estado actual del juego en consola:
    - Turno actual
    - Fichas en barra
    - Fichas borneadas
    - Último tiro de dados
    - Movimientos disponibles
    """
    jugador = juego.jugador_actual()
    print(f"\n🔁 Turno de: {jugador.nombre} ({jugador.color})")
    print(f"📍 Fichas en barra: {len(juego.fichas_en_barra(jugador.color))}")
    print(f"🎯 Fichas borneadas: {len(juego.fichas_borneadas(jugador.color))}")
    print(f"🎲 Último tiro: {juego.last_roll}")
    print(f"📦 Movimientos disponibles: {juego.available_moves}")

def ejecutar_cli():
    juego = Game()
    print("🎮 Bienvenido a Backgammon CLI")

    while True:
        mostrar_tablero(juego)
        mostrar_estado(juego)

        input("Presiona Enter para tirar los dados...")
        juego.tirar_dados()
        mostrar_estado(juego)

        jugador = juego.jugador_actual()
        color = jugador.color
        origenes = juego.puntos_validos_de_origen(color)

        for move in juego.available_moves:
            print(f"\n➡ Movimiento de {move} espacios")
            print(f"Posibles orígenes: {origenes}")
            try:
                origen = int(input("Selecciona punto de origen: "))
                destino = origen + move
                exito = juego.mover_ficha(origen, destino, color)
                print("✅ Movimiento exitoso" if exito else "❌ Movimiento inválido")
            except ValueError:
                print("⚠ Entrada inválida")

        if juego.verificar_ganador():
            print(f"\n🏆 ¡{juego.verificar_ganador()} ha ganado el juego!")
            break

        if input("¿Pasar al siguiente turno? (s/n): ").lower() != "s":
            print("👋 Fin del juego. ¡Gracias por jugar!")
            break

        juego.cambiar_turno()
