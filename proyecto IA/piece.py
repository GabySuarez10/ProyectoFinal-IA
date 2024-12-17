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
        return 0 <= x <= 7 and 0 <= y <= 7 and type(tablero[y][x]) is str

    def ObtenerPosicionesDisponibles(self, tablero):
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
                listaPosicionesDisponibles.append((x, y))

        return listaPosicionesDisponibles

    def esta_en_trampa(self, tablero):
        """Verifica si la pieza está en una posición de trampa."""
        trampas = [(2, 2), (2, 5), (5, 2), (5, 5)]
        return (self.posX, self.posY) in trampas

    def __str__(self):
        return f"{self.color[0].upper()}{self.animal[0].upper()}"
    
    
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
                    listaEnemigosDisponibles.append((x, y))

        return listaEnemigosDisponibles


class Conejo_P(Piece):
    def __init__(self, peso, color, posX, posY):
        super().__init__("conejo", peso, color, posX, posY)

class Conejo(Piece):
    def __init__(self, peso, color, posX, posY):
        super().__init__("conejo", peso, color, posX, posY)
