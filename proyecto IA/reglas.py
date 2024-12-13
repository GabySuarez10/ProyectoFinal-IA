import piece

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
    # Devuelve una copia profunda del tablero
    return [row[:] for row in estado]

def mover_ficha(tablero, pos_inicial, pos_final):
    # Realiza una copia del tablero
    copia = ObtenerCopiaTablero(tablero)
    
    # Obtiene la ficha en la posición inicial
    ficha = copia[pos_inicial[1]][pos_inicial[0]]  # Acceso directo a la posición inicial
    
    if isinstance(ficha, piece.Piece) and ficha.congelada == False:  # Verifica si hay una ficha en la posición inicial
        # Obtiene las posiciones disponibles para moverse
        lista_pos_dispo = ficha.ObtenerPosicionesDisponibles(copia)
        
        # Verifica si la posición final es válida
        if pos_final in lista_pos_dispo:
            # Actualiza el tablero: limpia la posición inicial
            copia[pos_inicial[1]][pos_inicial[0]] = " "
            
            # Actualiza la posición de la ficha
            ficha.posX = pos_final[0]
            ficha.posY = pos_final[1]
            
            # Mueve la ficha a la posición final
            copia[pos_final[1]][pos_final[0]] = ficha

    trampas(copia)
    Congelados(copia)
    return copia

def empujar_ficha(tablero, pos_ficha, pos_enemigo, pos_resultado):
    # Realiza una copia del tablero
    copia = ObtenerCopiaTablero(tablero)
    
    
    ficha = copia[pos_ficha[1]][pos_ficha[0]] 
    
    if isinstance(ficha, piece.Piece) and ficha.congelada==False: 
       
        lista_enemigos = ficha.ObtenerEnemigos(copia)
        
        if pos_enemigo in lista_enemigos:
            if pos_resultado in copia [pos_enemigo[1]] [pos_enemigo[0]].ObtenerPosicionesDisponibles(copia):
                copia = ficha.Empujar(copia,copia[pos_enemigo[1]] [pos_enemigo[0]], pos_resultado)
    trampas(copia)
    Congelados(copia)
    return copia

def halar_ficha(tablero, pos_ficha, pos_enemigo, pos_resultado):

    copia = ObtenerCopiaTablero(tablero)
    
    
    ficha = copia[pos_ficha[1]][pos_ficha[0]] 
    
    if isinstance(ficha, piece.Piece)and ficha.congelada==False:  
       
        lista_enemigos = ficha.ObtenerEnemigos(copia)
        
        if pos_enemigo in lista_enemigos:
            if pos_resultado in ficha.ObtenerPosicionesDisponibles(copia):
                copia = ficha.Halar(copia,copia[pos_enemigo[1]] [pos_enemigo[0]], pos_resultado)
    trampas(copia)
    Congelados(copia)
    return copia