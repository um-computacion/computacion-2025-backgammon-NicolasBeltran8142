import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from core.player import Jugador, TurnManager


class TestJugador(unittest.TestCase):
    """Pruebas unitarias para la clase Jugador."""

    def setUp(self):
        """Inicializa dos jugadores antes de cada prueba."""
        self.jugador = Jugador("Jugador 1", "blanco")
        self.jugador_negro = Jugador("Jugador 2", "negro")

    def test_jugador_se_inicializa_correctamente(self):
        """Verifica que los atributos iniciales del jugador sean correctos."""
        self.assertEqual(self.jugador.nombre, "Jugador 1")
        self.assertEqual(self.jugador.color, "blanco")
        self.assertEqual(self.jugador.puntos, 0)
        self.assertEqual(self.jugador.fichas_fuera, 0)
        self.assertEqual(len(self.jugador.fichas), 15)

    def test_str_representacion(self):
        """Verifica la representación en texto del jugador."""
        self.assertEqual(str(self.jugador), "Jugador 1 juega con fichas blanco")

    def test_sumar_puntos_incrementa_correctamente(self):
        """Verifica que los puntos se acumulen correctamente."""
        self.jugador.sumar_puntos(5, verbose=False)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3, verbose=False)
        self.assertEqual(self.jugador.puntos, 8)

    def test_sacar_ficha_incrementa_fichas_fuera(self):
        """Verifica que sacar fichas aumente el contador de fichas fuera."""
        self.jugador.sacar_ficha(verbose=False)
        self.assertEqual(self.jugador.fichas_fuera, 1)
        for _ in range(4):
            self.jugador.sacar_ficha(verbose=False)
        self.assertEqual(self.jugador.fichas_fuera, 5)

    def test_ha_ganado_devuelve_false_si_faltan_fichas(self):
        """Verifica que no se declare victoria si faltan fichas fuera."""
        self.assertFalse(self.jugador.ha_ganado())
        for _ in range(14):
            self.jugador.sacar_ficha(verbose=False)
        self.assertFalse(self.jugador.ha_ganado())

    def test_ha_ganado_devuelve_true_si_tiene_15_fichas_fuera(self):
        """Verifica que se declare victoria si todas las fichas están fuera."""
        for ficha in self.jugador.fichas:
            ficha._position_ = "off"
        self.assertTrue(self.jugador.ha_ganado())

    def test_fichas_en_estado(self):
        """Verifica que se filtren correctamente las fichas por estado."""
        self.jugador.fichas[0]._position_ = "bar"
        self.jugador.fichas[1]._position_ = "off"
        self.assertEqual(len(self.jugador.fichas_en_estado("bar")), 1)
        self.assertEqual(len(self.jugador.fichas_en_estado("off")), 1)

    def test_fichas_en_punto(self):
        """Verifica que se filtren correctamente las fichas por punto."""
        self.jugador.fichas[0]._position_ = 5
        self.jugador.fichas[1]._position_ = 5
        self.assertEqual(len(self.jugador.fichas_en_punto(5)), 2)

    def test_puede_sacar_fichas_blancas(self):
        """Verifica que las fichas blancas puedan ser borneadas si están en casa."""
        mock_board = MagicMock()
        for i in range(15):
            self.jugador.fichas[i]._position_ = 18 + (i % 6)
        self.assertTrue(self.jugador.puede_sacar_fichas(mock_board))

    def test_puede_sacar_fichas_negras(self):
        """Verifica que las fichas negras puedan ser borneadas si están en casa."""
        mock_board = MagicMock()
        for i in range(15):
            self.jugador_negro.fichas[i]._position_ = i % 6
        self.assertTrue(self.jugador_negro.puede_sacar_fichas(mock_board))

    def test_no_puede_sacar_fichas_si_no_estan_en_casa(self):
        """Verifica que no se puedan bornear fichas si alguna está fuera de casa."""
        mock_board = MagicMock()
        self.jugador.fichas[0]._position_ = 17
        self.assertFalse(self.jugador.puede_sacar_fichas(mock_board))


class TestTurnManager(unittest.TestCase):
    """Pruebas unitarias para la clase TurnManager."""

    def setUp(self):
        """Inicializa dos jugadores y el administrador de turnos."""
        self.jugador_a = Jugador("A", "blanco")
        self.jugador_b = Jugador("B", "negro")
        self.tm = TurnManager(self.jugador_a, self.jugador_b)

    def test_alternancia_de_turnos_funciona_correctamente(self):
        """Verifica que los turnos alternen correctamente entre jugadores."""
        self.assertEqual(self.tm.jugador_actual().nombre, "A")
        self.tm.siguiente_turno()
        self.assertEqual(self.tm.jugador_actual().nombre, "B")
        self.tm.siguiente_turno()
        self.assertEqual(self.tm.jugador_actual().nombre, "A")

    @patch("sys.stdout", new_callable=StringIO)
    def test_mostrar_turno(self, mock_stdout):
        """Verifica que se imprima correctamente el turno actual."""
        self.tm.mostrar_turno()
        output = mock_stdout.getvalue()
        self.assertIn("Turno: A (blanco)", output)

        # Cambiamos turno y volvemos a capturar salida
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        self.tm.siguiente_turno()
        self.tm.mostrar_turno()
        output = mock_stdout.getvalue()
        self.assertIn("Turno: B (negro)", output)


if __name__ == "__main__":
    unittest.main()