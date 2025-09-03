historial_de_jugadas = []

def registrar_jugada(jugador, origen, destino, captura=False):
    jugada = {
        "jugador": jugador,
        "origen": origen,
        "destino": destino,
        "captura": captura
    }
    historial_de_jugadas.append(jugada)