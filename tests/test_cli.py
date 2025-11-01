import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from io import StringIO
from cli.cli import TableroView, EstadoView, fichas_movibles
from core.game import Game

class TestCLIViews(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_tablero_mostrar_basico(self, mock_stdout):
        juego = MagicMock()
        juego.board._puntos_ = [[] for _ in range(24)]
        juego.fichas_en_barra.return_value = []
        juego.fichas_borneadas.return_value = []

        view = TableroView()
        view.mostrar(juego)

        output = mock_stdout.getvalue()
        self.assertIn("Estado del tablero:", output)
        self.assertIn("Fichas borneadas:", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_tablero_mostrar_con_fichas(self, mock_stdout):
        
        ficha_mock = MagicMock()
        ficha_mock._color_ = "blanco"

        puntos = [[ficha_mock] for _ in range(24)]

        juego = MagicMock()
        juego.board._puntos_ = puntos
        juego.fichas_en_barra.return_value = [ficha_mock]
        juego.fichas_borneadas.side_effect = lambda c: [ficha_mock] if c == "blanco" else []

        view = TableroView()
        view.mostrar(juego)

        output = mock_stdout.getvalue()
        self.assertIn("BARRA", output)
        self.assertIn("Fichas borneadas", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_estado_view_mostrar(self, mock_stdout):
        jugador = MagicMock()
        jugador.nombre = "Marcos"
        jugador.color = "blanco"

        juego = MagicMock()
        juego.jugador_actual.return_value = jugador
        juego.fichas_en_barra.return_value = []
        juego.fichas_borneadas.return_value = []
        juego.last_roll = (3, 4)
        juego.available_moves = [3, 4]

        view = EstadoView()
        view.mostrar(juego)

        output = mock_stdout.getvalue()
        self.assertIn("Turno de:", output)
        self.assertIn("Marcos", output)
        self.assertIn("Ultimo tiro:", output)
        self.assertIn("Movimientos disponibles:", output)

    def test_fichas_movibles_con_movimientos(self):
        ficha = MagicMock()
        ficha._color_ = "blanco"
        ficha._position_ = 0

        juego = MagicMock()
        juego.board._puntos_ = [[ficha]] + [[] for _ in range(23)]
        juego.puntos_validos_de_origen.return_value = [0]
        juego.available_moves = [3, 5]
        juego.puede_mover.return_value = True

        result = fichas_movibles(juego, "blanco")
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0][1], list)
        self.assertIn(3, result[0][1])

    def test_fichas_movibles_sin_movimientos(self):
        ficha = MagicMock()
        ficha._color_ = "blanco"
        ficha._position_ = 0

        juego = MagicMock()
        juego.board._puntos_ = [[ficha]] + [[] for _ in range(23)]
        juego.puntos_validos_de_origen.return_value = [0]
        juego.available_moves = [3]
        juego.puede_mover.return_value = False

        result = fichas_movibles(juego, "blanco")
        self.assertEqual(result, [])

    @patch('builtins.input', side_effect=['n'])
    @patch('sys.stdout', new_callable=StringIO)
    @patch('cli.cli.Game')
    def test_ejecutar_cli_salir_inmediato(self, mock_game, mock_stdout, mock_input):
        from cli.cli import ejecutar_cli

        juego_mock = MagicMock()
        juego_mock.available_moves = []
        juego_mock.verificar_ganador.return_value = None
        mock_game.return_value = juego_mock

        ejecutar_cli()
        output = mock_stdout.getvalue()
        self.assertIn("Bienvenido a Backgammon CLI", output)
        self.assertIn("Fin del juego", output)

    
