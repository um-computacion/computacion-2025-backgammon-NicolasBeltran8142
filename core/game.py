from core.board import Board
from core.dados import Dice
from core.player import Jugador, TurnManager

class Game:
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Jugador("Jugador 1", "blanco")
        self.jugador2 = Jugador("Jugador 2", "negro")
        self.turnos = TurnManager(self.jugador1, self.jugador2)
        self.last_roll = []
        self.available_moves = []
        self.historial = []

        self.board.inicializar_fichas()
        self._asignar_fichas_a_jugadores()

    def _asignar_fichas_a_jugadores(self):
        posiciones = {
            "blanco": [0]*2 + [11]*5 + [16]*3 + [18]*5,
            "negro": [23]*2 + [12]*5 + [7]*3 + [5]*5
        }
        for color, puntos in posiciones.items():
            jugador = self.jugador1 if color == "blanco" else self.jugador2
            for i, punto in enumerate(puntos):
                jugador.fichas[i]._position_ = punto

    def tirar_dados(self):
        self.last_roll = self.dice.roll_dice()
        self.available_moves = self.dice.get_moves()
        return self.last_roll

    def jugador_actual(self):
        return self.turnos.jugador_actual()

    def cambiar_turno(self):
        self.turnos.siguiente_turno()

    def fichas_en_punto(self, punto, color):
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == punto]

    def fichas_en_barra(self, color):
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        jugador = self._jugador_por_color(color)
        return [f for f in jugador.fichas if f._position_ == "off"]

    def puntos_validos_de_origen(self, color):
        if self.fichas_en_barra(color):
            return ["bar"]
        return [p for p in range(24) if self.fichas_en_punto(p, color)]

    def puede_mover(self, origen, destino, color):
        if self.fichas_en_barra(color) and origen != "bar":
            return False
        if destino < 0 or destino > 23:
            return False
        distancia = self._calcular_distancia(origen, destino, color)
        if distancia not in self.available_moves:
            return False
        destino_fichas = self.board._puntos_[destino]
        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) > 1:
            return False
        return True

    def mover_ficha(self, origen, destino, color):
        if not self.puede_mover(origen, destino, color):
            return False

        ficha = self._obtener_ficha_a_mover(origen, color)
        if not ficha:
            return False

        destino_fichas = self.board._puntos_[destino]
        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) == 1:
            rival_color = "negro" if color == "blanco" else "blanco"
            rival = self.fichas_en_punto(destino, rival_color)[0]
            rival._position_ = "bar"
            self.board._puntos_[destino].pop()

        ficha._position_ = destino
        self.board.mover_ficha(origen, destino, color)

        distancia = self._calcular_distancia(origen, destino, color)
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
        if origen == "bar":
            fichas = self.fichas_en_barra(color)
        else:
            fichas = self.fichas_en_punto(origen, color)
        return fichas[0] if fichas else None

    def _jugador_por_color(self, color):
        return self.jugador1 if color == "blanco" else self.jugador2

    def _calcular_distancia(self, origen, destino, color):
        if origen == "bar":
            return destino if color == "blanco" else 23 - destino
        return abs(destino - origen)

    def verificar_ganador(self):
        if self.jugador1.ha_ganado():
            return self.jugador1.nombre
        elif self.jugador2.ha_ganado():
            return self.jugador2.nombre
        return None

    def mostrar_estado(self):
        jugador = self.jugador_actual()
        print(f"\nTurno de: {jugador.nombre} ({jugador.color})")
        print(f"Fichas en barra: {len(self.fichas_en_barra(jugador.color))}")
        print(f"Fichas borneadas: {len(self.fichas_borneadas(jugador.color))}")
        print(f"Último tiro: {self.last_roll}")
        print(f"Movimientos disponibles: {self.available_moves}")
