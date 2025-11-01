# Corregime los tests de Board porque no llego a la covertura

from core.checker import Checker


class Board:
    """
    Represents the Backgammon board, composed of 24 numbered points (0 to 23).
    Each point can hold a stack of checkers belonging to a player.

    Attributes:
        _puntos_ (list): A list of 24 slots, each containing a stack of checkers.
        historial_de_jugadas (list): A record of all moves made during the game.
        fichas (list): A list of all 30 checkers.
    """

    def __init__(self):
        """
        Initializes the board with 24 empty points and an empty move history.
        """
        self._puntos_ = [[] for _ in range(24)]
        self.historial_de_jugadas = []
        self.fichas = []

    def inicializar_fichas(self):
        """
        Places the initial checkers on the board according to standard setup.
        """
        self.fichas = []
        posiciones = {
            "negro": {23: 2, 12: 5, 7: 3, 5: 5},
            "blanco": {0: 2, 11: 5, 16: 3, 18: 5},
        }
        for color, puntos in posiciones.items():
            for punto, cantidad in puntos.items():
                for _ in range(cantidad):
                    checker = Checker(color, punto)
                    self._puntos_[punto].append(checker)
                    self.fichas.append(checker)

    def mover_ficha(self, origen, destino, color):
        """
        Moves a checker from the origin point to the destination, validating basic rules.

        Args:
            origen (int): Index of the origin point (0–23).
            destino (int): Index of the destination point (0–23).
            color (str): Color of the player making the move ("blanco" or "negro").

        Raises:
            ValueError: If the move is invalid due to range, color mismatch, or blocked destination.
        """
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise ValueError("Points must be between 0 and 23")

        punto_origen = self._puntos_[origen]
        punto_destino = self._puntos_[destino]

        if not punto_origen:
            raise ValueError(f"No checkers at point {origen}")

        ficha = punto_origen[-1]
        if ficha._color_ != color:
            raise ValueError(
                f"The checker at point {origen} does not match color {color}"
            )

        captura = False
        if (
            punto_destino
            and punto_destino[-1]._color_ != color
            and len(punto_destino) == 1
        ):
            punto_destino.pop()
            captura = True

        ficha._position_ = destino
        punto_origen.pop()
        punto_destino.append(ficha)

        self.registrar_jugada(color, origen, destino, captura)

    def eliminar_ficha_si_unica(self, punto, color):
        """
        Removes a checker from the point if it's the only one and matches the given color.

        Args:
            punto (int): Index of the point (0–23).
            color (str): Player color.

        Returns:
            Checker: The removed checker.

        Raises:
            ValueError: If the point is out of range or conditions are not met.
        """
        if not (0 <= punto < 24):
            raise ValueError("Point must be between 0 and 23")

        casilla = self._puntos_[punto]
        if len(casilla) == 1 and casilla[0]._color_ == color:
            ficha = casilla.pop()
            return ficha
        else:
            raise ValueError("Cannot remove checker: invalid conditions")

    def puede_entrar_desde_bar(self, color, entrada):
        """
        Checks if a checker can re-enter from the bar to the specified point.

        Args:
            color (str): Player color.
            entrada (int): Entry point (0–5 for blanco, 18–23 for negro).

        Returns:
            bool: True if entry is allowed, False if blocked.
        """
        punto = self._puntos_[entrada]
        return not punto or punto[-1]._color_ == color or len(punto) < 2

    def intentar_reingreso(self, color):
        """
        Attempts to re-enter a checker from the bar onto the board.

        Args:
            color (str): Player color.

        Returns:
            int or None: Entry point if successful, None if all are blocked.
        """
        entradas = range(0, 6) if color == "blanco" else range(18, 24)
        for entrada in entradas:
            if self.puede_entrar_desde_bar(color, entrada):
                self._puntos_[entrada].append(Checker(color, entrada))
                print(f"{color} re-enters at point {entrada}")
                return entrada
        print(f"{color} cannot re-enter: all points are blocked.")
        return None

    def registrar_jugada(self, jugador, origen, destino, captura=False):
        """
        Records a move in the game history.

        Args:
            jugador (str): Player color.
            origen (int): Origin point.
            destino (int): Destination point.
            captura (bool): Whether a capture occurred.
        """
        jugada = {
            "jugador": jugador,
            "origen": origen,
            "destino": destino,
            "captura": captura,
        }
        self.historial_de_jugadas.append(jugada)

    def mostrar_historial(self):
        """
        Prints the history of moves made during the game.
        """
        print("\nMove history:")
        for j in self.historial_de_jugadas:
            texto = f"{j['jugador']} moved from {j['origen']} to {j['destino']}"
            if j["captura"]:
                texto += " (capture)"
            print(texto)

    def mostrar_tablero(self):
        """
        Prints the current state of the board in a visual format.
        """
        print("\nWelcome to Backgammon Compucation 2025\n")

        print("TOP ZONE (13 → 24):")
        print(" ".join([f"{i:2}" for i in range(12, 24)]))
        print(
            " ".join(
                [
                    (
                        "".join(
                            [
                                "B" if f._color_ == "blanco" else "N"
                                for f in self._puntos_[i]
                            ]
                        )
                        if self._puntos_[i]
                        else "--"
                    )
                    for i in range(12, 24)
                ]
            )
        )

        print("\n" + "-" * 50 + "\n")

        print("BOTTOM ZONE (12 → 1):")
        print(" ".join([f"{i:2}" for i in reversed(range(12))]))
        print(
            " ".join(
                [
                    (
                        "".join(
                            [
                                "B" if f._color_ == "blanco" else "N"
                                for f in self._puntos_[i]
                            ]
                        )
                        if self._puntos_[i]
                        else "--"
                    )
                    for i in reversed(range(12))
                ]
            )
        )

# Corregime los tests de Checker porque no llego a la covertura

import unittest
from core.checker import Checker, Punto, validar_movimiento


class TestChecker(unittest.TestCase):
    def test_init(self):
        checker = Checker("blanco", 1)
        self.assertEqual(checker.color, "blanco")
        self.assertEqual(checker.posicion, 1)

    def test_init_invalid_position(self):
        with self.assertRaises(ValueError):
            Checker("blanco", 24)

    def test_mover_a(self):
        checker = Checker("blanco", 1)
        checker.mover_a(2)
        self.assertEqual(checker.posicion, 2)

    def test_mover_a_invalid_position(self):
        checker = Checker("blanco", 1)
        with self.assertRaises(ValueError):
            checker.mover_a(24)

    def test_repr(self):
        checker = Checker("blanco", 1)
        self.assertEqual(repr(checker), "Checker(blanco, 1)")

    def test_eq(self):
        checker1 = Checker("blanco", 1)
        checker2 = Checker("blanco", 1)
        self.assertEqual(checker1, checker2)

    def test_hash(self):
        checker1 = Checker("blanco", 1)
        checker2 = Checker("blanco", 1)
        self.assertEqual(hash(checker1), hash(checker2))


class TestPunto(unittest.TestCase):
    def test_esta_vacio(self):
        punto = Punto()
        self.assertTrue(punto.esta_vacio())

    def test_es_del_jugador(self):
        punto = Punto("Jugador1", 1)
        self.assertTrue(punto.es_del_jugador("Jugador1"))

    def test_es_del_oponente(self):
        punto = Punto("Jugador2", 1)
        self.assertTrue(punto.es_del_oponente("Jugador1"))

    def test_esta_bloqueado(self):
        punto = Punto("Jugador2", 2)
        self.assertTrue(punto.esta_bloqueado("Jugador1"))


class TestValidacion(unittest.TestCase):

    def test_valido_sin_obstaculos_en_rango_correcto(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[8] = Punto(None, 0)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_valido_con_captura_de_oponente(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador2", 1)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_dado_incorrecto(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[9] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 9, 3))

    def test_invalido_por_punto_bloqueado(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[8] = Punto("Jugador2", 2)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_direccion_contraria(self):
        tablero = [Punto() for _ in range(24)]
        tablero[8] = Punto("Jugador1", 1)
        tablero[5] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 8, 5, 3))

    def test_fuera_de_rango_origen(self):
        tablero = [Punto() for _ in range(24)]
        self.assertFalse(validar_movimiento(tablero, "Jugador1", -1, 5, 3))

    def test_fuera_de_rango_destino(self):
        tablero = [Punto() for _ in range(24)]
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 24, 3))

    def test_sin_fichas_en_origen(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto(None, 0)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_color_incorrecto_en_origen(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador2", 1)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_valido_a_punto_propio(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador1", 2)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_doble_ficha_oponente(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador2", 2)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_invalido_por_direccion_contraria_jugador2(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador2", 1)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador2", 5, 8, 3))

# Corregime los tests de Cli porque no llego a la covertura

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

# Corregime los tests de Dados porque no llego a la covertura

import unittest
from core.dados import Dice


class TestDice(unittest.TestCase):
    """Pruebas unitarias para la clase Dice (dados del juego)."""

    def test_roll_dice_returns_valid_values(self):
        """Verifica que al tirar los dados se obtengan valores entre 1 y 6."""
        dice = Dice()
        val1, val2 = dice.roll_dice()
        self.assertIn(val1, range(1, 7))
        self.assertIn(val2, range(1, 7))

    def test_get_values_reflects_last_roll(self):
        """Verifica que get_values devuelva el último resultado de los dados."""
        dice = Dice()
        rolled = dice.roll_dice()
        self.assertEqual(dice.get_values(), rolled)

    def test_is_double_true(self):
        """Verifica que is_double devuelva True cuando ambos dados son iguales."""
        dice = Dice()
        dice.set_values_for_test(4, 4)
        self.assertTrue(dice.is_double())

    def test_is_double_false(self):
        """Verifica que is_double devuelva False cuando los dados son distintos."""
        dice = Dice()
        dice.set_values_for_test(3, 5)
        self.assertFalse(dice.is_double())

    def test_set_values_for_test_sets_correctly(self):
        """Verifica que set_values_for_test asigne correctamente los valores."""
        dice = Dice()
        dice.set_values_for_test(2, 6)
        self.assertEqual(dice.get_values(), (2, 6))

    def test_get_moves_for_double(self):
        """Verifica que get_moves devuelva cuatro movimientos si hay doble."""
        dice = Dice()
        dice.set_values_for_test(5, 5)
        self.assertEqual(dice.get_moves(), [5, 5, 5, 5])

    def test_get_moves_for_non_double(self):
        """Verifica que get_moves devuelva dos movimientos si no hay doble."""
        dice = Dice()
        dice.set_values_for_test(2, 4)
        self.assertEqual(dice.get_moves(), [2, 4])

    def test_set_values_for_test_invalid_values(self):
        """Verifica que set_values_for_test lance error con valores inválidos."""
        dice = Dice()
        with self.assertRaises(ValueError):
            dice.set_values_for_test(0, 5)
        with self.assertRaises(ValueError):
            dice.set_values_for_test(7, 5)

# Corregime los tests de Game porque no llego a la covertura

import unittest
from unittest.mock import patch
from io import StringIO
from core.game import Game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    # Turnos
    def test_jugador_actual_es_jugador1_al_inicio(self):
        jugador = self.game.jugador_actual()
        self.assertEqual(jugador.nombre, "Jugador 1")
        self.assertEqual(jugador.color, "blanco")

    def test_cambiar_turno_alterna_entre_jugadores(self):
        jugador1 = self.game.jugador_actual()
        self.game.cambiar_turno()
        jugador2 = self.game.jugador_actual()
        self.assertNotEqual(jugador1, jugador2)
        self.assertEqual(jugador2.color, "negro")

    # Dados
    def test_tirar_dados_actualiza_last_roll_y_available_moves(self):
        resultado = self.game.tirar_dados()
        self.assertEqual(self.game.last_roll, resultado)
        self.assertTrue(len(self.game.available_moves) in [2, 4])

    # Estado inicial
    def test_fichas_en_barra_vacia_al_inicio(self):
        self.assertEqual(len(self.game.fichas_en_barra("blanco")), 0)
        self.assertEqual(len(self.game.fichas_en_barra("negro")), 0)

    def test_fichas_borneadas_vacias_al_inicio(self):
        self.assertEqual(len(self.game.fichas_borneadas("blanco")), 0)
        self.assertEqual(len(self.game.fichas_borneadas("negro")), 0)

    # Movimiento válido
    def test_mover_ficha_valido_actualiza_posicion_y_tablero(self):
        origen = 18
        destino = 17
        self.game.available_moves = [1]
        resultado = self.game.mover_ficha(origen, destino, "blanco")
        self.assertTrue(resultado)
        self.assertEqual(len(self.game.fichas_en_punto(origen, "blanco")), 4)
        self.assertEqual(len(self.game.fichas_en_punto(destino, "blanco")), 1)

    # Movimiento inválido
    def test_mover_ficha_invalido_sin_ficha_en_origen(self):
        self.game.available_moves = [1]
        resultado = self.game.mover_ficha(10, 11, "blanco")
        self.assertFalse(resultado)

    def test_mover_ficha_invalida_por_puede_mover_false(self):
        self.game.available_moves = [3]
        resultado = self.game.mover_ficha(5, 1, "blanco")
        self.assertFalse(resultado)

    # Validación de movimiento
    def test_puede_mover_valido(self):
        self.game.available_moves = [1]
        self.assertTrue(self.game.puede_mover(18, 17, "blanco"))

    def test_puede_mover_invalido_fuera_de_rango(self):
        self.game.available_moves = [1]
        self.assertFalse(self.game.puede_mover(0, -1, "blanco"))

    def test_puede_mover_falla_si_hay_fichas_en_barra_y_origen_distinto(self):
        self.game.jugador1.fichas[0]._position_ = "bar"
        self.assertFalse(self.game.puede_mover(18, 17, "blanco"))

    def test_puede_mover_falla_si_destino_ocupado_por_2_o_mas_rivales(self):
        self.game.available_moves = [1]
        origen = 11
        destino = 10
        negras = self.game.fichas_en_punto(5, "negro")[:2]
        self.game.board._puntos_[5] = self.game.board._puntos_[5][2:]
        for f in negras:
            f._position_ = destino
        self.game.board._puntos_[destino] = negras
        self.assertFalse(self.game.puede_mover(origen, destino, "blanco"))

    # Captura
    def test_mover_ficha_con_captura_envia_rival_a_barra(self):
        origen = 18
        destino = 17
        ficha_negra = self.game.fichas_en_punto(5, "negro")[0]
        self.game.board._puntos_[5].pop(0)
        ficha_negra._position_ = destino
        self.game.board._puntos_[destino] = [ficha_negra]
        self.game.available_moves = [1]
        self.game.last_roll = (1, 2)
        resultado = self.game.mover_ficha(origen, destino, "blanco")
        self.assertTrue(resultado)
        self.assertEqual(ficha_negra._position_, "bar")
        self.assertEqual(len(self.game.fichas_en_punto(destino, "blanco")), 1)

    # Historial
    def test_historial_se_actualiza_correctamente(self):
        origen = 18
        destino = 17
        self.game.available_moves = [1]
        self.game.last_roll = (1, 2)
        self.game.mover_ficha(origen, destino, "blanco")
        ultimo = self.game.historial[-1]
        self.assertEqual(ultimo["jugador"], "blanco")
        self.assertEqual(ultimo["origen"], origen)
        self.assertEqual(ultimo["destino"], destino)
        self.assertEqual(ultimo["dados"], (1, 2))

    def test_puede_mover_falla_si_no_puede_sacar_fichas(self):
        self.game.jugador1.fichas[0]._position_ = 10  # Not in home board
        self.game.available_moves = [1]
        self.assertFalse(self.game.puede_mover(18, "off", "blanco"))

    def test_calcular_distancia(self):
        # White
        self.assertEqual(self.game._calcular_distancia("bar", 23, "blanco"), 1)
        self.assertEqual(self.game._calcular_distancia(23, "off", "blanco"), 1)
        # Black
        self.assertEqual(self.game._calcular_distancia("bar", 0, "negro"), 1)
        self.assertEqual(self.game._calcular_distancia(0, "off", "negro"), 1)
        # Normal
        self.assertEqual(self.game._calcular_distancia(10, 15, "blanco"), 5)

    # Simulación de turno
    def test_simular_turno_completo_con_movimiento_valido(self):
        self.game.tirar_dados()
        jugador = self.game.jugador_actual()
        origenes = self.game.puntos_validos_de_origen(jugador.color)
        for move in self.game.available_moves:
            for origen in origenes:
                destino = origen - move if jugador.color == "blanco" else origen + move
                if self.game.puede_mover(origen, destino, jugador.color):
                    resultado = self.game.mover_ficha(origen, destino, jugador.color)
                    self.assertTrue(resultado)
                    return

    def test_puntos_validos_de_origen_devuelve_puntos_con_fichas(self):
        puntos = self.game.puntos_validos_de_origen("blanco")
        self.assertTrue(all(isinstance(p, int) for p in puntos))
        self.assertGreater(len(puntos), 0)

    # Victoria
    def test_verificar_ganador_none_al_inicio(self):
        self.assertIsNone(self.game.verificar_ganador())

    def test_verificar_ganador_funciona_si_jugador1_gana(self):
        for ficha in self.game.jugador1.fichas:
            ficha._position_ = "off"
        self.assertEqual(self.game.verificar_ganador(), "Jugador 1")

    def test_verificar_ganador_funciona_si_jugador2_gana(self):
        for ficha in self.game.jugador2.fichas:
            ficha._position_ = "off"
        self.assertEqual(self.game.verificar_ganador(), "Jugador 2")

    @patch("sys.stdout", new_callable=StringIO)
    def test_mostrar_estado(self, mock_stdout):
        self.game.last_roll = (5, 6)
        self.game.available_moves = [5, 6]
        self.game.mostrar_estado()
        output = mock_stdout.getvalue()
        self.assertIn("Turno: Jugador 1 (blanco)", output)
        self.assertIn("Última tirada: (5, 6)", output)
        self.assertIn("Movimientos disponibles: [5, 6]", output)

# Corregime los tests de Player porque no llego a la covertura

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
        self.jugador.sumar_puntos(5)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3)
        self.assertEqual(self.jugador.puntos, 8)

    def test_sacar_ficha_incrementa_fichas_fuera(self):
        """Verifica que sacar fichas aumente el contador de fichas fuera."""
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 1)
        for _ in range(4):
            self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 5)

    def test_ha_ganado_devuelve_false_si_faltan_fichas(self):
        """Verifica que no se declare victoria si faltan fichas fuera."""
        self.assertFalse(self.jugador.ha_ganado())
        for _ in range(14):
            self.jugador.sacar_ficha()
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
        self.jugador_a = Jugador("A", "white")
        self.jugador_b = Jugador("B", "black")
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
        self.assertIn("Turno: A (white)", mock_stdout.getvalue())
        self.tm.siguiente_turno()
        mock_stdout.seek(0)
        mock_stdout.truncate(0)
        self.tm.mostrar_turno()
        self.assertIn("Turno: B (black)", mock_stdout.getvalue())
