import unittest
from core.player import Jugador, TurnManager


class TestJugador(unittest.TestCase):

    def setUp(self):
        self.jugador = Jugador("Jugador 1", "blanco")

    # Creación y atributos
    def test_jugador_se_inicializa_correctamente(self):
        self.assertEqual(self.jugador.nombre, "Jugador 1")
        self.assertEqual(self.jugador.color, "blanco")
        self.assertEqual(self.jugador.puntos, 0)
        self.assertEqual(self.jugador.fichas_fuera, 0)

    # Puntos
    def test_sumar_puntos_incrementa_correctamente(self):
        self.jugador.sumar_puntos(5)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3)
        self.assertEqual(self.jugador.puntos, 8)

    # Fichas fuera
    def test_sacar_ficha_incrementa_fichas_fuera(self):
        self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 1)
        for _ in range(4):
            self.jugador.sacar_ficha()
        self.assertEqual(self.jugador.fichas_fuera, 5)

    # Victoria
    def test_ha_ganado_devuelve_false_si_faltan_fichas(self):
        self.assertFalse(self.jugador.ha_ganado())
        for _ in range(14):
            self.jugador.sacar_ficha()
        self.assertFalse(self.jugador.ha_ganado())

    def test_ha_ganado_devuelve_true_si_tiene_15_fichas_fuera(self):
        for ficha in self.jugador.fichas:
            ficha._position_ = "off"
        self.assertTrue(self.jugador.ha_ganado())


class TestTurnManager(unittest.TestCase):

    def test_alternancia_de_turnos_funciona_correctamente(self):
        tm = TurnManager(Jugador("A", "white"), Jugador("B", "black"))
        self.assertEqual(tm.jugador_actual().nombre, "A")
        tm.siguiente_turno()
        self.assertEqual(tm.jugador_actual().nombre, "B")
        tm.siguiente_turno()
        self.assertEqual(tm.jugador_actual().nombre, "A")
