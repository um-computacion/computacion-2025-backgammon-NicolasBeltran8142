from core.board import Board
from core.dados import Dice
from core.checker import Checker
from core.player import Jugador

class Backgammon:
    def __init__(self):
        self.board = Board()
        self.dice = Dice()
        self.player1 = Jugador("Jugador1", "blanco")
        self.player2 = Jugador("Jugador2", "negro")
        self.current_player = self.player1
        self.last_roll = None
        self.available_moves = []
        self.historial = []

        self.fichas = {
            "blanco": [Checker("blanco", None) for _ in range(15)],
            "negro": [Checker("negro", None) for _ in range(15)]
        }

    def iniciar_partida(self):
        self.board.inicializar_fichas()
        posiciones = {
            "blanco": [0]*2 + [11]*5 + [16]*3 + [18]*5,
            "negro": [23]*2 + [12]*5 + [7]*3 + [5]*5
        }
        for color in posiciones:
            for i, punto in enumerate(posiciones[color]):
                self.fichas[color][i]._position_ = punto

    def tirar_dados(self):
        self.last_roll = self.dice.roll()
        self.available_moves = self.dice.get_moves(self.last_roll)
        return self.last_roll

    def cambiar_turno(self):
        self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def fichas_en_punto(self, punto, color):
        return [f for f in self.fichas[color] if f._position_ == punto]

    def fichas_en_barra(self, color):
        return [f for f in self.fichas[color] if f._position_ == "bar"]

    def fichas_borneadas(self, color):
        return [f for f in self.fichas[color] if f._position_ == "off"]

    def mover_ficha(self, origen, destino, color):
        fichas = self.fichas_en_punto(origen, color)
        if not fichas:
            return False

        ficha = fichas[0]
        destino_fichas = self.board._puntos_[destino]

        if destino_fichas and destino_fichas[-1]._color_ != color and len(destino_fichas) == 1:
            rival_color = "negro" if color == "blanco" else "blanco"
            rival = self.fichas_en_punto(destino, rival_color)[0]
            rival._position_ = "bar"
            self.board._puntos_[destino].pop()

        ficha._position_ = destino
        self.board.mover_ficha(origen, destino, color)
        self.historial.append((color, origen, destino))
        return True
