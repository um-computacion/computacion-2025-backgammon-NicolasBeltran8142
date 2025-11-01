import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import TableroView, EstadoView, fichas_movibles, ejecutar_cli
from core.game import Game


class TestCli(unittest.TestCase):
    """Pruebas completas para la interfaz de linea de comandos."""

    def setUp(self):
        self.juego = Game()
        self.tablero_view = TableroView()
        self.estado_view = EstadoView()

    def test_mostrar_tablero(self):
        """Verifica que el tablero se imprime correctamente."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Estado del tablero", output)
            self.assertIn("BARRA", output)
            self.assertIn("Fichas borneadas", output)

    def test_mostrar_estado(self):
        """Verifica que el estado se muestra correctamente."""
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Turno de", output)
            self.assertIn("Fichas en barra", output)
            self.assertIn("Movimientos disponibles", output)

    def test_mostrar_tablero_vacio(self):
        """Cubre tablero vacio sin fichas."""
        self.juego.board._puntos_ = [[] for _ in range(24)]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Estado del tablero", output)

    def test_mostrar_estado_con_datos(self):
        """Cubre el caso donde hay fichas en barra y borneadas."""
        self.juego.turno = "negro"
        self.juego.fichas_en_barra = MagicMock(return_value=[1, 2])
        self.juego.available_moves = [4, 6]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Turno de", output)
            self.assertIn("Jugador", output)

    def test_fichas_movibles_con_movimientos(self):
        """Cubre fichas movibles."""
        self.juego.available_moves = [3, 4]
        self.juego.board.inicializar_fichas()
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertTrue(isinstance(fichas, list))

    def test_fichas_movibles_sin_movimientos(self):
        """Cubre el caso sin movimientos."""
        self.juego.available_moves = []
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertEqual(len(fichas), 0)

    @patch("builtins.input")
    def test_ejecutar_cli_movimiento_valido_y_salida(self, mock_input):
        """Flujo basico con movimiento y salida."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3, 4]

        def mover_y_limpiar(*args):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover_y_limpiar)
        mock_input.side_effect = ["", "0", "4", "n"]

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()

        salida = fake_out.getvalue()
        self.assertIn("Movimiento exitoso", salida)
        self.assertIn("Fin del juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_sin_movimientos_posibles(self, mock_input):
        """Jugador sin movimientos."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 1]
        mock_input.side_effect = ["", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("No hay movimientos posibles", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_entrada_invalida(self, mock_input):
        """Entrada no numerica."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 2]

        def mover(*args):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover)
        mock_input.side_effect = ["", "abc", "0", "3", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles", return_value=[(MagicMock(_position_=1), [3])]
            ):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Entrada invalida", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_victoria(self, mock_input):
        """Flujo donde un jugador gana."""
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 1"])
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        mock_input.side_effect = ["", "s", ""]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Jugador 1 ha ganado el juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_continuar_turno_y_ganar(self, mock_input):
        """Jugador continua y luego gana."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 2"])
        mock_input.side_effect = ["", "s", ""]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Jugador 2 ha ganado el juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_index_error_en_seleccion(self, mock_input):
        """Seleccion fuera del rango."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [2]
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_input.side_effect = ["", "99", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles", return_value=[(MagicMock(_position_=0), [2])]
            ):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Entrada invalida", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_sin_ganador_y_salida_manual(self, mock_input):
        """Jugador sale sin ganar."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_input.side_effect = ["", "n"]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Fin del juego", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_movimiento_invalido_reintento(self, mock_input):
        """Cubre un intento de movimiento invalido seguido de exito."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3]
        self.juego.mover_ficha = MagicMock(side_effect=[False, True])
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_input.side_effect = ["", "0", "4", "0", "3", "n"]
        mock_ficha = MagicMock(_position_=0, _color_="blanco")
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[(mock_ficha, [3])]):
                with patch("sys.stdout", new=StringIO()) as fake_out:
                    ejecutar_cli()
        salida = fake_out.getvalue()
        self.assertIn("Movimiento invalido", salida)
        self.assertIn("Movimiento exitoso", salida)

    def test_tablero_view_con_fichas_largas(self):
        """Punto con muchas fichas."""
        mock_ficha = MagicMock(_color_="blanco")
        self.juego.board._puntos_[0] = [mock_ficha] * 6
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_ficha] * 6)
        self.juego.fichas_borneadas = MagicMock(return_value=[])
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            salida = fake_out.getvalue()
            self.assertIn("6", salida)

    def test_tablero_view_con_fichas_en_todos_los_segmentos(self):
        """Puntos, barra y borneadas activas."""
        mock_blanca = MagicMock(_color_="blanco")
        mock_negra = MagicMock(_color_="negro")
        self.juego.board._puntos_[12] = [mock_blanca] * 3
        self.juego.board._puntos_[18] = [mock_negra] * 2
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_blanca, mock_negra])
        self.juego.fichas_borneadas = MagicMock(
            side_effect=lambda color: (
                [mock_blanca] * 2 if color == "blanco" else [mock_negra]
            )
        )
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            salida = fake_out.getvalue()
            self.assertIn("Estado del tablero", salida)
            self.assertIn("BARRA", salida)
            self.assertIn("Fichas borneadas", salida)

    def test_estado_view_con_muchos_movimientos(self):
        """Cubre el caso con varios movimientos disponibles."""
        self.juego.available_moves = [1, 2, 3, 4]
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            salida = fake_out.getvalue()
            self.assertIn("Movimientos disponibles", salida)

    @patch("builtins.input")
    def test_ejecutar_cli_con_instancia_real(self, mock_input):
        """Ejecuta el CLI con Game real para cubrir líneas finales."""
        mock_input.side_effect = ["", "n"]  # tirar dados, salir

        with patch("sys.stdout", new=StringIO()) as fake_out:
            ejecutar_cli()

        salida = fake_out.getvalue()
        self.assertIn("Fin del juego", salida)


if __name__ == "__main__":
    unittest.main()
