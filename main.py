from core.dados import Dice

def main():
    dice = Dice()
    values = dice.roll_dice()
    print(f"Tirada: {values}")
    print(f"¿Es doble? {dice.is_double()}")

if __name__ == "__main__":
    main()
