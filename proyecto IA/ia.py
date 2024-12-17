import reglas
import piece
from reglas import validar_movimiento


def evaluar_tablero(tablero, color_jugador):
    puntaje = 0
    for fila in tablero:
        for casilla in fila:
            if isinstance(casilla, piece.Piece):
                if casilla.color == color_jugador:
                    puntaje += casilla.peso
                else:
                    puntaje -= casilla.peso
    return puntaje


def generar_movimientos(tablero, color_jugador):
    movimientos = []
    for y in range(len(tablero)):
        for x in range(len(tablero[y])):
            if len(movimientos) >= 4:  # Limitar a 4 movimientos
                break
            casilla = tablero[y][x]
            if isinstance(casilla, piece.Piece) and casilla.color == color_jugador:
                posiciones_adyacentes = [
                    (x + dx, y + dy)
                    for dx in [-1, 0, 1]
                    for dy in [-1, 0, 1]
                    if (dx != 0 or dy != 0) and 0 <= x + dx < len(tablero[0]) and 0 <= y + dy < len(tablero)
                ]
                posiciones_validas = [
                    pos for pos in posiciones_adyacentes if validar_movimiento(tablero, (x, y), pos)
                ]
                for pos_final in posiciones_validas:
                    movimientos.append(((x, y), pos_final))
                    if len(movimientos) >= 4:
                        break
    return movimientos




# Algoritmo Minimax con poda alfa-beta
def minimax(tablero, profundidad, alfa, beta, maximizando, color_jugador):
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

# Función para decidir el mejor movimiento
def decidir_mejor_movimiento(tablero, profundidad, color_jugador):
    _, mejor_movimiento = minimax(tablero, profundidad, float('-inf'), float('inf'), True, color_jugador)
    return mejor_movimiento

