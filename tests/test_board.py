import unittest
import io
from unittest.mock import patch
from core.board import Board
from core.checker import Checker


class TestBoard(unittest.TestCase):
    """Pruebas unitarias para el módulo Board."""

    def setUp(self):
        """Inicializa un tablero con fichas estándar antes de cada prueba."""
        self.board = Board()
        self.board.inicializar_fichas()

    def test_inicializacion_correcta(self):
        """Verifica que las fichas iniciales estén en las posiciones correctas."""
        self.assertEqual(len(self.board._puntos_[0]), 2)
        self.assertTrue(all(f._color_ == "blanco" for f in self.board._puntos_[0]))
        self.assertEqual(len(self.board._puntos_[23]), 2)
        self.assertTrue(all(f._color_ == "negro" for f in self.board._puntos_[23]))

    def test_mover_ficha_valida(self):
        """Verifica que una ficha se mueva correctamente entre puntos válidos."""
        self.board._puntos_[12] = []
        self.board.mover_ficha(11, 12, "blanco")
        self.assertEqual(len(self.board._puntos_[11]), 4)
        self.assertEqual(len(self.board._puntos_[12]), 1)
        self.assertEqual(self.board._puntos_[12][0]._position_, 12)

    def test_mover_ficha_con_captura(self):
        """Verifica que se capture una ficha rival si hay una sola en destino."""
        self.board._puntos_[12] = [Checker("negro", 12)]
        self.board._puntos_[11] = [Checker("blanco", 11)]
        self.board.mover_ficha(11, 12, "blanco")
        self.assertEqual(len(self.board._puntos_[12]), 1)
        self.assertEqual(self.board._puntos_[12][0]._color_, "blanco")

    def test_mover_ficha_color_incorrecto(self):
        """Verifica que no se pueda mover una ficha si el color no coincide."""
        self.board._puntos_[12] = [Checker("negro", 12)]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(12, 13, "blanco")

    def test_mover_ficha_origen_vacio(self):
        """Verifica que no se pueda mover desde un punto vacío."""
        self.board._puntos_[10] = []
        with self.assertRaises(ValueError):
            self.board.mover_ficha(10, 11, "blanco")

    def test_mover_ficha_fuera_de_rango(self):
        """Verifica que no se pueda mover desde o hacia posiciones inválidas."""
        self.board._puntos_[0] = [Checker("blanco", 0)]
        with self.assertRaises(ValueError):
            self.board.mover_ficha(-1, 5, "blanco")
        with self.assertRaises(ValueError):
            self.board.mover_ficha(0, 24, "blanco")

    def test_eliminar_ficha_si_unica(self):
        """Verifica que se elimine correctamente una ficha única del punto."""
        self.board._puntos_[5] = [Checker("negro", 5)]
        ficha = self.board.eliminar_ficha_si_unica(5, "negro")
        self.assertEqual(ficha._color_, "negro")
        self.assertEqual(self.board._puntos_[5], [])

    def test_eliminar_ficha_falla_si_multiple(self):
        """Verifica que no se elimine si hay más de una ficha en el punto."""
        self.board._puntos_[5] = [Checker("negro", 5), Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "negro")

    def test_eliminar_ficha_color_incorrecto(self):
        """Verifica que no se elimine si el color no coincide con el jugador."""
        self.board._puntos_[5] = [Checker("negro", 5)]
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(5, "blanco")

    def test_eliminar_ficha_fuera_de_rango(self):
        """Verifica que no se pueda eliminar desde una posición inválida."""
        with self.assertRaises(ValueError):
            self.board.eliminar_ficha_si_unica(24, "blanco")

    def test_puede_entrar_desde_bar_blanco(self):
        """Verifica los casos válidos e inválidos de entrada desde la barra para blanco."""
        self.board._puntos_[3] = []
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 3))
        self.board._puntos_[4] = [Checker("blanco", 4)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 4))
        self.board._puntos_[5] = [Checker("negro", 5)]
        self.assertTrue(self.board.puede_entrar_desde_bar("blanco", 5))
        self.board._puntos_[6] = [Checker("negro", 6), Checker("negro", 6)]
        self.assertFalse(self.board.puede_entrar_desde_bar("blanco", 6))

    def test_puede_entrar_desde_bar_negro(self):
        """Verifica la entrada desde la barra para el jugador negro."""
        for i in range(18, 24):
            self.board._puntos_[i] = []
        self.assertTrue(self.board.puede_entrar_desde_bar("negro", 18))

    def test_reingreso_exitoso(self):
        """Verifica que se pueda reingresar desde la barra si hay espacio disponible."""
        entrada = self.board.intentar_reingreso("blanco")
        self.assertIn(entrada, range(0, 6))
        self.assertTrue(
            any(f._color_ == "blanco" for f in self.board._puntos_[entrada])
        )

    def test_reingreso_prioriza_punto_mas_bajo(self):
        """Verifica que el reingreso se haga en el primer punto disponible."""
        self.board._puntos_[0] = []
        self.board._puntos_[1] = []
        entrada = self.board.intentar_reingreso("blanco")
        self.assertEqual(entrada, 0)

    def test_reingreso_fallido(self):
        """Verifica que no se pueda reingresar si todos los puntos están bloqueados."""
        b = Board()
        for i in range(6):
            b._puntos_[i] = [Checker("negro", i), Checker("negro", i)]
        entrada = b.intentar_reingreso("blanco")
        self.assertIsNone(entrada)

    def test_registro_de_jugada_con_captura(self):
        """Verifica que se registre correctamente una jugada con captura."""
        self.board.registrar_jugada("blanco", 0, 5, captura=True)
        self.assertEqual(len(self.board.historial_de_jugadas), 1)
        jugada = self.board.historial_de_jugadas[0]
        self.assertEqual(jugada["jugador"], "blanco")
        self.assertEqual(jugada["origen"], 0)
        self.assertEqual(jugada["destino"], 5)
        self.assertTrue(jugada["captura"])

    def test_registro_de_jugada_sin_captura(self):
        """Verifica que se registre correctamente una jugada sin captura."""
        self.board.registrar_jugada("negro", 5, 10)
        jugada = self.board.historial_de_jugadas[0]
        self.assertEqual(jugada["jugador"], "negro")
        self.assertEqual(jugada["origen"], 5)
        self.assertEqual(jugada["destino"], 10)
        self.assertFalse(jugada["captura"])

    def test_mostrar_historial(self, mock_stdout):
        """Verifica que el historial de jugadas se imprima correctamente."""
        self.board.registrar_jugada("blanco", 0, 5, captura=True)
        self.board.mostrar_historial()
        output = mock_stdout.getvalue()
        self.assertIn("Move history:", output)
        self.assertIn("blanco moved from 0 to 5 (capture)", output)

    def test_mostrar_tablero(self, mock_stdout):
        """Verifica que el tablero se imprima correctamente en consola."""
        self.board.mostrar_tablero()
        output = mock_stdout.getvalue()
        self.assertIn("TOP ZONE", output)
        self.assertIn("BOTTOM ZONE", output)
        self.assertIn("B", output)
        self.assertIn("N", output)

    def test_mostrar_tablero_con_barra_y_borneadas(self, mock_stdout):
        """Verifica que se impriman correctamente las fichas en barra y borneadas."""
        self.board._barra_bl
