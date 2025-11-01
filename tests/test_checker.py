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
