import piece
import pygame

def verificar_victoria(tablero, pantalla):
    # Revisar si algún conejo plateado está en la fila 7 (lado inicial de los dorados)
    for x in range(len(tablero[7])):  # Recorremos la fila 7
        if isinstance(tablero[7][x], piece.Piece) and tablero[7][x].animal == "conejo" and tablero[7][x].color == "plateado":
            mostrar_mensaje(pantalla, "Haz perdido")
            return True  # Victoria para el jugador plateado
    # Revisar si algún conejo dorado está en la fila 0 (lado inicial de los plateados)
    for x in range(len(tablero[0])):  # Recorremos la fila 0
        if isinstance(tablero[0][x], piece.Piece) and tablero[0][x].animal == "conejo" and tablero[0][x].color == "dorado":
            mostrar_mensaje(pantalla, "¡El jugador dorado gana!")
            return True  # Victoria para el jugador dorado
    return False  # No hay victoria aún

def mostrar_mensaje(pantalla, mensaje):
    fuente = pygame.font.Font(None, 50)  # Crear una fuente
    texto = fuente.render(mensaje, True, (255, 255, 0))  # Crear el texto
    pantalla.fill((0, 0, 0))  # Llenar la pantalla con negro
    pantalla.blit(texto, (pantalla.get_width() // 2 - texto.get_width() // 2, pantalla.get_height() // 2 - texto.get_height() // 2))
    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.delay(3000)

def trampas(tablero): 
    # La sintaxis es (X,Y)
    posiciones_trampas = [(2, 2), (2, 5), (5, 2), (5, 5)]
    listas_seguras = [
        [(2, 1), (3, 2), (1, 2), (2, 3)],
        [(2, 6), (3, 5), (2, 4), (1, 5)],
        [(4, 2), (5, 1), (6, 2), (5, 3)],
        [(4, 5), (6, 5), (5, 6), (5, 4)]
    ]

    for pos_trampa, seguras in zip(posiciones_trampas, listas_seguras):
        segura = False
        if isinstance(tablero[pos_trampa[1]][pos_trampa[0]], piece.Piece):
            color = tablero[pos_trampa[1]][pos_trampa[0]].color
            for posicion in seguras:
                if (
                    isinstance(tablero[posicion[1]][posicion[0]], piece.Piece)
                    and color == tablero[posicion[1]][posicion[0]].color
                ):
                    segura = True
                    break
        if not segura:
            tablero[pos_trampa[1]][pos_trampa[0]] = "0"


def Congelados(tablero):
    #descongelamos todas las fichas
    for i in range (8): 
        for j in range (8):
            if isinstance(tablero[i][j], piece.Piece):
                tablero [i][j].congelada = False
    #congelamos las fichas que tienen un enemigo que pesa mas que ellas y no tienen compañeros a los lados
    for i in range (8): 
        for j in range (8):
            if isinstance(tablero[i][j], piece.Piece):
                listaEnemigos = tablero [i][j].ObtenerEnemigos(tablero)
                for enemigo in listaEnemigos:
                    segura = False
                #verificamos si tiene amigos que lo salven
                    listaCardinales = [(enemigo[0], enemigo[1] -1),
                                       (enemigo[0]-1,enemigo[1]),
                                       (enemigo[0],enemigo[1]+1),
                                       (enemigo[0]+1,enemigo[1])]
                    for posicion in listaCardinales:
                        try:
                            if tablero [enemigo[1] ][enemigo[0]].color == tablero [posicion[1] ][posicion[0]].color:
                                segura = True
                        except:
                            continue
                    if not segura:
                        tablero [enemigo[1] ][enemigo[0]].congelada = True
                        
def ObtenerCopiaTablero(estado):
    import copy
    return copy.deepcopy(estado)  # Asegura una copia profunda


def validar_movimiento(tablero, pos_inicial, pos_final):
    """
    Valida si un movimiento es permitido según las reglas generales del juego.
    """
    if not (0 <= pos_inicial[0] < len(tablero[0]) and 0 <= pos_inicial[1] < len(tablero)):
        return False  # Posición inicial fuera del tablero

    if not (0 <= pos_final[0] < len(tablero[0]) and 0 <= pos_final[1] < len(tablero)):
        return False  # Posición final fuera del tablero

    ficha = tablero[pos_inicial[1]][pos_inicial[0]]
    
    if not isinstance(ficha, piece.Piece):
        return False  # No hay una ficha en la posición inicial
    
    if ficha.congelada:
        return False  # La ficha está congelada
    
    posiciones_disponibles = ficha.ObtenerPosicionesDisponibles(tablero)
    return pos_final in posiciones_disponibles


def mover_ficha(tablero, pos_inicial, pos_final):
    print(f"Intentando mover pieza de {pos_inicial} a {pos_final}")
    copia = ObtenerCopiaTablero(tablero)
    if validar_movimiento(copia, pos_inicial, pos_final):
        ficha = copia[pos_inicial[1]][pos_inicial[0]]
        # Actualizar tablero y posición de la ficha
        copia[pos_inicial[1]][pos_inicial[0]] = " "
        ficha.posX, ficha.posY = pos_final
        copia[pos_final[1]][pos_final[0]] = ficha

        trampas(copia)
        Congelados(copia)
        return copia  # Devuelve el tablero actualizado
    return tablero  # Si no es válido, devuelve el tablero original



def empujar_ficha(tablero, pos_ficha, pos_enemigo, pos_resultado):
    copia = ObtenerCopiaTablero(tablero)
    ficha = copia[pos_ficha[1]][pos_ficha[0]]

    if isinstance(ficha, piece.Piece) and not ficha.congelada:
        lista_enemigos = ficha.ObtenerEnemigos(copia)
        if pos_enemigo in lista_enemigos:
            enemigo = copia[pos_enemigo[1]][pos_enemigo[0]]
            if pos_resultado in enemigo.ObtenerPosicionesDisponibles(copia):
                copia = ficha.Empujar(copia, enemigo, pos_resultado)
                trampas(copia)
                Congelados(copia)
    return copia


def halar_ficha(tablero, pos_ficha, pos_enemigo, pos_resultado):
    copia = ObtenerCopiaTablero(tablero)
    ficha = copia[pos_ficha[1]][pos_ficha[0]]

    if isinstance(ficha, piece.Piece) and not ficha.congelada:
        lista_enemigos = ficha.ObtenerEnemigos(copia)
        if pos_enemigo in lista_enemigos:
            enemigo = copia[pos_enemigo[1]][pos_enemigo[0]]
            if pos_resultado in ficha.ObtenerPosicionesDisponibles(copia):
                copia = ficha.Halar(copia, enemigo, pos_resultado)
                trampas(copia)
                Congelados(copia)
    return copia
