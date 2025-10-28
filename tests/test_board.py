import unittest
from core.board import Board
from core.checker import Checker


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.board.inicializar_fichas()

    def test_inicializacion_correcta(self):
        self.assertEqual(len(self.board._puntos_[0]), 2)
        self.assertTrue(all(f._color_ == "blanco" for f in self.board._puntos_[0]))
        self.assertEqual(len(self.board._puntos_[23]), 2)
        self.assertTrue(all(f._color_ == "negro" for f in self.board._puntos_[23]))

    def test_mover_ficha_valida(self):
        self.board._puntos_[12] = []
        self.board.mover_ficha(11, 12, "blanco")
        self.assertEqual(len(self.board._puntos_[11]), 4)
        self.assertEqual(len(self.board._puntos_[12]), 1)
        self.assertEqual(self.board._puntos_[12][0]._position_, 12)

    def test_mover_ficha_con_captura(self):
        self.board._puntos_[12] = [Checker("negro", 12)]
        self.board._puntos_[11] = [Checker("blanco", 11)]
        self.board.mover_ficha(11, 12, "blanco")
        self.assertEqual(len(self.board._puntos_[12]), 1)
        self.assertEqual(self.board._puntos_[12][0]._color_, "blanco")

    def test_mover_ficha_color_incorrecto(self):
        self.board._puntos_[12] = [Checker("negro", 12)]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(12, 13, "blanco")

    def test_mover_ficha_origen_vacio(self):
        self.board._puntos_[10] = []
        with self.assertRaises(ValueError):
            self.board.mover_ficha(10, 11, "blanco")

    def test_mover_ficha_fuera_de_rango(self):
        self.board._puntos_[0] = [Checker("blanco", 0)]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(-1, 5, "blanco")
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 24, "blanco")

    def test_eliminar_ficha_si_unica(self):
        self.board._puntos_[5] = [Checker("negro", 5)]
        ficha = self.board.eliminar_ficha_si_unica(5, "negro")
        self.assertEqual(ficha._color_, "negro")
        self.assertEqual(self.board._puntos_[5], [])

    def test_eliminar_ficha_falla_si_multiple(self):
        self.board._puntos_[5] = [Checker("negro", 5), Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "negro")

    def test_eliminar_ficha_color_incorrecto(self):
        self.board._puntos_[5] = [Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "blanco")

    def test_eliminar_ficha_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(24, "blanco")

    def test_puede_entrar_desde_bar(self):
        self.board._puntos_[3] = []
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 3))
        self.board._puntos_[4] = [Checker("blanco", 4)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 4))
        self.board._puntos_[5] = [Checker("negro", 5)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 5))
        self.board._puntos_[6] = [Checker("negro", 6), Checker("negro", 6)]
        self.assertFalse(self.board.puede_entrar_desde_bar("blanco", 6))

    def test_reingreso_exitoso(self):
        entrada = self.board.intentar_reingreso("blanco")
        self.assertIn(entrada, range(0, 6))
        self.assertTrue(
            any(f._color_ == "blanco" for f in self.board._puntos_[entrada])
        )

    def test_reingreso_fallido(self):
        b = Board()
        for i in range(6):
            b._puntos_[i] = [Checker("negro", i), Checker("negro", i)]
        entrada = b.intentar_reingreso("blanco")
        self.assertIsNone(entrada)

    def test_registro_de_jugada(self):
        self.board.registrar_jugada("blanco", 0, 5, captura=True)
        self.assertEqual(len(self.board.historial_de_jugadas), 1)
        jugada = self.board.historial_de_jugadas[0]
        self.assertEqual(jugada["jugador"], "blanco")
        self.assertEqual(jugada["origen"], 0)
        self.assertEqual(jugada["destino"], 5)
        self.assertTrue(jugada["captura"])
