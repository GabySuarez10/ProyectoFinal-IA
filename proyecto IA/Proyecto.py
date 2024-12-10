import random
import numpy as np

tablero = [
    [" ", " ", " ", " ", " ", " ", " ", " "]
    [" ", " ", " ", " ", " ", " ", " ", " "]
    [" ", " ", " ", " ", " ", " ", " ", " "]
    [" ", " ", " ", " ", " ", " ", " ", " "]   
    [" ", " ", " ", " ", " ", " ", " ", " "]
    [" ", " ", " ", " ", " ", " ", " ", " "]
    [" ", " ", " ", " ", " ", " ", " ", " "]
    [" ", " ", " ", " ", " ", " ", " ", " "]
]

class conejo: 
    def init (self, color, peso, activa, viva, posX, posY):
        self.color = color
        self.peso = 0
        self.activa = activa
        self.viva = viva
        self.posX = 0
        self.posY = 0

#retornar lista con las posiciones disponibles que tenga la ficha
    def obtenerCasillasDispo(self):
        self.posX
        self.posY
        abajo = False
        izquierda = False
        derecha = False
        adelante = False
        listaMov = [] #adelante, atras, izq, derecha
        #verifico el mov hacia abajo
        if self.posY != 7 and self.color == "plateado" and type (tablero[self.posY + 1][self.posX] is str):
            adelante = True
        if  self.posY != 0 and self.color == "dorado":
            adelanre = True



