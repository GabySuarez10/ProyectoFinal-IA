class Piece:
    def __init__(self,animal,peso, color, posX, posY):
        self.animal = animal
        self.color = color  # Color de la pieza (por ejemplo, "dorado" o "plateado")
        self.posX = posX    # Posición X en el tablero
        self.posY = posY    # Posición Y en el tablero
        self.peso = peso    # Peso de la pieza (para evaluaciones de IA)
        self.congelada = False  # Indica si la pieza está congelada

    def ObtenerPosicionesDisponibles(self, tablero):
        posiciones_disponibles = []
        movimientos_posibles = [
            (self.posX, self.posY - 1),  # Arriba
            (self.posX, self.posY + 1),  # Abajo
            (self.posX - 1, self.posY),  # Izquierda
            (self.posX + 1, self.posY),  # Derecha
        ]

        for pos in movimientos_posibles:
            x, y = pos
            # Verificar si la posición está dentro de los límites del tablero
            if 0 <= x < len(tablero[0]) and 0 <= y < len(tablero):
                # Verificar si la posición está vacía
                if tablero[y][x] == " ":
                    posiciones_disponibles.append(pos)

        return posiciones_disponibles

    def ObtenerEnemigos(self, tablero):
        """
        Encuentra enemigos adyacentes a la posición actual.
        """
        enemigos = []
        movimientos_posibles = [
            (self.posX, self.posY - 1),  # Arriba
            (self.posX, self.posY + 1),  # Abajo
            (self.posX - 1, self.posY),  # Izquierda
            (self.posX + 1, self.posY),  # Derecha
        ]

        for pos in movimientos_posibles:
            x, y = pos
            if 0 <= x < len(tablero[0]) and 0 <= y < len(tablero):
                ficha = tablero[y][x]
                if isinstance(ficha, Piece) and ficha.color != self.color:
                    enemigos.append(pos)
        return enemigos

    def Empujar(self, tablero, enemigo, pos_resultado):
        """
        Implementación para empujar a un enemigo (personalizar según reglas del juego).
        """
        # Mueve al enemigo a la nueva posición y actualiza el tablero.
        tablero[pos_resultado[1]][pos_resultado[0]] = enemigo
        tablero[enemigo.posY][enemigo.posX] = " "
        enemigo.posX, enemigo.posY = pos_resultado
        return tablero

    def Halar(self, tablero, enemigo, pos_resultado):
        """
        Implementación para halar a un enemigo (personalizar según reglas del juego).
        """
        # Mueve al enemigo a la nueva posición y actualiza el tablero.
        tablero[pos_resultado[1]][pos_resultado[0]] = enemigo
        tablero[enemigo.posY][enemigo.posX] = " "
        enemigo.posX, enemigo.posY = pos_resultado
        return tablero


class Conejo(Piece):
    def __init__(self, id, color, posX, posY):
        # Llamar al constructor de la clase base (Piece) con los parámetros adecuados
        super().__init__("conejo", id, color, posX, posY)
    
    def PosicionesDisponibles(self, tablero):
        """
        Limita los movimientos del conejo a un paso en las direcciones cardinales.
        """
        posiciones_disponibles = []
        movimientos_posibles = [
            (self.posX, self.posY - 1),  # Arriba
        ]

        for pos in movimientos_posibles:
            x, y = pos
            # Verificar si la posición está dentro de los límites del tablero
            if 0 <= x < len(tablero[0]) and 0 <= y < len(tablero):
                # Verificar si la posición está vacía
                if tablero[y][x] == " ":
                    posiciones_disponibles.append(pos)

        return posiciones_disponibles

class Conejo_P(Piece):
    def __init__(self, id, color, posX, posY):
        # Llamar al constructor de la clase base (Piece) con los parámetros adecuados
        super().__init__("conejo", id, color, posX, posY)
    
    def PosicionesDisponibles(self, tablero):
        """
        Limita los movimientos del conejo a un paso en las direcciones cardinales.
        """
        posiciones_disponibles = []
        movimientos_posibles = [
            (self.posX, self.posY + 1),  # Abajo 
        ]

        for pos in movimientos_posibles:
            x, y = pos
            # Verificar si la posición está dentro de los límites del tablero
            if 0 <= x < len(tablero[0]) and 0 <= y < len(tablero):
                # Verificar si la posición está vacía
                if tablero[y][x] == " ":
                    posiciones_disponibles.append(pos)

        return posiciones_disponibles
    
    
