import reglas
import piece
from reglas import validar_movimiento


def evaluar_tablero(tablero, color_jugador):
    """
    Evalúa el tablero y asigna un puntaje.
    Un puntaje positivo favorece al jugador actual, negativo al oponente.
    """
    puntaje = 0

    for fila in tablero:
        for casilla in fila:
            if isinstance(casilla, piece.Piece):
                if casilla.color == color_jugador:
                    puntaje += casilla.peso  # Suma el peso de las piezas del jugador actual
                else:
                    puntaje -= casilla.peso  # Resta el peso de las piezas del oponente

    return puntaje


def generar_movimientos(tablero, color_jugador):
    """
    Genera todos los movimientos válidos para un jugador.
    Ahora solo permite que los conejos se muevan una vez por turno.
    """
    movimientos = []

    for y in range(len(tablero)):
        for x in range(len(tablero[y])):
            casilla = tablero[y][x]
            if isinstance(casilla, piece.Piece) and casilla.color == color_jugador:
                if casilla.animal == "conejo":
                    continue  # No permite que el conejo se mueva si ya ha sido movido

                posiciones_disponibles = casilla.ObtenerPosicionesDisponibles(tablero)
                # Filtrar movimientos inválidos según las reglas
                posiciones_validas = [
                    pos for pos in posiciones_disponibles if validar_movimiento(tablero, (x, y), pos)
                ]
                for pos_final in posiciones_validas:
                    movimientos.append(((x, y), pos_final))

    return movimientos

def minimax(tablero, profundidad, alfa, beta, maximizando, color_jugador):
    """
    Algoritmo Minimax con poda alfa-beta, ahora con la restricción para los conejos.
    """
    if profundidad == 0:
        return evaluar_tablero(tablero, color_jugador), None

    color_oponente = "dorado" if color_jugador == "plateado" else "plateado"
    mejor_movimiento = None

    if maximizando:
        max_eval = float('-inf')
        movimientos = generar_movimientos(tablero, color_jugador)

        for movimiento in movimientos:
            pos_inicial, pos_final = movimiento
            nuevo_tablero = reglas.mover_ficha(tablero, pos_inicial, pos_final)
                
            evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, False, color_jugador)

            if evaluacion > max_eval:
                max_eval = evaluacion
                mejor_movimiento = movimiento

            alfa = max(alfa, evaluacion)
            if beta <= alfa:
                break

        return max_eval, mejor_movimiento

    else:
        min_eval = float('inf')
        movimientos = generar_movimientos(tablero, color_oponente)

        for movimiento in movimientos:
            pos_inicial, pos_final = movimiento
            nuevo_tablero = reglas.mover_ficha(tablero, pos_inicial, pos_final)


            evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, True, color_jugador)

            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = movimiento

            beta = min(beta, evaluacion)
            if beta <= alfa:
                break

        return min_eval, mejor_movimiento



def decidir_mejor_movimiento(tablero, profundidad, color_jugador):
    """
    Determina el mejor movimiento para el jugador dado.
    """
    _, mejor_movimiento = minimax(tablero, profundidad, float('-inf'), float('inf'), True, color_jugador)
    return mejor_movimiento
