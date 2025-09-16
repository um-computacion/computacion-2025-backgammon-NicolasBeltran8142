import unittest
from core.board import Board, historial_de_jugadas, registrar_jugada
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
class TestRegistro(unittest.TestCase):
    def test_registrar_jugada(self):
        historial_de_jugadas.clear()
        registrar_jugada("Jugador1", 5, 10)
        self.assertEqual(len(historial_de_jugadas), 1)
        self.assertEqual(historial_de_jugadas[0]["origen"], 5)
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
            self.board.mover_ficha(2, 3, "blanco")  

    def test_error_color_incorrecto(self):
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "negro")  

    def test_error_destino_ocupado_por_oponente(self):
        self.board._puntos_[1].append(Checker("negro", 1))
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 1, "blanco")  
            
    def test_remove_single_checker_success(self):
        self.board._puntos_[8] = [Checker("blanco", 8)]
        removed = self.board.eliminar_ficha_si_unica(8, "blanco")
        self.assertEqual(removed._color_, "blanco")
        self.assertEqual(self.board._puntos_[8], [])

    def test_remove_fails_if_multiple_checkers(self):
        self.board._puntos_[5] = [Checker("negro", 5), Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "negro")

    def test_remove_fails_if_wrong_color(self):
        self.board._puntos_[7] = [Checker("blanco", 7)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(7, "negro")

    def test_remove_fails_if_empty(self):
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(3, "blanco")

    def test_remove_fails_if_invalid_index(self):
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(24, "blanco")
class TestReingresoDesdeBar(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_puede_entrar_en_punto_vacio(self):
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_puede_entrar_en_punto_con_una_ficha_rival(self):
        self.board._puntos_[0] = [Checker("negro", 0)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_no_puede_entrar_en_punto_bloqueado_por_rival(self):
        self.board._puntos_[0] = [Checker("negro", 0), Checker("negro", 0)]
        self.assertFalse(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_puede_entrar_en_punto_con_fichas_propias(self):
        self.board._puntos_[0] = [Checker("blanco", 0), Checker("blanco", 0)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_intentar_reingreso_exitoso(self):
        # Todos los puntos de entrada están vacíos
        resultado = self.board.intentar_reingreso("blanco")
        self.assertTrue(resultado)
        # Verificamos que haya una ficha blanca en algún punto de entrada
        self.assertTrue(any(
            self.board._puntos_[i] and self.board._puntos_[i][-1]._color_ == "blanco"
            for i in range(0, 6)
        ))

    def test_intentar_reingreso_fallido(self):
        # Bloquear todos los puntos de entrada para blanco
        for i in range(0, 6):
            self.board._puntos_[i] = [Checker("negro", i), Checker("negro", i)]
        resultado = self.board.intentar_reingreso("blanco")
        self.assertFalse(resultado)
if __name__ == "__main__":
    unittest.main()
