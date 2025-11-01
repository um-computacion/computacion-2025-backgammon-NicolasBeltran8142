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
