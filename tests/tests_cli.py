import unittest
from core.player import Jugador, TurnManager


class TestJugador(unittest.TestCase):

    def setUp(self):
        self.jugador = Jugador("Jugador 1", "blanco")

    def test_jugador_se_inicializa_correctamente(self):
        self.assertEqual(self.jugador.nombre, "Jugador 1")
        self.assertEqual(self.jugador.color, "blanco")
        self.assertEqual(self.jugador.puntos, 0)
        self.assertEqual(self.jugador.fichas_fuera, 0)
        self.assertEqual(len(self.jugador.fichas), 15)

    def test_sumar_puntos_acumula_correctamente(self):
        self.jugador.sumar_puntos(5, verbose=False)
        self.assertEqual(self.jugador.puntos, 5)
        self.jugador.sumar_puntos(3, verbose=False)
        self.assertEqual(self.jugador.puntos, 8)

    def test_sacar_ficha_incrementa_contador(self):
        for i in range(5):
            self.jugador.sacar_ficha(verbose=False)
        self.assertEqual(self.jugador.fichas_fuera, 5)

    def test_ha_ganado_devuelve_false_si_faltan_fichas(self):
        for ficha in self.jugador.fichas[:10]:
            ficha._position_ = "off"
        self.assertFalse(self.jugador.ha_ganado())

    def test_ha_ganado_devuelve_true_si_todas_las_fichas_estan_off(self):
        for ficha in self.jugador.fichas:
            ficha._position_ = "off"
        self.assertTrue(self.jugador.ha_ganado())


class TestTurnManager(unittest.TestCase):

    def test_turno_alterna_correctamente_entre_jugadores(self):
        jugador_a = Jugador("A", "white")
        jugador_b = Jugador("B", "black")
        tm = TurnManager(jugador_a, jugador_b)

        self.assertEqual(tm.jugador_actual().nombre, "A")
        tm.siguiente_turno()
        self.assertEqual(tm.jugador_actual().nombre, "B")
        tm.siguiente_turno()
        self.assertEqual(tm.jugador_actual().nombre, "A")
