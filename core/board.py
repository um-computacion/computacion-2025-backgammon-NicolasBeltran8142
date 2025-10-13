from core.checker import Checker

class Board:
    def __init__(self):
        self._puntos_ = [[] for _ in range(24)]
        self.historial_de_jugadas = []

    def inicializar_fichas(self):
        posiciones = {
            "blanco": {0: 2, 11: 5, 16: 3, 18: 5},
            "negro": {23: 2, 12: 5, 7: 3, 5: 5}
        }
        for color, puntos in posiciones.items():
            for punto, cantidad in puntos.items():
                for _ in range(cantidad):
                    self._puntos_[punto].append(Checker(color, punto))

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

        captura = False
        if punto_destino and punto_destino[-1]._color_ != color and len(punto_destino) == 1:
            punto_destino.pop()
            captura = True

        ficha._position_ = destino
        punto_origen.pop()
        punto_destino.append(ficha)

        self.registrar_jugada(color, origen, destino, captura)

    def eliminar_ficha_si_unica(self, punto, color):
        if not (0 <= punto < 24):
            raise ValueError("El punto debe estar entre 0 y 23")

        casilla = self._puntos_[punto]
        if len(casilla) == 1 and casilla[0]._color_ == color:
            ficha = casilla.pop()
            return ficha
        else:
            raise ValueError("No se puede eliminar la ficha: condiciones inválidas")

    def puede_entrar_desde_bar(self, color, entrada):
        punto = self._puntos_[entrada]
        return not punto or punto[-1]._color_ == color or len(punto) < 2

    def intentar_reingreso(self, color):
        entradas = range(0, 6) if color == "blanco" else range(18, 24)
        for entrada in entradas:
            if self.puede_entrar_desde_bar(color, entrada):
                self._puntos_[entrada].append(Checker(color, entrada))
                print(f"{color} reingresa en el punto {entrada}")
                return entrada
        print(f"{color} no puede reingresar: todos los puntos están bloqueados.")
        return None

    def registrar_jugada(self, jugador, origen, destino, captura=False):
        jugada = {
            "jugador": jugador,
            "origen": origen,
            "destino": destino,
            "captura": captura
        }
        self.historial_de_jugadas.append(jugada)

    def mostrar_historial(self):
        print("\nHistorial de jugadas:")
        for j in self.historial_de_jugadas:
            texto = f"{j['jugador']} movió de {j['origen']} a {j['destino']}"
            if j["captura"]:
                texto += " (captura)"
            print(texto)

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
