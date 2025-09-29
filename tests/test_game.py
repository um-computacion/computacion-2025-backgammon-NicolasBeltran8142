import unittest
from core.game import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

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

    def test_tirar_dados_actualiza_last_roll_y_available_moves(self):
        resultado = self.game.tirar_dados()
        self.assertEqual(self.game.last_roll, resultado)
        self.assertTrue(len(self.game.available_moves) in [2, 4])

    def test_fichas_en_barra_vacia_al_inicio(self):
        blanco_barra = self.game.fichas_en_barra("blanco")
        negro_barra = self.game.fichas_en_barra("negro")
        self.assertEqual(len(blanco_barra), 0)
        self.assertEqual(len(negro_barra), 0)

    def test_mover_ficha_valido_actualiza_posicion(self):
        # Forzamos una ficha blanca en punto 0 y destino libre en 1
        ficha = self.game.fichas_en_punto(0, "blanco")[0]
        origen = ficha._position_
        destino = origen + 1
        resultado = self.game.mover_ficha(origen, destino, "blanco")
        self.assertTrue(resultado)
        self.assertEqual(ficha._position_, destino)

    def test_mover_ficha_invalido_sin_ficha_en_origen(self):
        resultado = self.game.mover_ficha(10, 11, "blanco")  # No hay ficha blanca en 10
        self.assertFalse(resultado)

    def test_verificar_ganador_none_al_inicio(self):
        ganador = self.game.verificar_ganador()
        self.assertIsNone(ganador)

    def test_historial_se_actualiza_con_movimiento(self):
        ficha = self.game.fichas_en_punto(0, "blanco")[0]
        origen = ficha._position_
        destino = origen + 1
        self.game.mover_ficha(origen, destino, "blanco")
        self.assertIn(("blanco", origen, destino), self.game.historial)