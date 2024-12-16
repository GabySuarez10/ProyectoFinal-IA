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
                    listaEnemigosDisponibles.append((x,y))

        return listaEnemigosDisponibles


    def Empujar(self, tablero, enemigo, direccion):
        """Empuja al enemigo hacia una de sus direcciones disponibles."""
        direcciones = {
            "arriba": (enemigo.posX, enemigo.posY - 1),
            "derecha": (enemigo.posX + 1, enemigo.posY),
            "abajo": (enemigo.posX, enemigo.posY + 1),
            "izquierda": (enemigo.posX - 1, enemigo.posY)
        }

        x, y = direccion
        if self._es_posicion_valida(x, y, tablero):
            # Mueve el enemigo y la pieza actual
            tablero[enemigo.posY][enemigo.posX] = " "
            tablero[self.posY][self.posX] = " "
            self.posX, self.posY = enemigo.posX, enemigo.posY
            enemigo.posX, enemigo.posY = x, y
            tablero[enemigo.posY][enemigo.posX] = enemigo
            tablero[self.posY][self.posX] = self

        return tablero

    def Halar(self, tablero, enemigo, direccion):
        """Hala al enemigo hacia la posición de la pieza."""
        direcciones = {
            "arriba": (self.posX, self.posY - 1),
            "derecha": (self.posX + 1, self.posY),
            "abajo": (self.posX, self.posY + 1),
            "izquierda": (self.posX - 1, self.posY)
        }

        x, y = direccion
        if self._es_posicion_valida(x, y, tablero):
            # Mueve la pieza y el enemigo
            tablero[enemigo.posY][enemigo.posX] = " "
            tablero[self.posY][self.posX] = " "
            enemigo.posX, enemigo.posY = self.posX, self.posY
            self.posX, self.posY = x, y
            tablero[self.posY][self.posX] = self
            tablero[enemigo.posY][enemigo.posX] = enemigo

        return tablero
    
    def __str__(self):
            return f"{self.color[0].upper()}{self.animal[0].upper()}"

class Conejo_P(Piece):
    def __init__(self, peso, color, posX, posY):
        super().__init__("conejo", peso, color, posX, posY)

class Conejo(Piece):
    def __init__(self, peso, color, posX, posY):
        super().__init__("conejo", peso, color, posX, posY)