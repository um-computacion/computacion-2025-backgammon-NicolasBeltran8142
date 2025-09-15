import unittest
from core.player import Jugador

class TestJugador(unittest.TestCase):
    def setUp(self):
        self.jugador = Jugador("Jugador 1", "blanco")

    def test_creacion_jugador(self):
        self.assertEqual(self.jugador.nombre, "Jugador 1")
        self.assertEqual(self.jugador.color, "blanco")
        self.assertEqual(self.jugador.puntos, 0)
        self.assertEqual(self.jugador.fichas_fuera, 0)

    def test_sumar_puntos(self):
        self.jugador.sumar_puntos(5)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3)
        self.assertEqual(self.jugador.puntos, 8)

    def test_sacar_ficha(self):
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 1)
        for _ in range(4):
            self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 5)

    def test_ha_ganado_false(self):
        self.assertFalse(self.jugador.ha_ganado())
        for _ in range(14):
            self.jugador.sacar_ficha()
        self.assertFalse(self.jugador.ha_ganado())

    def test_ha_ganado_true(self):
        for _ in range(15):
            self.jugador.sacar_ficha()
        self.assertTrue(self.jugador.ha_ganado())

if __name__ == "__main__":
    unittest.main()
