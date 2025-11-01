import unittest
from core.checker import Checker, Punto, validar_movimiento


class TestChecker(unittest.TestCase):
    """
    Pruebas unitarias para la clase Checker.
    Verifica la inicializacion, movimiento, representacion y comparacion de fichas.
    """

    def test_init(self):
        """Verifica que una ficha se inicialice correctamente con color y posicion."""
        checker = Checker("blanco", 1)
        self.assertEqual(checker.color, "blanco")
        self.assertEqual(checker.posicion, 1)

    def test_init_invalid_position(self):
        """Verifica que no se permita una posicion fuera del rango valido."""
        with self.assertRaises(ValueError):
            Checker("blanco", 24)

    def test_mover_a(self):
        """Verifica que una ficha se pueda mover a una nueva posicion valida."""
        checker = Checker("blanco", 1)
        checker.mover_a(2)
        self.assertEqual(checker.posicion, 2)

    def test_mover_a_invalid_position(self):
        """Verifica que no se permita mover a una posicion fuera del rango."""
        checker = Checker("blanco", 1)
        with self.assertRaises(ValueError):
            checker.mover_a(24)

    def test_repr(self):
        """Verifica la representacion en texto de una ficha."""
        checker = Checker("blanco", 1)
        self.assertEqual(repr(checker), "Checker(blanco, 1)")

    def test_eq(self):
        """Verifica que dos fichas iguales sean consideradas equivalentes."""
        checker1 = Checker("blanco", 1)
        checker2 = Checker("blanco", 1)
        self.assertEqual(checker1, checker2)

    def test_hash(self):
        """Verifica que dos fichas iguales tengan el mismo hash."""
        checker1 = Checker("blanco", 1)
        checker2 = Checker("blanco", 1)
        self.assertEqual(hash(checker1), hash(checker2))


class TestPunto(unittest.TestCase):
    """
    Pruebas unitarias para la clase Punto.
    Verifica el estado del punto y su relacion con los jugadores.
    """

    def test_esta_vacio(self):
        """Verifica que un punto sin fichas se considere vacio."""
        punto = Punto()
        self.assertTrue(punto.esta_vacio())

    def test_es_del_jugador(self):
        """Verifica que el punto pertenezca al jugador correcto."""
        punto = Punto("Jugador1", 1)
        self.assertTrue(punto.es_del_jugador("Jugador1"))

    def test_es_del_oponente(self):
        """Verifica que el punto pertenezca al oponente."""
        punto = Punto("Jugador2", 1)
        self.assertTrue(punto.es_del_oponente("Jugador1"))

    def test_esta_bloqueado(self):
        """Verifica que el punto este bloqueado para el jugador."""
        punto = Punto("Jugador2", 2)
        self.assertTrue(punto.esta_bloqueado("Jugador1"))


class TestValidacion(unittest.TestCase):
    """
    Pruebas unitarias para la funcion validar_movimiento.
    Verifica si un movimiento es valido segun las reglas del juego.
    """

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
        self.assertFalse(validar_movimiento([Punto() for _ in range(24)], "Jugador1", -1, 5, 3))

    def test_fuera_de_rango_destino(self):
        self.assertFalse(validar_movimiento([Punto() for _ in range(24)], "Jugador1", 5, 24, 3))

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
