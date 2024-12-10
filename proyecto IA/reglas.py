import piece

def ObtenerCopiaTablero(estado):
    # Devuelve una copia profunda del tablero
    return [row[:] for row in estado]

def mover_ficha(tablero, pos_inicial, pos_final):
    # Realiza una copia del tablero
    copia = ObtenerCopiaTablero(tablero)
    
    # Obtiene la ficha en la posición inicial
    ficha = copia[pos_inicial[1]][pos_inicial[0]]  # Acceso directo a la posición inicial
    
    if isinstance(ficha, piece.Piece):  # Verifica si hay una ficha en la posición inicial
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
    
    return copia
