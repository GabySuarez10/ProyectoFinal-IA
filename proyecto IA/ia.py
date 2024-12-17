import piece
import reglas
import copy

TRAMPAS_SEGURAS = {
    (2, 2): [(2, 1), (3, 2), (1, 2), (2, 3)],
    (2, 5): [(2, 6), (3, 5), (2, 4), (1, 5)],
    (5, 2): [(4, 2), (5, 1), (6, 2), (5, 3)],
    (5, 5): [(4, 5), (6, 5), (5, 6), (5, 4)],
}

def es_posicion_valida(pos):
    """Verifica si una posición está dentro de los límites del tablero."""
    return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

def evaluar_tablero(tablero, color_jugador):
    puntaje = 0
    for fila in tablero:
        for casilla in fila:
            if isinstance(casilla, piece.Piece):
                if casilla.color == color_jugador:
                    puntaje += casilla.peso
                    puntaje += (7 - casilla.posY) if casilla.animal == "conejo" else 0
                    if casilla.esta_en_trampa(tablero):
                        puntaje -= 7
                else:
                    puntaje -= casilla.peso
                    puntaje -= (casilla.posY) if casilla.animal == "conejo" else 0

    # Control del centro y trampas
    posiciones_centro = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for y, x in posiciones_centro:
        if isinstance(tablero[y][x], piece.Piece):
            if tablero[y][x].color == color_jugador:
                puntaje += 3
            else:
                puntaje -= 3

    # Control de trampas
    for trampa, adyacentes in TRAMPAS_SEGURAS.items():
        pieza_trampa = tablero[trampa[1]][trampa[0]]
        if isinstance(pieza_trampa, piece.Piece):
            if pieza_trampa.color == color_jugador:
                puntaje += 5
            else:
                puntaje -= 5

    return puntaje


def generar_movimientos(tablero, color_jugador):
    """Genera todos los movimientos válidos para un jugador."""
    movimientos = []

    for y in range(len(tablero)):
        for x in range(len(tablero[y])):
            casilla = tablero[y][x]
            if isinstance(casilla, piece.Piece) and casilla.color == color_jugador:
                posiciones_disponibles = casilla.ObtenerPosicionesDisponibles(tablero)

                for pos_final in posiciones_disponibles:
                    if es_posicion_valida(pos_final) and reglas.validar_movimiento(tablero, (x, y), pos_final):
                        # Prioridad máxima: Conejos hacia la fila de victoria
                        if casilla.animal == "conejo" and (
                            (color_jugador == "dorado" and pos_final[1] == 0) or
                            (color_jugador == "plateado" and pos_final[1] == 7)
                        ):
                            movimientos.append((3, "mover", (x, y), pos_final))
                        # Prioridad media: Evitar trampas peligrosas
                        elif not es_posicion_trampa_peligrosa(tablero, pos_final, casilla):
                            movimientos.append((2, "mover", (x, y), pos_final))
                        else:
                            movimientos.append((1, "mover", (x, y), pos_final))

                # Agregar movimientos de halar y empujar
                enemigos = casilla.ObtenerEnemigos(tablero)
                for enemigo in enemigos:
                    for pos_final in casilla.ObtenerPosicionesDisponibles(tablero):
                        if es_posicion_valida(pos_final) and reglas.validar_movimiento(tablero, enemigo, pos_final):
                            movimientos.append((2, "halar", (x, y), enemigo, pos_final))

                    # Empujar
                    posiciones_empujar = tablero[enemigo[1]][enemigo[0]].ObtenerPosicionesDisponibles(tablero)
                    for pos_final in posiciones_empujar:
                        if es_posicion_valida(pos_final) and reglas.validar_movimiento(tablero, enemigo, pos_final):
                            movimientos.append((2, "empujar", (x, y), enemigo, pos_final))

    # Ordenar movimientos por prioridad
    movimientos.sort(reverse=True)
    return [mov[1:] for mov in movimientos]

def es_posicion_trampa_peligrosa(tablero, pos, pieza):
    """Determina si una trampa es peligrosa."""
    if pos in TRAMPAS_SEGURAS:
        for segura in TRAMPAS_SEGURAS[pos]:
            if es_posicion_valida(segura) and isinstance(tablero[segura[1]][segura[0]], piece.Piece) and \
                    tablero[segura[1]][segura[0]].color == pieza.color:
                return False  # Trampa segura
        return True  # Trampa peligrosa
    return False  # No es una trampa

def aplicar_movimiento(tablero, movimiento):
    """Aplica un movimiento al tablero y retorna una copia modificada."""
    nuevo_tablero = copy.deepcopy(tablero)
    if movimiento[0] == "mover":
        _, pos_inicial, pos_final = movimiento
        nuevo_tablero = reglas.mover_ficha(nuevo_tablero, pos_inicial, pos_final)
    elif movimiento[0] == "halar":
        _, pos_inicial, pos_enemigo, pos_resultado = movimiento
        nuevo_tablero = reglas.halar_ficha(nuevo_tablero, pos_inicial, pos_enemigo, pos_resultado)
    elif movimiento[0] == "empujar":
        _, pos_inicial, pos_enemigo, pos_resultado = movimiento
        nuevo_tablero = reglas.empujar_ficha(nuevo_tablero, pos_inicial, pos_enemigo, pos_resultado)
    return nuevo_tablero


def minimax(tablero, profundidad, alfa, beta, es_turno_ia, color_jugador, transposicion):
    """Algoritmo Minimax con poda alfa-beta y tabla de transposición."""
    # Generar un hash único del tablero
    estado_tablero = hash(str(tablero))
    if estado_tablero in transposicion:
        return transposicion[estado_tablero]

    if profundidad == 0 or reglas.verificar_victoria(tablero, None):
        valor = evaluar_tablero(tablero, color_jugador)
        transposicion[estado_tablero] = (valor, None)
        return valor, None

    if es_turno_ia:
        mejor_valor = float('-inf')
        mejor_movimiento = None
        posibles_movimientos = generar_movimientos(tablero, color_jugador)

        for movimiento in posibles_movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, False, color_jugador, transposicion)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

            alfa = max(alfa, mejor_valor)
            if beta <= alfa:
                break

        transposicion[estado_tablero] = (mejor_valor, mejor_movimiento)
        return mejor_valor, mejor_movimiento
    else:
        mejor_valor = float('inf')
        mejor_movimiento = None
        color_oponente = "dorado" if color_jugador == "plateado" else "plateado"
        posibles_movimientos = generar_movimientos(tablero, color_oponente)

        for movimiento in posibles_movimientos:
            nuevo_tablero = aplicar_movimiento(tablero, movimiento)
            valor, _ = minimax(nuevo_tablero, profundidad - 1, alfa, beta, True, color_jugador, transposicion)

            if valor < mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento

            beta = min(beta, mejor_valor)
            if beta <= alfa:
                break

        transposicion[estado_tablero] = (mejor_valor, mejor_movimiento)
        return mejor_valor, mejor_movimiento


def decidir_mejor_movimiento(tablero, profundidad, color_jugador):
    """Decide el mejor movimiento usando Minimax."""
    mejor_valor, mejor_movimiento = minimax(tablero, profundidad, float('-inf'), float('inf'), True, color_jugador, {})


    if mejor_movimiento is None:
        print("La IA no encontró movimientos válidos. Turno terminado.")
        return None

    print(f"Mejor movimiento elegido por la IA: {mejor_movimiento}")
    return mejor_movimiento
