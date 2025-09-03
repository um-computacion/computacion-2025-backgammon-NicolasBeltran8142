import unittest
from core.registro import registrar_jugada, historial_de_jugadas

class TestRegistro(unittest.TestCase):
    def test_registrar_jugada(self):
        historial_de_jugadas.clear()
        registrar_jugada("Jugador1", 5, 10)
        self.assertEqual(len(historial_de_jugadas), 1)
        self.assertEqual(historial_de_jugadas[0]["origen"], 5)