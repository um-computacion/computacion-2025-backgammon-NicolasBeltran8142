class Checker:
    def __init__(self, color, position):
        self._color_ = color
        self._position_ = position
def validar_movimiento(tablero, jugador, origen, destino, valor_dado):
    if not (0 <= origen < len(tablero)) or not (0 <= destino < len(tablero)):
        return False

    punto_origen = tablero[origen]
    punto_destino = tablero[destino]

    if punto_origen._jugador_ != jugador or punto_origen._cantidad_ == 0:
        return False

    distancia = abs(destino - origen)
    if distancia != valor_dado:
        return False

    if punto_destino._jugador_ not in [None, jugador] and punto_destino._cantidad_ > 1:
        return False

    if jugador == "Jugador1" and destino < origen:
        return False
    if jugador == "Jugador2" and destino > origen:
        return False

    return True
class Punto:
    def __init__(self, jugador=None, cantidad=0):
        self._jugador_ = jugador
        self._cantidad_ = cantidad