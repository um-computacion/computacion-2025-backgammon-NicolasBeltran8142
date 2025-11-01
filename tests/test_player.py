import unittest
import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from core.player import Jugador, TurnManager


class TestJugador(unittest.TestCase):

    def setUp(self):
        self.jugador = Jugador("Jugador 1", "blanco")
        self.jugador_negro = Jugador("Jugador 2", "negro")

    # Creación y atributos
    def test_jugador_se_inicializa_correctamente(self):
        self.assertEqual(self.jugador.nombre, "Jugador 1")
        self.assertEqual(self.jugador.color, "blanco")
        self.assertEqual(self.jugador.puntos, 0)
        self.assertEqual(self.jugador.fichas_fuera, 0)
        self.assertEqual(len(self.jugador.fichas), 15)

    def test_str_representacion(self):
        self.assertEqual(
            str(self.jugador), "Jugador 1 juega con fichas blanco"
        )

    # Puntos
    def test_sumar_puntos_incrementa_correctamente(self):
        self.jugador.sumar_puntos(5)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3)
        self.assertEqual(self.jugador.puntos, 8)

    # Fichas fuera
    def test_sacar_ficha_incrementa_fichas_fuera(self):
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 1)
        for _ in range(4):
            self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 5)

    # Victoria
    def test_ha_ganado_devuelve_false_si_faltan_fichas(self):
        self.assertFalse(self.jugador.ha_ganado())
        for _ in range(14):
            self.jugador.sacar_ficha()
        self.assertFalse(self.jugador.ha_ganado())

    def test_ha_ganado_devuelve_true_si_tiene_15_fichas_fuera(self):
        for ficha in self.jugador.fichas:
            ficha._position_ = "off"
        self.assertTrue(self.jugador.ha_ganado())

    # Estado y posición de fichas
    def test_fichas_en_estado(self):
        self.jugador.fichas[0]._position_ = "bar"
        self.jugador.fichas[1]._position_ = "off"
        self.assertEqual(len(self.jugador.fichas_en_estado("bar")), 1)
        self.assertEqual(len(self.jugador.fichas_en_estado("off")), 1)

    def test_fichas_en_punto(self):
        self.jugador.fichas[0]._position_ = 5
        self.jugador.fichas[1]._position_ = 5
        self.assertEqual(len(self.jugador.fichas_en_punto(5)), 2)

    # Lógica de "bear off"
    def test_puede_sacar_fichas_blancas(self):
        mock_board = MagicMock()
        for i in range(15):
            self.jugador.fichas[i]._position_ = 18 + (i % 6)
        self.assertTrue(self.jugador.puede_sacar_fichas(mock_board))

    def test_puede_sacar_fichas_negras(self):
        mock_board = MagicMock()
        for i in range(15):
            self.jugador_negro.fichas[i]._position_ = i % 6
        self.assertTrue(self.jugador_negro.puede_sacar_fichas(mock_board))

    def test_no_puede_sacar_fichas_si_no_estan_en_casa(self):
        mock_board = MagicMock()
        self.jugador.fichas[0]._position_ = 17
        self.assertFalse(self.jugador.puede_sacar_fichas(mock_board))


class TestTurnManager(unittest.TestCase):

    def setUp(self):
        self.jugador_a = Jugador("A", "white")
        self.jugador_b = Jugador("B", "black")
        self.tm = TurnManager(self.jugador_a, self.jugador_b)

    def test_alternancia_de_turnos_funciona_correctamente(self):
        self.assertEqual(self.tm.jugador_actual().nombre, "A")
        self.tm.siguiente_turno()
        self.assertEqual(self.tm.jugador_actual().nombre, "B")
        self.tm.siguiente_turno()
        self.assertEqual(self.tm.jugador_actual().nombre, "A")

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_turno(self, mock_stdout):
        self.tm.mostrar_turno()
        self.assertIn("Turno: A (white)", mock_stdout.getvalue())
        self.tm.siguiente_turno()
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        self.tm.mostrar_turno()
        self.assertIn("Turno: B (black)", mock_stdout.getvalue())
