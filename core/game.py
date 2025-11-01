from core.board import Board
from core.dados import Dice
from core.player import Jugador, TurnManager

class Game:
    """
    Coordina la lógica general del juego de Backgammon, incluyendo el estado del tablero,
    tiradas de dados, turnos de jugadores, validación de movimientos y condición de victoria.

    Atributos:
        board (Board): El tablero de juego.
        dice (Dice): El gestor de dados.
        jugador1 (Jugador): Jugador 1 (blanco).
        jugador2 (Jugador): Jugador 2 (negro).
        turnos (TurnManager): Administra la rotación de turnos.
        last_roll (list): Última tirada de dados.
        available_moves (list): Movimientos disponibles según los dados.
        historial (list): Historial de movimientos realizados.
    """

    def __init__(self):
        """
        Inicializa el juego con tablero, jugadores, dados y gestor de turnos.
        """
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Jugador("Jugador 1", "blanco")
        self.jugador2 = Jugador("Jugador 2", "negro")
        self.turnos = TurnManager(self.jugador1, self.jugador2)
        self.last_roll = []
        self.available_moves = []
        self.historial = []

        self._asignar_fichas_a_jugadores()

    def _asignar_fichas_a_jugadores(self):
        """
        Asigna las posiciones iniciales de las fichas según la configuración estándar.
        """
        posiciones = {
            "blanco": [0]*2 + [11]*5 + [16]*3 + [18]*5,
            "negro": [23]*2 + [12]*5 + [7]*3 + [5]*5
        }
        for point in self.board._puntos_:
            point.clear()

        for color, puntos in posiciones.items():
            jugador = self.jugador1 if color == "blanco" else self.jugador2
            for ficha in jugador.fichas:
                ficha._position_ = None

            for i, punto in enumerate(puntos):
                jugador.fichas[i]._position_ = punto
                self.board._puntos_[punto].append(jugador.fichas[i])

    def tirar_dados(self):
        """
        Lanza los dados y actualiza los movimientos disponibles.

        Retorna:
            list: Valores obtenidos en la tirada.
        """
        self.last_roll = self.dice.roll_dice()
        self.available_moves = self.dice.get_moves()
        return self.last_roll

    def jugador_actual(self):
        """
        Retorna el jugador que tiene el turno actual.

        Retorna:
            Jugador: El jugador activo.
        """
        return self.turnos.jugador_actual()

    def cambiar_turno(self):
        """
        Cambia al turno del siguiente jugador.
        """
        self.turnos.siguiente_turno()

    def fichas_en_punto(self, punto, color):
        """
        Retorna las fichas de un color en un punto específico del tablero.

        Args:
            punto (int): Índice del punto en el tablero.
            color (str): Color del jugador.

        Retorna:
            list: Fichas en ese punto.
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        """
        Retorna las fichas de un color que están en la barra.

        Args:
            color (str): Color del jugador.

        Retorna:
            list: Fichas en la barra.
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        """
        Retorna las fichas de un color que ya fueron retiradas del tablero.

        Args:
            color (str): Color del jugador.

        Retorna:
            list: Fichas con posición "off".
        """
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "off"]

    def puntos_validos_de_origen(self, color):
        """
        Retorna los puntos válidos desde donde el jugador puede mover fichas.

        Args:
            color (str): Color del jugador.

        Retorna:
            list: Puntos válidos o ["bar"] si hay fichas en la barra.
        """
        if self.fichas_en_barra(color):
            return ["bar"]
        return [p for p in range(24) if self.fichas_en_punto(p, color)]

    def puede_mover(self, origen, destino, color):
        """
        Verifica si un movimiento es válido según las reglas del juego.

        Args:
            origen (int o str): Punto de origen o "bar".
            destino (int o str): Punto de destino o "off".
            color (str): Color del jugador.

        Retorna:
            bool: True si el movimiento es válido, False si no lo es.
        """
        if self.fichas_en_barra(color) and origen != "bar":
            return False

        jugador = self._jugador_por_color(color)
        if destino == "off":
            if not jugador.puede_sacar_fichas(self.board):
                return False
            distancia = (24 - origen) if color == "blanco" else (origen + 1)
            return distancia in self.available_moves

        if not (0 <= destino <= 23):
            return False

        distancia = self._calcular_distancia(origen, destino, color)
        if distancia not in self.available_moves:
            return False

        destino_fichas = self.board._puntos_[destino]
        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) > 1:
            return False

        return True

    def mover_ficha(self, origen, destino, color):
        """
        Ejecuta un movimiento válido, incluyendo captura y registro en el historial.

        Args:
            origen (int o str): Punto de origen o "bar".
            destino (int o str): Punto de destino o "off".
            color (str): Color del jugador.

        Retorna:
            bool: True si el movimiento fue exitoso, False si no lo fue.
        """
        if not self.puede_mover(origen, destino, color):
            return False

        ficha = self._obtener_ficha_a_mover(origen, color)
        if not ficha:
            return False

        distancia = self._calcular_distancia(origen, destino, color)

        # Movimiento hacia fuera del tablero
        if destino == "off":
            ficha._position_ = "off"
            if origen != "bar" and self.board._puntos_[origen]:
                self.board._puntos_[origen].pop()

        else:
            destino_fichas = self.board._puntos_[destino]

            # Captura si hay una sola ficha rival
            if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) == 1:
                rival = destino_fichas[-1]
                rival._position_ = "bar"
                self.board._puntos_[destino].pop()

            ficha._position_ = destino

            if origen != "bar" and self.board._puntos_[origen]:
                self.board._puntos_[origen].pop()

            self.board._puntos_[destino].append(ficha)

        if distancia in self.available_moves:
            self.available_moves.remove(distancia)

        self.historial.append({
            "jugador": color,
            "origen": origen,
            "destino": destino,
            "dados": self.last_roll
        })

        return True

    def _obtener_ficha_a_mover(self, origen, color):
        """
        Obtiene la ficha que se va a mover desde el origen.

        Args:
            origen (int o str): Punto de origen o "bar".
            color (str): Color del jugador.

        Retorna:
            Ficha o None: La ficha a mover, si existe.
        """
        fichas = self.fichas_en_barra(color) if origen == "bar" else self.fichas_en_punto(origen, color)
        return fichas[0] if fichas else None

    def _jugador_por_color(self, color):
        """
        Retorna el objeto jugador según el color.

        Args:
            color (str): "blanco" o "negro".

        Retorna:
            Jugador: El jugador correspondiente.
        """
        return self.jugador1 if color == "blanco" else self.jugador2

    def _calcular_distancia(self, origen, destino, color):
        """
        Calcula la distancia del movimiento según origen, destino y color.

        Args:
            origen (int o str): Punto de origen o "bar".
            destino (int o str): Punto de destino o "off".
            color (str): Color del jugador.

        Retorna:
            int: Distancia del movimiento.
        """
        if origen == "bar":
            return (24 - destino) if color == "blanco" else (destino + 1)
        if destino == "off":
            return (24 - origen) if color == "blanco" else (origen + 1)
        return abs(destino - origen)

    def verificar_ganador(self):
        """
        Verifica si algún jugador ha ganado la partida.

        Retorna:
            str o None: Nombre del jugador ganador, o None si aún no hay ganador.
        """
        if len(self.fichas_borneadas("blanco")) == 15:
            return self.jugador1.nombre
        if len(self.fichas_borneadas("negro")) == 15:
            return self.jugador2.nombre
        return None

    def mostrar_estado(self):
        """
        Muestra el estado actual del juego en la consola.
        """
        jugador = self.jugador_actual()
        print(f"\nTurno: {jugador.nombre} ({jugador.color})")
        print(f"Fichas en la barra: {len(self.fichas_en_barra(jugador.color))}")
        print(f"Fichas retiradas: {len(self.fichas_borneadas(jugador.color))}")
        print(f"Última tirada: {self.last_roll}")
        print(f"Movimientos disponibles: {self.available_moves}")
