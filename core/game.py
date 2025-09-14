from core.checker import validar_movimiento

if validar_movimiento(tablero, jugador, origen, destino, valor_dado):
    mover_ficha(tablero, origen, destino)
else:
    print("Movimiento inválido")
