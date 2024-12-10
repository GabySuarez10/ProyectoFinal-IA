class Piece:
    def __init__(self, animal, peso, color, posX, posY):
        self.animal = animal
        self.color = color
        self.peso = peso
        self.congelada = False
        self.viva = True
        self.posX = posX
        self.posY = posY

    def _es_posicion_valida(self, x, y, tablero):
        """Verifica si la posición (x, y) es válida en el tablero."""
        return 0 <= x <= 7 and 0 <= y <= 7 and type(tablero[y][x]) is str

    def ObtenerPosicionesDisponibles(self, tablero):
        """Retorna las direcciones disponibles para mover la ficha."""
        posiciones = {
            "arriba": (self.posX, self.posY - 1),
            "derecha": (self.posX + 1, self.posY),
            "abajo": (self.posX, self.posY + 1),
            "izquierda": (self.posX - 1, self.posY)
        }

        listaPosicionesDisponibles = []

        for posicion, (x, y) in posiciones.items():
            if self._es_posicion_valida(x, y, tablero):
                if posicion == "arriba" and self.animal == "conejo" and self.color == "plateado":
                    continue
                if posicion == "abajo" and self.animal == "conejo" and self.color == "dorado":
                    continue
                listaPosicionesDisponibles.append((x,y))

        return listaPosicionesDisponibles

    def ObtenerEnemigos(self, tablero):
        """Retorna las direcciones de enemigos de menor peso."""
        posiciones = {
            "arriba": (self.posX, self.posY - 1),
            "derecha": (self.posX + 1, self.posY),
            "abajo": (self.posX, self.posY + 1),
            "izquierda": (self.posX - 1, self.posY)
        }

        listaEnemigosDisponibles = []

        for direccion, (x, y) in posiciones.items():
            if 0 <= x <= 7 and 0 <= y <= 7 and type(tablero[y][x]) is not str:
                enemigo = tablero[y][x]
                if enemigo.color != self.color and enemigo.peso < self.peso:
                    listaEnemigosDisponibles.append(direccion)

        return listaEnemigosDisponibles


    def Empujar(self, tablero, enemigo, direccion):
        """Empuja al enemigo hacia una de sus direcciones disponibles."""
        direcciones = {
            "arriba": (enemigo.posX, enemigo.posY - 1),
            "derecha": (enemigo.posX + 1, enemigo.posY),
            "abajo": (enemigo.posX, enemigo.posY + 1),
            "izquierda": (enemigo.posX - 1, enemigo.posY)
        }

        x, y = direcciones[direccion]
        if self._es_posicion_valida(x, y, tablero):
            # Mueve el enemigo y la pieza actual
            tablero[enemigo.posY][enemigo.posX] = " "
            tablero[self.posY][self.posX] = " "
            self.posX, self.posY = enemigo.posX, enemigo.posY
            enemigo.posX, enemigo.posY = x, y
            tablero[enemigo.posY][enemigo.posX] = enemigo
            tablero[self.posY][self.posX] = self

        return tablero

    def Jalar(self, tablero, enemigo, direccion):
        """Jala al enemigo hacia la posición de la pieza."""
        direcciones = {
            "arriba": (self.posX, self.posY - 1),
            "derecha": (self.posX + 1, self.posY),
            "abajo": (self.posX, self.posY + 1),
            "izquierda": (self.posX - 1, self.posY)
        }

        x, y = direcciones[direccion]
        if self._es_posicion_valida(x, y, tablero):
            # Mueve la pieza y el enemigo
            tablero[enemigo.posY][enemigo.posX] = " "
            tablero[self.posY][self.posX] = " "
            enemigo.posX, enemigo.posY = self.posX, self.posY
            self.posX, self.posY = x, y
            tablero[self.posY][self.posX] = self
            tablero[enemigo.posY][enemigo.posX] = enemigo

        return tablero
    # Función para calcular las posiciones válidas de una pieza
def calcular_posiciones_movimiento(tablero, pieza):
    posiciones_validas = []
    
    # Este es un ejemplo para el conejo (deberías agregar las reglas de movimiento correspondientes a tus piezas)
    if pieza.animal == "conejo":
        x, y = pieza.posX, pieza.posY
        # El conejo puede moverse a una posición horizontal o verticalmente adyacente
        if x + 1 < 8 and tablero[y][x + 1] == " ":
            posiciones_validas.append((x + 1, y))
        if x - 1 >= 0 and tablero[y][x - 1] == " ":
            posiciones_validas.append((x - 1, y))
        if y + 1 < 8 and tablero[y + 1][x] == " ":
            posiciones_validas.append((x, y + 1))
        if y - 1 >= 0 and tablero[y - 1][x] == " ":
            posiciones_validas.append((x, y - 1))

    return posiciones_validas
