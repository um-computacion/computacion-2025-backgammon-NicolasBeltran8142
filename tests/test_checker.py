import unittest
from core.checker import validar_movimiento, Punto

class TestValidacion(unittest.TestCase):
    def test_movimiento_valido(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[8] = Punto(None, 0)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_movimiento_valido_con_captura(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 1)
        tablero[8] = Punto("Jugador2", 1)
        self.assertTrue(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_movimiento_invalido_por_dado(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[9] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 9, 3))

    def test_movimiento_invalido_por_bloqueo(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador1", 2)
        tablero[8] = Punto("Jugador2", 2)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_movimiento_invalido_por_direccion(self):
        tablero = [Punto() for _ in range(24)]
        tablero[8] = Punto("Jugador1", 1)
        tablero[5] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 8, 5, 3))

    def test_movimiento_fuera_de_rango_origen(self):
        tablero = [Punto() for _ in range(24)]
        resultado = validar_movimiento(tablero, "Jugador1", -1, 5, 3)
        self.assertFalse(resultado)

    def test_movimiento_fuera_de_rango_destino(self):
        tablero = [Punto() for _ in range(24)]
        resultado = validar_movimiento(tablero, "Jugador1", 5, 24, 3)
        self.assertFalse(resultado)

    def test_movimiento_sin_fichas_en_origen(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto(None, 0)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))

    def test_movimiento_con_color_incorrecto_en_origen(self):
        tablero = [Punto() for _ in range(24)]
        tablero[5] = Punto("Jugador2", 1)
        tablero[8] = Punto(None, 0)
        self.assertFalse(validar_movimiento(tablero, "Jugador1", 5, 8, 3))
