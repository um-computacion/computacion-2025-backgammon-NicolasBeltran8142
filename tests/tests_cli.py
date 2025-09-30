import unittest
from unittest.mock import patch
from io import StringIO
from core.game import Game
from cli.cli import mostrar_tablero, mostrar_estado

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    # 📦 Tablero
    def test_mostrar_tablero_imprime_24_puntos(self):
        with patch('sys.stdout', new=StringIO()) as salida:
            mostrar_tablero(self.game)
            output = salida.getvalue()
            self.assertIn("Punto  0:", output)
            self.assertIn("Punto 23:", output)
            self.assertEqual(output.count("Punto"), 24)

    # 🔁 Estado del juego
    def test_mostrar_estado_imprime_datos_del_jugador(self):
        self.game.tirar_dados()
        with patch('sys.stdout', new=StringIO()) as salida:
            mostrar_estado(self.game)
            output = salida.getvalue()
            self.assertIn("Turno de:", output)
            self.assertIn("Fichas en barra:", output)
            self.assertIn("Fichas borneadas:", output)
            self.assertIn("Movimientos disponibles:", output)

    # 🎲 Simulación de entrada
    @patch('builtins.input', side_effect=["", "0", "s"])
    def test_ejecucion_basica_del_cli(self, mock_input):
        from cli.cli import ejecutar_cli
        # Forzamos un movimiento simple
        self.game.available_moves = [1]
        ficha = self.game.fichas_en_punto(0, "blanco")[0]
        ficha._position_ = 0
        self.game.board._puntos_[1] = []
        with patch('sys.stdout', new=StringIO()) as salida:
            with patch('core.game.Game', return_value=self.game):
                ejecutar_cli()
                output = salida.getvalue()
                self.assertIn("Bienvenido a Backgammon CLI", output)
                self.assertIn("Movimiento exitoso", output)

    # 🧠 Validación de flujo
    def test_estado_inicial_del_juego_en_cli(self):
        with patch('sys.stdout', new=StringIO()) as salida:
            mostrar_estado(self.game)
            output = salida.getvalue()
            self.assertIn("Jugador 1", output)
            self.assertIn("blanco", output)

if __name__ == "__main__":
    unittest.main()
