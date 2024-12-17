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
                    # Bonus por posición estratégica
                    if casilla.animal == "conejo":
                        puntaje += (7 - casilla.posY) if color_jugador == "dorado" else casilla.posY
                    # Penalizar posiciones en trampas
                    if casilla.esta_en_trampa(tablero):
                        puntaje -= 5
                else:
                    puntaje -= casilla.peso
    return puntaje


def generar_movimientos(tablero, color_jugador):
    movimientos = []

    for y in range(len(tablero)):
        for x in range(len(tablero[y])):
            casilla = tablero[y][x]
            if isinstance(casilla, piece.Piece) and casilla.color == color_jugador:
                posiciones_disponibles = casilla.ObtenerPosicionesDisponibles(tablero)
                posiciones_validas = [
                    pos for pos in posiciones_disponibles if validar_movimiento(tablero, (x, y), pos)
                ]
                for pos_final in posiciones_validas:
                    # Restricción para conejos (solo mover hacia adelante)
                    if casilla.animal == "conejo" and not movimiento_valido_conejo((x, y), pos_final, color_jugador):
                        continue
                    movimientos.append(((x, y), pos_final))

    return movimientos

def movimiento_valido_conejo(pos_inicial, pos_final, color_jugador):
    x1, y1 = pos_inicial
    x2, y2 = pos_final
    return (y2 < y1) if color_jugador == "dorado" else (y2 > y1)


import copy

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
            nuevo_tablero = copy.deepcopy(tablero)
            reglas.mover_ficha(nuevo_tablero, pos_inicial, pos_final)

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
            nuevo_tablero = copy.deepcopy(tablero)
            reglas.mover_ficha(nuevo_tablero, pos_inicial, pos_final)

            evaluacion, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, True, color_jugador)

            if evaluacion < min_eval:
                min_eval = evaluacion
                mejor_movimiento = movimiento

            beta = min(beta, evaluacion)
            if beta <= alfa:
                break

        return min_eval, mejor_movimiento


def decidir_mejor_movimiento(tablero, profundidad, color_jugador):
    _, mejor_movimiento = minimax(tablero, profundidad, float('-inf'), float('inf'), True, color_jugador)
    if mejor_movimiento is None:
        print("No hay movimientos válidos disponibles.")
    return mejor_movimiento
