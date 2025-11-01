import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from cli.cli import TableroView, EstadoView, fichas_movibles
from core.game import Game


class TestTableroView(unittest.TestCase):

    def setUp(self):
        self.juego = Game()
        self.vista = TableroView()

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_tablero_no_vacio(self, mock_stdout):
        self.vista.mostrar(self.juego)
        output = mock_stdout.getvalue()
        self.assertIn("Estado del tablero:", output)
        self.assertIn("13  14  15  16  17  18", output)
        self.assertIn("Blanco=", output)
        self.assertIn("Negro=", output)


class TestEstadoView(unittest.TestCase):

    def setUp(self):
        self.juego = Game()
        self.vista = EstadoView()

    @patch('sys.stdout', new_callable=StringIO)
    def test_mostrar_estado_del_juego(self):
        self.juego.last_roll = (3, 4)
        self.juego.available_moves = [3, 4]
        resultado = self.vista.mostrar(self.juego)
        self.assertIn("Turno de: Jugador 1 (blanco)", resultado)
        self.assertIn("Dados: (3, 4)", resultado)
        self.assertIn("Movimientos restantes: [3, 4]", resultado)


class TestFichasMovibles(unittest.TestCase):

    def setUp(self):
        self.juego = Game()

    def test_fichas_movibles_al_inicio(self):
        self.juego.available_moves = [1, 2]
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertTrue(len(fichas) > 0)

    def test_sin_fichas_movibles_si_no_hay_movimientos(self):
        self.juego.available_moves = []
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertEqual(len(fichas), 0)
