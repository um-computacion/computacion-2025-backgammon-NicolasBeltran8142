import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import TableroView, EstadoView, fichas_movibles, iniciar_juego_cli
from core.game import Game


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.juego = Game()
        self.tablero = TableroView()
        self.estado = EstadoView()

    # ---------- TableroView ----------
    def test_tablero_imprime_estructura_basica(self):
        with patch("sys.stdout", new=StringIO()) as out:
            self.tablero.mostrar(self.juego)
            s = out.getvalue()
        self.assertIn("Estado del tablero:", s)
        self.assertIn("BARRA", s)
        self.assertIn("Fichas borneadas:", s)

    def test_tablero_con_tablero_vacio(self):
        self.juego.board._puntos_ = [[] for _ in range(24)]
        with patch("sys.stdout", new=StringIO()) as out:
            self.tablero.mostrar(self.juego)
            s = out.getvalue()
        self.assertIn("Estado del tablero:", s)

    def test_tablero_con_muchas_fichas_en_un_punto_y_en_barra(self):
        ficha_blanca = MagicMock(_color_="blanco")
        self.juego.board._puntos_[0] = [ficha_blanca] * 6
        self.juego.fichas_en_barra = MagicMock(return_value=[ficha_blanca] * 7)
        self.juego.fichas_borneadas = MagicMock(return_value=[])
        with patch("sys.stdout", new=StringIO()) as out:
            self.tablero.mostrar(self.juego)
            s = out.getvalue()
        # Cuando hay >5 fichas en un punto, la línea inferior imprime el conteo "6"
        self.assertIn("6", s)

    def test_tablero_con_segmentos_superior_e_inferior_activos(self):
        mock_b = MagicMock(_color_="blanco")
        mock_n = MagicMock(_color_="negro")
        self.juego.board._puntos_[12] = [mock_b] * 3
        self.juego.board._puntos_[18] = [mock_n] * 2
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_b, mock_n])
        self.juego.fichas_borneadas = MagicMock(
            side_effect=lambda c: ([mock_b] * 2) if c == "blanco" else [mock_n]
        )
        with patch("sys.stdout", new=StringIO()) as out:
            self.tablero.mostrar(self.juego)
            s = out.getvalue()
        self.assertIn("Estado del tablero:", s)
        self.assertIn("BARRA", s)
        self.assertIn("Fichas borneadas:", s)

    # ---------- EstadoView ----------
    def test_estado_view_basico(self):
        with patch("sys.stdout", new=StringIO()) as out:
            self.estado.mostrar(self.juego)
            s = out.getvalue()
        self.assertIn("Turno de:", s)
        self.assertIn("Fichas en barra:", s)
        self.assertIn("Movimientos disponibles:", s)

    def test_estado_view_con_movimientos(self):
        self.juego.available_moves = [1, 2, 3, 4]
        with patch("sys.stdout", new=StringIO()) as out:
            self.estado.mostrar(self.juego)
            s = out.getvalue()
        self.assertIn("Movimientos disponibles", s)

    # ---------- fichas_movibles ----------
    def test_fichas_movibles_sin_movimientos(self):
        self.juego.available_moves = []
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertEqual(fichas, [])

    def test_fichas_movibles_con_top_de_mi_color_y_puede_mover(self):
        # Armo un punto con una ficha blanca arriba
        ficha_top = MagicMock(_color_="blanco", _position_=3)
        self.juego.board._puntos_[3] = [MagicMock(), ficha_top]
        self.juego.available_moves = [2, 4]
        # El juego dice que ese punto es válido como origen
        self.juego.puntos_validos_de_origen = MagicMock(return_value=[3])
        # Y que ambos destinos son válidos
        self.juego.puede_mover = MagicMock(side_effect=lambda o, d, c: True)

        movibles = fichas_movibles(self.juego, "blanco")
        self.assertEqual(len(movibles), 1)
        ficha, destinos = movibles[0]
        self.assertEqual(ficha, ficha_top)
        self.assertTrue(set(destinos) == {5, 7})

    def test_fichas_movibles_top_de_otro_color_no_cuenta(self):
        # Top de color distinto
        ficha_top = MagicMock(_color_="negro", _position_=8)
        self.juego.board._puntos_[8] = [ficha_top]
        self.juego.available_moves = [1]
        self.juego.puntos_validos_de_origen = MagicMock(return_value=[8])
        self.juego.puede_mover = MagicMock(return_value=True)

        movibles = fichas_movibles(self.juego, "blanco")
        self.assertEqual(movibles, [])

    def test_fichas_movibles_cuando_puede_mover_falso(self):
        ficha_top = MagicMock(_color_="blanco", _position_=5)
        self.juego.board._puntos_[5] = [ficha_top]
        self.juego.available_moves = [6]
        self.juego.puntos_validos_de_origen = MagicMock(return_value=[5])
        self.juego.puede_mover = MagicMock(return_value=False)

        movibles = fichas_movibles(self.juego, "blanco")
        self.assertEqual(movibles, [])

    # ---------- iniciar_juego_cli (flujos completos) ----------
    @patch("builtins.input")
    def test_cli_flujo_movimiento_valido_y_fin(self, mock_input):
        # Entradas: tirar dados, elegir ficha 0, destino 4, no continuar
        mock_input.side_effect = ["", "0", "4", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [4]

        def mover_y_limpiar(*_):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover_y_limpiar)

        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles",
                return_value=[(MagicMock(_position_=1), [4])],
            ):
                with patch("sys.stdout", new=StringIO()) as out:
                    iniciar_juego_cli()
                    s = out.getvalue()
        self.assertIn("Movimiento exitoso", s)
        self.assertIn("Fin del juego", s)

    @patch("builtins.input")
    def test_cli_sin_movimientos_posibles(self, mock_input):
        mock_input.side_effect = ["", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 1]
        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[]):
                with patch("sys.stdout", new=StringIO()) as out:
                    iniciar_juego_cli()
                    s = out.getvalue()
        self.assertIn("No hay movimientos posibles", s)

    @patch("builtins.input")
    def test_cli_entrada_invalida_y_luego_valida(self, mock_input):
        mock_input.side_effect = ["", "abc", "0", "3", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3]

        def mover(*_):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover)

        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles",
                return_value=[(MagicMock(_position_=1), [3])],
            ):
                with patch("sys.stdout", new=StringIO()) as out:
                    iniciar_juego_cli()
                    s = out.getvalue()
        self.assertIn("Entrada inválida. Intentá de nuevo", s)
        self.assertIn("Movimiento exitoso", s)

    @patch("builtins.input")
    def test_cli_seleccion_fuera_de_rango(self, mock_input):
        mock_input.side_effect = ["", "99", "0", "2", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [2]
        self.juego.verificar_ganador = MagicMock(return_value=None)

        def mover_y_limpiar(*_):
            self.juego.available_moves.clear()
            return True

        self.juego.mover_ficha = MagicMock(side_effect=mover_y_limpiar)

        with patch("cli.cli.Game", return_value=self.juego):
            with patch(
                "cli.cli.fichas_movibles",
                return_value=[(MagicMock(_position_=0), [2])],
            ):
                with patch("sys.stdout", new=StringIO()) as out:
                    iniciar_juego_cli()
                    s = out.getvalue()
        self.assertIn("Entrada inválida. Intentá de nuevo", s)

    @patch("builtins.input")
    def test_cli_destino_no_permitido(self, mock_input):
        mock_input.side_effect = ["", "0", "99", "0", "3", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3]
        self.juego.verificar_ganador = MagicMock(return_value=None)

        def mover_y_limpiar(origen, destino, color):
            if destino == 3:
                self.juego.available_moves.clear()
                return True
            return False

        self.juego.mover_ficha = MagicMock(side_effect=mover_y_limpiar)
        ficha = MagicMock(_position_=0, _color_="blanco")

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[(ficha, [3])]):
                with patch("sys.stdout", new=StringIO()) as out:
                    iniciar_juego_cli()
                    s = out.getvalue()
        self.assertIn("Destino no permitido para esa ficha", s)
        self.assertIn("Movimiento exitoso", s)

    @patch("builtins.input")
    def test_cli_movimiento_invalido_luego_exitoso(self, mock_input):
        mock_input.side_effect = ["", "0", "4", "0", "3", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3]

        def mover_side(origen, destino, color):
            if destino == 4:
                return False
            if destino == 3:
                self.juego.available_moves.clear()
                return True
            return False

        self.juego.mover_ficha = MagicMock(side_effect=mover_side)
        self.juego.verificar_ganador = MagicMock(return_value=None)
        mock_ficha = MagicMock(_position_=0, _color_="blanco")

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("cli.cli.fichas_movibles", return_value=[(mock_ficha, [3, 4])]):
                with patch("sys.stdout", new=StringIO()) as out:
                    iniciar_juego_cli()
                    s = out.getvalue()
        self.assertIn("Movimiento inválido", s)
        self.assertIn("Movimiento exitoso", s)

    @patch("builtins.input")
    def test_cli_victoria_inmediata(self, mock_input):
        mock_input.side_effect = ["", "s", ""]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 1"])

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as out:
                iniciar_juego_cli()
                s = out.getvalue()
        self.assertIn("Jugador 1 ha ganado el juego", s)

    @patch("builtins.input")
    def test_cli_continuar_turno_y_ganar(self, mock_input):
        mock_input.side_effect = ["", "s", ""]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 2"])

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as out:
                iniciar_juego_cli()
                s = out.getvalue()
        self.assertIn("Jugador 2 ha ganado el juego", s)

    @patch("builtins.input")
    def test_cli_salida_manual_sin_ganador(self, mock_input):
        mock_input.side_effect = ["", "n"]
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(return_value=None)

        with patch("cli.cli.Game", return_value=self.juego):
            with patch("sys.stdout", new=StringIO()) as out:
                iniciar_juego_cli()
                s = out.getvalue()
        self.assertIn("Fin del juego", s)


if __name__ == "__main__":
    unittest.main()