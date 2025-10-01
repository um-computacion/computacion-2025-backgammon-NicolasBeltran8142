from core.game import Game

def mostrar_tablero(juego):
    print("\nEstado del tablero:")
    for i in range(24):
        fichas = juego.board._puntos_[i]
        contenido = "".join([f._color_[0].upper() for f in fichas])
        print(f"Punto {i:2}: {contenido or '-'}")
    print("-" * 30)

def mostrar_estado(juego):
    jugador = juego.jugador_actual()
    print(f"\nTurno de: {jugador.nombre} ({jugador.color})")
    print(f"Fichas en barra: {len(juego.fichas_en_barra(jugador.color))}")
    print(f"Fichas borneadas: {len(juego.fichas_borneadas(jugador.color))}")
    print(f"Último tiro: {juego.last_roll}")
    print(f"Movimientos disponibles: {juego.available_moves}")

def fichas_movibles(juego, color):
    fichas = []
    for punto in juego.puntos_validos_de_origen(color):
        stack = juego.board._puntos_[punto]
        if stack and stack[-1]._color_ == color:
            ficha = stack[-1]
            posibles = []
            for m in juego.available_moves:
                destino = punto + m
                if juego.puede_mover(punto, destino, color):
                    posibles.append(destino)
            if posibles:
                fichas.append((ficha, posibles))
    return fichas

def ejecutar_cli():
    juego = Game()
    print("Bienvenido a Backgammon CLI")
    print("Usá los números de punto (0 a 23) para mover tus fichas.\n")

    while True:
        mostrar_tablero(juego)
        mostrar_estado(juego)

        input("Presiona Enter para tirar los dados...")
        juego.tirar_dados()
        mostrar_estado(juego)

        jugador = juego.jugador_actual()
        color = jugador.color

        fichas_disponibles = fichas_movibles(juego, color)

        if not fichas_disponibles:
            print("No hay movimientos posibles este turno.")
        else:
            print("\nFichas disponibles para mover (solo la ficha superior de cada punto):")
            for i, (ficha, destinos) in enumerate(fichas_disponibles):
                print(f"{i}: Ficha en punto {ficha._position_} → posibles destinos: {destinos}")

            try:
                eleccion = int(input("Seleccioná el número de ficha que querés mover: "))
                ficha, destinos = fichas_disponibles[eleccion]
                print(f"\nPosibles destinos para la ficha en {ficha._position_}:")
                for d in destinos:
                    print(f"- {d}")
                destino = int(input("Seleccioná destino: "))
                origen = ficha._position_
                if destino in destinos:
                    exito = juego.mover_ficha(origen, destino, color)
                    print("Movimiento exitoso" if exito else "Movimiento inválido")
                else:
                    print("Destino no permitido para esa ficha.")
            except (ValueError, IndexError):
                print("Entrada inválida. Intenta de nuevo.")

        if juego.verificar_ganador():
            print(f"\n{juego.verificar_ganador()} ha ganado el juego!")
            break

        continuar = input("\n¿Pasar al siguiente turno? (s/n): ")
        if continuar.lower() != "s":
            print("Fin del juego. Gracias por jugar.")
            break

        juego.cambiar_turno()
