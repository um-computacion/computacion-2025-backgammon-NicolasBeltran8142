import unittest
from core.dados import Dice

class TestDice(unittest.TestCase):
    def test_roll_dice_returns_two_values(self):
        dice = Dice()
        values = dice.roll_dice()
        self.assertEqual(len(values), 2)
        self.assertTrue(all(1 <= v <= 6 for v in values))

    def test_get_values_after_roll(self):
        dice = Dice()
        dice.roll_dice()
        values = dice.get_values()
        self.assertEqual(len(values), 2)
        self.assertTrue(all(1 <= v <= 6 for v in values))

    def test_is_double_true(self):
        dice = Dice()
        dice._Dice__values__ = (3, 3)
        self.assertTrue(dice.is_double())

    def test_is_double_false(self):
        dice = Dice()
        dice.set_values_for_test(2, 5)
        self.assertFalse(dice.is_double())


if __name__ == "__main__":
    unittest.main()