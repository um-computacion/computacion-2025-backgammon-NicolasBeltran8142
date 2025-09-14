import unittest
from core.board import Board
from core.checker import Checker

class TestBoardInitialization(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.inicializar_fichas()

    def test_total_fichas(self):
        total = sum(len(punto) for punto in self.board._puntos_)
        self.assertEqual(total, 30, "Debe haber 30 fichas en total (15 por jugador)")

    def test_posiciones_blancas(self):
        posiciones_blancas = {0: 2, 11: 5, 16: 3, 18: 5}
        for punto, cantidad in posiciones_blancas.items():
            fichas = self.board._puntos_[punto]
            self.assertEqual(len([f for f in fichas if f._color_ == "blanco"]), cantidad,
                             f"Debe haber {cantidad} fichas blancas en el punto {punto}")

    def test_posiciones_negras(self):
        posiciones_negras = {23: 2, 12: 5, 7: 3, 5: 5}
        for punto, cantidad in posiciones_negras.items():
            fichas = self.board._puntos_[punto]
            self.assertEqual(len([f for f in fichas if f._color_ == "negro"]), cantidad,
                             f"Debe haber {cantidad} fichas negras en el punto {punto}")
class TestMovimientoFichas(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.inicializar_fichas()

    def test_mover_ficha_valida(self):
        origen = 0
        destino = 1
        color = "blanco"
        self.board.mover_ficha(origen, destino, color)
        self.assertEqual(len(self.board._puntos_[origen]), 1)
        self.assertEqual(len(self.board._puntos_[destino]), 1)
        self.assertEqual(self.board._puntos_[destino][0]._color_, "blanco")

    def test_error_sin_fichas_en_origen(self):
        with self.assertRaises(ValueError):
            self.board.mover_ficha(2, 3, "blanco")  # punto 2 está vacío

    def test_error_color_incorrecto(self):
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "negro")  # hay fichas blancas en el punto 0

    def test_error_destino_ocupado_por_oponente(self):
        # colocamos una ficha negra en el destino
        self.board._puntos_[1].append(Checker("negro", 1))
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "blanco")  # blanco no puede ir a punto ocupado por negro
if __name__ == "__main__":
    unittest.main()
