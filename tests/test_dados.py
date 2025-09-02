import pytest
from core.dice import Dice

def test_roll_dice_returns_two_values():
    dice = Dice()
    values = dice.roll_dice()
    assert len(values) == 2
    assert all(1 <= v <= 6 for v in values)

def test_get_values_after_roll():
    dice = Dice()
    dice.roll_dice()
    values = dice.get_values()
    assert len(values) == 2
    assert all(1 <= v <= 6 for v in values)

def test_is_double_true():
    dice = Dice()
    dice._Dice__values__ = (3, 3)  # Forzamos tirada
    assert dice.is_double() is True

def test_is_double_false():
    dice = Dice()
    dice._Dice__values__ = (2, 5)  # Forzamos tirada
    assert dice.is_double() is False
