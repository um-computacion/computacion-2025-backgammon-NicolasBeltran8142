from core.checker import Checker

class Board:
    
    def __init__(self):
        self._puntos_ = [[] for _ in range(24)]

    def inicializar_fichas(self):
        # Blancas
        for _ in range(2):
            self._puntos_[0].append(Checker("blanco", 0))
        for _ in range(5):
            self._puntos_[11].append(Checker("blanco", 11))
        for _ in range(3):
            self._puntos_[16].append(Checker("blanco", 16))
        for _ in range(5):
            self._puntos_[18].append(Checker("blanco", 18))

        # Negras
        for _ in range(2):
            self._puntos_[23].append(Checker("negro", 23))
        for _ in range(5):
            self._puntos_[12].append(Checker("negro", 12))
        for _ in range(3):
            self._puntos_[7].append(Checker("negro", 7))
        for _ in range(5):
            self._puntos_[5].append(Checker("negro", 5))
    def mostrar_tablero(self):
        print("\nEstado del tablero:")
        for i, punto in enumerate(self.puntos):
            contenido = "".join(["B" if f.color == "blanco" else "N" for f in punto])
            print(f"Punto {i:2}: {contenido if contenido else '.'}")

    def mover_ficha(self, origen, destino, color):
        if not (0 <= origen < 24 and 0 <= destino < 24):
            raise ValueError("Los puntos deben estar entre 0 y 23")

        punto_origen = self._puntos_[origen]
        punto_destino = self._puntos_[destino]

        if not punto_origen:
            raise ValueError(f"No hay fichas en el punto {origen}")

        ficha = punto_origen[-1]
        if ficha._color_ != color:
            raise ValueError(f"La ficha en el punto {origen} no es del color {color}")

        if punto_destino and punto_destino[-1]._color_ != color:
            raise ValueError(f"No se puede mover al punto {destino}, ocupado por el oponente")

        ficha._position_ = destino
        punto_origen.pop()
        punto_destino.append(ficha)
    def mostrar_tablero(self):
        print("\nBienvenido a Backgammon Compucation 2025\n")

        print("ZONA SUPERIOR (13 → 24):")
        print(" ".join([f"{i:2}" for i in range(12, 24)]))
        print(" ".join([
            "".join(["B" if f._color_ == "blanco" else "N" for f in self._puntos_[i]]) if self._puntos_[i] else "--"
            for i in range(12, 24)
        ]))

        print("\n" + "-" * 50 + "\n")

        print("ZONA INFERIOR (12 → 1):")
        print(" ".join([f"{i:2}" for i in reversed(range(12))]))
        print(" ".join([
            "".join(["B" if f._color_ == "blanco" else "N" for f in self._puntos_[i]]) if self._puntos_[i] else "--"
            for i in reversed(range(12))
        ]))
    def eliminar_ficha_si_unica(self, punto, color):
        if not (0 <= punto < 24):
            raise ValueError("El punto debe estar entre 0 y 23")

        casilla = self._puntos_[punto]
        if len(casilla) == 1 and casilla[0]._color_ == color:
            ficha = casilla.pop()
            print(f"Se eliminó una ficha {color} del punto {punto}")
            return ficha
        else:
            raise ValueError(f"No se puede eliminar la ficha del punto {punto}: está vacío, hay múltiples fichas o el color no coincide")
    def puede_entrar_desde_bar(self, color, entrada):
        punto = self._puntos_[entrada]
        if not punto:
            return True
        return punto[-1]._color_ == color or len(punto) < 2
    def intentar_reingreso(self, color):
        entradas = range(0, 6) if color == "blanco" else range(18, 24)

        for entrada in entradas:
            if self.puede_entrar_desde_bar(color, entrada):
                self._puntos_[entrada].append(Checker(color, entrada))
                print(f"{color} reenters at point {entrada}")
                return True

        print(f"{color} No se puede volver a entrar: todos los puntos de entrada están bloqueados. Se perdió el turno.")
        return False



 
historial_de_jugadas = []
       
def registrar_jugada(jugador, origen, destino, captura=False):
    jugada = {
        "jugador": jugador,
        "origen": origen,
        "destino": destino,
        "captura": captura
    }
    historial_de_jugadas.append(jugada)