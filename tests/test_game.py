import unittest
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
        ficha = self.game.fichas_en_punto(0, "blanco")[0]
        origen = ficha._position_
        destino = origen + 1
        self.game.available_moves = [1]
        resultado = self.game.mover_ficha(origen, destino, "blanco")
        self.assertTrue(resultado)
        self.assertEqual(ficha._position_, destino)
        self.assertIn(ficha, self.game.board._puntos_[destino])

    # Movimiento inválido
    def test_mover_ficha_invalido_sin_ficha_en_origen(self):
        self.game.available_moves = [1]
        resultado = self.game.mover_ficha(10, 11, "blanco")
        self.assertFalse(resultado)

    def test_mover_ficha_invalida_por_puede_mover_false(self):
        self.game.available_moves = [3]
        resultado = self.game.mover_ficha(0, 10, "blanco")
        self.assertFalse(resultado)

    # Validación de movimiento
    def test_puede_mover_valido(self):
        self.game.available_moves = [1]
        self.assertTrue(self.game.puede_mover(0, 1, "blanco"))

    def test_puede_mover_invalido_fuera_de_rango(self):
        self.game.available_moves = [1]
        self.assertFalse(self.game.puede_mover(0, 24, "blanco"))

    def test_puede_mover_falla_si_hay_fichas_en_barra_y_origen_distinto(self):
        self.game.jugador1.fichas[0]._position_ = "bar"
        self.assertFalse(self.game.puede_mover(0, 5, "blanco"))

    def test_puede_mover_falla_si_destino_ocupado_por_2_o_mas_rivales(self):
        self.game.available_moves = [1]
        destino = 1
        negras = self.game.fichas_en_punto(5, "negro")[:2]
        for f in negras:
            f._position_ = destino
        self.game.board._puntos_[destino] = negras
        self.assertFalse(self.game.puede_mover(0, destino, "blanco"))

    # Captura
    def test_mover_ficha_con_captura_envia_rival_a_barra(self):
        ficha_blanca = self.game.fichas_en_punto(0, "blanco")[0]
        ficha_negra = self.game.fichas_en_punto(5, "negro")[0]
        ficha_negra._position_ = 1
        self.game.board._puntos_[1] = [ficha_negra]
        self.game.available_moves = [1]
        self.game.last_roll = (1, 2)
        resultado = self.game.mover_ficha(0, 1, "blanco")
        self.assertTrue(resultado)
        self.assertEqual(ficha_negra._position_, "bar")
        self.assertIn(ficha_blanca, self.game.board._puntos_[1])

    # Historial
    def test_historial_se_actualiza_correctamente(self):
        ficha = self.game.fichas_en_punto(0, "blanco")[0]
        origen = ficha._position_
        destino = origen + 1
        self.game.available_moves = [1]
        self.game.last_roll = (1, 2)
        self.game.mover_ficha(origen, destino, "blanco")
        ultimo = self.game.historial[-1]
        self.assertEqual(ultimo["jugador"], "blanco")
        self.assertEqual(ultimo["origen"], origen)
        self.assertEqual(ultimo["destino"], destino)
        self.assertEqual(ultimo["dados"], (1, 2))

    # Simulación de turno
    def test_simular_turno_completo_con_movimiento_valido(self):
        self.game.tirar_dados()
        jugador = self.game.jugador_actual()
        origenes = self.game.puntos_validos_de_origen(jugador.color)
        for move in self.game.available_moves:
            for origen in origenes:
                destino = origen + move
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
