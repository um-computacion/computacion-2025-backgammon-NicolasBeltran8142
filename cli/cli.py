from core.game import Game


class TableroView:
    """Una vista que muestra el estado del tablero de Backgammon."""

    def mostrar(self, juego):
        """Muestra el tablero, incluyendo las fichas en cada punto y la barra.

        Args:
            juego (Game): El estado actual del juego.
        """
        board = juego.board
        puntos = board._puntos_

        def get_checker_char(color):
            """Devuelve el carácter que representa una ficha de un color."""
            return color[0].upper() if color else " "

        print("\nEstado del tablero:")
        print(" 13  14  15  16  17  18   BAR   19  20  21  22  23  24")
        print("+---+---+---+---+---+---+------+---+---+---+---+---+---+")

        fichas_blancas = juego.fichas_en_barra("blanco")
        fichas_negras = juego.fichas_en_barra("negro")
        barra = fichas_blancas + fichas_negras

        for i in range(5):
            fila_izq = []
            for p in range(12, 18):
                stack = puntos[p]
                char = " "
                if len(stack) > i:
                    char = (
                        str(len(stack))
                        if len(stack) > 5 and i == 4
                        else get_checker_char(stack[-1]._color_)
                    )
                fila_izq.append(f" {char} ")

            barra_char = " "
            if len(barra) > i:
                barra_char = get_checker_char(barra[i]._color_)

            fila_der = []
            for p in range(18, 24):
                stack = puntos[p]
                char = " "
                if len(stack) > i:
                    char = (
                        str(len(stack))
                        if len(stack) > 5 and i == 4
                        else get_checker_char(stack[-1]._color_)
                    )
                fila_der.append(f" {char} ")

            print(f"|{'|'.join(fila_izq)}|  {barra_char}  |{'|'.join(fila_der)}|")

        print("+---+---+---+---+---+---+------+---+---+---+---+---+---+")
        print(" 12  11  10   9   8   7   BAR    6   5   4   3   2   1")

        for i in range(4, -1, -1):
            fila_izq = []
            for p in range(11, 5, -1):
                stack = puntos[p]
                char = " "
                if len(stack) > i:
                    char = (
                        str(len(stack))
                        if len(stack) > 5 and i == 4
                        else get_checker_char(stack[-1]._color_)
                    )
                fila_izq.append(f" {char} ")

            barra_char = " "
            if len(barra) > i + 5:
                barra_char = get_checker_char(barra[i + 5]._color_)

            fila_der = []
            for p in range(5, -1, -1):
                stack = puntos[p]
                char = " "
                if len(stack) > i:
                    char = (
                        str(len(stack))
                        if len(stack) > 5 and i == 4
                        else get_checker_char(stack[-1]._color_)
                    )
                fila_der.append(f" {char} ")

            print(f"|{'|'.join(fila_izq)}|  {barra_char}  |{'|'.join(fila_der)}|")

        print("+---+---+---+---+---+---+------+---+---+---+---+---+---+")
        home_blanco = len(juego.fichas_borneadas("blanco"))
        home_negro = len(juego.fichas_borneadas("negro"))
        print(
            f"\nFichas borneadas: Blanco={home_blanco} {'W'*home_blanco} | Negro={home_negro} {'B'*home_negro}"
        )


class EstadoView:
    """Muestra el estado actual del juego, incluyendo el turno y los dados."""

    def mostrar(self, juego):
        """Muestra el jugador actual, las fichas en la barra, los dados y los movimientos.

        Args:
            juego (Game): El estado actual del juego.
        """
        jugador = juego.jugador_actual()
        print(f"\nTurno de: {jugador.nombre} ({jugador.color})")
        print(f"Fichas en barra: {len(juego.fichas_en_barra(jugador.color))}")
        print(f"Fichas borneadas: {len(juego.fichas_borneadas(jugador.color))}")
        print(f"Último tiro: {juego.last_roll}")
        print(f"Movimientos disponibles: {juego.available_moves}")


def fichas_movibles(juego, color):
    """Obtiene una lista de fichas que el jugador puede mover.

    Args:
        juego (Game): El estado actual del juego.
        color (str): El color del jugador ('blanco' o 'negro').

    Returns:
        list: Una lista de tuplas, donde cada tupla contiene una ficha y una lista de
              posibles destinos.
    """
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
    """Ejecuta el juego de Backgammon en la interfaz de línea de comandos."""
    juego = Game()
    tablero = TableroView()
    estado = EstadoView()

    print("Bienvenido a Backgammon CLI")
    print("Usá los números de punto (0 a 23) para mover tus fichas.\n")

    while True:
        tablero.mostrar(juego)
        estado.mostrar(juego)

        input("Presioná Enter para tirar los dados...")
        juego.tirar_dados()

        while juego.available_moves:
            tablero.mostrar(juego)
            estado.mostrar(juego)

            jugador = juego.jugador_actual()
            color = jugador.color
            fichas_disponibles = fichas_movibles(juego, color)

            if not fichas_disponibles:
                print("No hay movimientos posibles con los dados restantes.")
                break

            print(
                "\nFichas disponibles para mover (solo la ficha superior de cada punto):"
            )
            for i, (ficha, destinos) in enumerate(fichas_disponibles):
                print(
                    f"{i}: Ficha en punto {ficha._position_} → posibles destinos: {sorted(set(destinos))}"
                )

            try:
                eleccion = int(
                    input("Seleccioná el número de ficha que querés mover: ")
                )
                ficha, destinos = fichas_disponibles[eleccion]
                print(f"\nPosibles destinos para la ficha en {ficha._position_}:")
                for d in sorted(set(destinos)):
                    print(f"- {d}")
                destino = int(input("Seleccioná destino: "))
                origen = ficha._position_
                if destino in destinos:
                    exito = juego.mover_ficha(origen, destino, color)
                    if exito:
                        print("Movimiento exitoso.")
                    else:
                        print("Movimiento inválido.")
                else:
                    print("Destino no permitido para esa ficha.")
            except (ValueError, IndexError):
                print("Entrada inválida. Intenta de nuevo.")

        ganador = juego.verificar_ganador()
        if ganador:
            print(f"\n{ganador} ha ganado el juego!")
            break

        continuar = input(
            "\n¿Pasar al siguiente turno? (¡¡Darle a no cerrará el juego!!) (s/n): "
        )
        if continuar.lower() != "s":
            print("Fin del juego. Gracias por jugar.")
            break
