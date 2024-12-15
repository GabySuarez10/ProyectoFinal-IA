import reglas
import piece

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
    Genera todos los movimientos posibles para un jugador.
    Retorna una lista de movimientos en forma de (pos_inicial, pos_final).
    """
    movimientos = []

    for y in range(8):
        for x in range(8):
            casilla = tablero[y][x]
            if isinstance(casilla, piece.Piece) and casilla.color == color_jugador:
                posiciones_disponibles = casilla.ObtenerPosicionesDisponibles(tablero)
                for pos_final in posiciones_disponibles:
                    movimientos.append(((x, y), pos_final))

    return movimientos

def minimax(tablero, profundidad, alfa, beta, maximizando, color_jugador):
    """
    Algoritmo Minimax con poda alfa-beta.
    - tablero: estado actual del tablero.
    - profundidad: nivel de profundidad en el árbol de decisión.
    - alfa, beta: valores para la poda alfa-beta.
    - maximizando: True si es el turno del jugador maximizador, False para el minimizador.
    - color_jugador: color del jugador actual (dorado o plateado).
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
