import unittest
from core.board import Board, historial_de_jugadas, registrar_jugada
from core.checker import Checker

class TestBoardInitialization(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.inicializar_fichas()

    def test_total_fichas(self):
        total = sum(len(punto) for punto in self.board._puntos_)
        self.assertEqual(total, 30)

    def test_posiciones_blancas(self):
        posiciones_blancas = {0: 2, 11: 5, 16: 3, 18: 5}
        for punto, cantidad in posiciones_blancas.items():
            fichas = self.board._puntos_[punto]
            self.assertEqual(len([f for f in fichas if f._color_ == "blanco"]), cantidad)

    def test_posiciones_negras(self):
        posiciones_negras = {23: 2, 12: 5, 7: 3, 5: 5}
        for punto, cantidad in posiciones_negras.items():
            fichas = self.board._puntos_[punto]
            self.assertEqual(len([f for f in fichas if f._color_ == "negro"]), cantidad)
    def test_mostrar_tablero_activa_ramas(self):
        board = Board()
        board.mostrar_tablero()


class TestMovimientoFichas(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.inicializar_fichas()

    def test_mover_ficha_valida(self):
        self.board.mover_ficha(0, 1, "blanco")
        self.assertEqual(len(self.board._puntos_[0]), 1)
        self.assertEqual(len(self.board._puntos_[1]), 1)
        self.assertEqual(self.board._puntos_[1][0]._color_, "blanco")

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

    def test_mover_ficha_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.board.mover_ficha(-1, 25, "blanco")

class TestEliminarFichas(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_eliminar_ficha_unica_exitosa(self):
        self.board._puntos_[8] = [Checker("blanco", 8)]
        ficha = self.board.eliminar_ficha_si_unica(8, "blanco")
        self.assertEqual(ficha._color_, "blanco")
        self.assertEqual(self.board._puntos_[8], [])

    def test_error_si_multiples_fichas(self):
        self.board._puntos_[5] = [Checker("negro", 5), Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "negro")

    def test_error_si_color_incorrecto(self):
        self.board._puntos_[7] = [Checker("blanco", 7)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(7, "negro")

    def test_error_si_punto_vacio(self):
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(3, "blanco")

    def test_error_si_indice_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(24, "blanco")
    
    def test_mover_desde_punto_vacio(self):
        board = Board()
        # Punto 3 está vacío por defecto
        with self.assertRaises(ValueError) as context:
            board.mover_ficha(3, 5, "blanco")
        self.assertIn("No hay fichas en el punto", str(context.exception))



class TestReingresoDesdeBar(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_puede_entrar_en_punto_vacio(self):
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_puede_entrar_con_una_ficha_rival(self):
        self.board._puntos_[0] = [Checker("negro", 0)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_no_puede_entrar_si_bloqueado(self):
        self.board._puntos_[0] = [Checker("negro", 0), Checker("negro", 0)]
        self.assertFalse(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_puede_entrar_con_fichas_propias(self):
        self.board._puntos_[0] = [Checker("blanco", 0), Checker("blanco", 0)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 0))

    def test_reingreso_exitoso(self):
        resultado = self.board.intentar_reingreso("blanco")
        self.assertTrue(resultado)
        self.assertTrue(any(
            self.board._puntos_[i] and self.board._puntos_[i][-1]._color_ == "blanco"
            for i in range(0, 6)
        ))

    def test_reingreso_fallido(self):
        for i in range(0, 6):
            self.board._puntos_[i] = [Checker("negro", i), Checker("negro", i)]
        resultado = self.board.intentar_reingreso("blanco")
        self.assertFalse(resultado)

class TestRegistro(unittest.TestCase):
    def test_registrar_jugada_sin_captura(self):
        historial_de_jugadas.clear()
        registrar_jugada("Jugador1", 5, 10)
        self.assertEqual(len(historial_de_jugadas), 1)
        jugada = historial_de_jugadas[0]
        self.assertEqual(jugada["jugador"], "Jugador1")
        self.assertEqual(jugada["origen"], 5)
        self.assertEqual(jugada["destino"], 10)
        self.assertFalse(jugada["captura"])

    def test_registrar_jugada_con_captura(self):
        historial_de_jugadas.clear()
        registrar_jugada("Jugador1", 4, 6, captura=True)
        jugada = historial_de_jugadas[0]
        self.assertTrue(jugada["captura"])

class TestChecker(unittest.TestCase):
    def test_atributos_checker(self):
        ficha = Checker("blanco", 5)
        self.assertEqual(ficha._color_, "blanco")
        self.assertEqual(ficha._position_, 5)


class TestFormatoTablero(unittest.TestCase):
    def test_formato_punto_vacio(self):
        board = Board()
        self.assertEqual(board._puntos_[10], [])
        board.mostrar_tablero()  

if __name__ == "__main__":
    unittest.main()
