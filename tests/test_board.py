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

if __name__ == "__main__":
    unittest.main()
