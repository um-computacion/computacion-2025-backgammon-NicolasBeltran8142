import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import TableroView, EstadoView, fichas_movibles, ejecutar_cli
from core.game import Game

class TestCli(unittest.TestCase):
    """Pruebas para la interfaz de linea de comandos."""

    def setUp(self):
        """Configuracion inicial para cada prueba."""
        self.juego = Game()
        self.tablero_view = TableroView()
        self.estado_view = EstadoView()

    def test_mostrar_tablero(self):
        """Prueba que la vista del tablero se muestra correctamente."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Estado del tablero", output)
            self.assertIn("BARRA", output)
            self.assertIn("Fichas borneadas", output)

    def test_mostrar_estado(self):
        """Prueba que la vista de estado se muestra correctamente."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.estado_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Turno de", output)
            self.assertIn("Fichas en barra", output)
            self.assertIn("Movimientos disponibles", output)

    def test_fichas_movibles_con_movimientos(self):
        """Prueba que se identifican las fichas que se pueden mover."""
        self.juego.available_moves = [3, 4]
        self.juego.board.inicializar_fichas()
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertTrue(len(fichas) > 0)

    def test_fichas_movibles_sin_movimientos(self):
        """Prueba que no se devuelven fichas si no hay movimientos."""
        self.juego.available_moves = []
        fichas = fichas_movibles(self.juego, "blanco")
        self.assertEqual(len(fichas), 0)

    @patch('builtins.input')
    def test_ejecutar_cli_movimiento_valido_y_salida(self, mock_input):
        """Prueba un flujo simple: tirar, mover y salir."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [3, 4]
        
        def mock_move_and_clear(*args):
            self.juego.available_moves.clear()
            return True
        self.juego.mover_ficha = MagicMock(side_effect=mock_move_and_clear)

        mock_input.side_effect = ["", "0", "4", "n"]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('cli.cli.Game', return_value=self.juego):
                ejecutar_cli()
        
        output = fake_out.getvalue()
        self.assertIn("Movimiento exitoso", output)
        self.assertIn("Fin del juego", output)

    @patch('builtins.input')
    def test_ejecutar_cli_sin_movimientos_posibles(self, mock_input):
        """Prueba el caso donde un jugador no tiene movimientos."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 1]
        
        # Simplificado: Tira, no hay movimientos, sale.
        mock_input.side_effect = ["", "n"]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('cli.cli.Game', return_value=self.juego):
                with patch('cli.cli.fichas_movibles', return_value=[]):
                    ejecutar_cli()
        
        output = fake_out.getvalue()
        self.assertIn("No hay movimientos posibles", output)
        self.assertIn("Fin del juego", output)

    @patch('builtins.input')
    def test_ejecutar_cli_entrada_invalida(self, mock_input):
        """Prueba el manejo de errores para entradas no validas."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [1, 2]

        def mock_move_and_clear(*args):
            self.juego.available_moves.clear()
            return True
        self.juego.mover_ficha = MagicMock(side_effect=mock_move_and_clear)
        
        mock_input.side_effect = ["", "letra", "0", "3", "n"]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('cli.cli.Game', return_value=self.juego):
                with patch('cli.cli.fichas_movibles', return_value=[(MagicMock(_position_=1), [3])]):
                    ejecutar_cli()

        output = fake_out.getvalue()
        self.assertIn("Entrada invalida", output)
        self.assertIn("Movimiento exitoso", output)

    @patch('builtins.input')
    def test_ejecutar_cli_victoria(self, mock_input):
        """Prueba el flujo completo hasta que un jugador gana."""
        # El primer turno no hay ganador, el segundo si.
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 1"])
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        
        # Secuencia: Tira, pasa turno, tira de nuevo, gana.
        mock_input.side_effect = ["", "s", ""]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('cli.cli.Game', return_value=self.juego):
                 ejecutar_cli()

        output = fake_out.getvalue()
        self.assertIn("Jugador 1 ha ganado el juego", output)
    def test_tablero_view_con_fichas_largas(self):
        """Prueba los casos donde hay mas de 5 fichas en un punto o en la barra."""
        mock_ficha = MagicMock(_color_="blanco")
        self.juego.board._puntos_[0] = [mock_ficha] * 6
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_ficha] * 6)
        self.juego.fichas_borneadas = MagicMock(return_value=[])
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("6", output)  
    @patch('builtins.input')
    def test_ejecutar_cli_destino_no_permitido_y_movimiento_invalido(self, mock_input):
        """Prueba los mensajes de destino no permitido y movimiento invalido."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [2]
        
        mock_ficha = MagicMock(_position_=0, _color_="blanco")
        self.juego.jugador_actual.return_value.color = "blanco"
        self.juego.mover_ficha.return_value = False  
        self.juego.verificar_ganador.return_value = None

        mock_input.side_effect = [
            "", 
            "0",
            "9",   
            "0",  
            "2",  
            "n"     
        ]

        with patch('cli.cli.Game', return_value=self.juego):
            with patch('cli.cli.fichas_movibles', return_value=[(mock_ficha, [2])]):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    ejecutar_cli()
        output = fake_out.getvalue()
        self.assertIn("Destino no permitido", output)
        self.assertIn("Movimiento invalido", output)
    @patch('builtins.input')
    def test_ejecutar_cli_continuar_turno_y_ganar(self, mock_input):
        """Cubre el flujo donde el jugador decide continuar y luego hay un ganador."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(side_effect=[None, "Jugador 2"])

        mock_input.side_effect = [
            "",   # tirar dados primer turno
            "s",  # continuar al siguiente turno
            ""    # tirar dados segundo turno (gana)
        ]

        with patch('cli.cli.Game', return_value=self.juego):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                ejecutar_cli()

        output = fake_out.getvalue()
        self.assertIn("Jugador 2 ha ganado el juego", output)
    @patch('builtins.input')
    def test_ejecutar_cli_index_error_en_seleccion(self, mock_input):
        """Cubre el caso donde se elige una ficha fuera del rango disponible."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = [2]
        self.juego.verificar_ganador = MagicMock(return_value=None)

        mock_input.side_effect = ["", "99", "n"]

        with patch('cli.cli.Game', return_value=self.juego):
            with patch('cli.cli.fichas_movibles', return_value=[(MagicMock(_position_=0), [2])]):
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    ejecutar_cli()

        output = fake_out.getvalue()
        self.assertIn("Entrada invalida", output)

    @patch('builtins.input')
    def test_ejecutar_cli_sin_ganador_y_salida_manual(self, mock_input):
        """Cubre el caso donde no hay ganador y el jugador decide salir."""
        self.juego.tirar_dados = MagicMock()
        self.juego.available_moves = []
        self.juego.verificar_ganador = MagicMock(return_value=None)

        mock_input.side_effect = ["", "n"]

        with patch('cli.cli.Game', return_value=self.juego):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                ejecutar_cli()

        output = fake_out.getvalue()
        self.assertIn("Fin del juego", output)
    def test_tablero_view_con_fichas_en_todos_los_segmentos(self):
        """Cubre puntos, barra y borneadas con fichas visibles."""
        mock_blanca = MagicMock(_color_="blanco")
        mock_negra = MagicMock(_color_="negro")

        # Puntos con fichas
        self.juego.board._puntos_[12] = [mock_blanca] * 3
        self.juego.board._puntos_[18] = [mock_negra] * 2

        # Barra con fichas
        self.juego.fichas_en_barra = MagicMock(return_value=[mock_blanca, mock_negra])

        # Fichas borneadas
        self.juego.fichas_borneadas = MagicMock(side_effect=lambda color: [mock_blanca]*2 if color=="blanco" else [mock_negra]*1)

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.tablero_view.mostrar(self.juego)
            output = fake_out.getvalue()
            self.assertIn("Estado del tablero", output)
            self.assertIn("Fichas borneadas", output)
            self.assertIn("BARRA", output)
            self.assertIn("2", output)  # borneadas blancas
            self.assertIn("1", output)  # borneadas negras

if __name__ == '__main__':
    unittest.main()
