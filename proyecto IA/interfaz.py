import pygame
import sys
import piece
import reglas
import os  
import ia 

os.chdir(os.path.dirname(__file__))


# Configuración general
ANCHO = 512
ALTO = 600
TAM_CELDA = 64
FPS = 5
NEGRO = (0, 0, 0)
VINOTINTO = (128, 0, 32)
CAFE = (210, 180, 140)
pos1 = None
pos2 = None
pos3 = None

# Función para obtener la posición de un clic en el tablero
def obtener_posicion(pos1, pos2, pos3=[0,0]):
    pos1X = ""
    pos1Y = ""
    pos2X = ""
    pos2Y = ""
    pos3X = ""
    pos3Y = ""
  
   #convierte coordenadas del click a posicion en el tablero
    pos1X = int(pos1[0]/TAM_CELDA)
    pos1Y = int(pos1[1]/TAM_CELDA)
    print(f"Primer clic en: {pos1}")
    
    pos2X = int(pos2[0]/TAM_CELDA)
    pos2Y = int(pos2[1]/TAM_CELDA)
    print(f"Segundo clic en: {pos2}")
    
    pos3X = int(pos3[0]/TAM_CELDA)
    pos3Y = int(pos3[1]/TAM_CELDA)
    print(f"Primer clic en: {pos3}")
    
    #limpia las posiciones
    pos1 = None
    pos2 = None
    pos3 = None
    return (pos1X, pos1Y), (pos2X, pos2Y), (pos3X, pos3Y)

# Inicializar pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

# Tablero inicial
tablero1 = [
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", "0", " ", " ", "0", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", "0", " ", " ", "0", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
]

# Función para obtener una copia del tablero
def ObtenerCopiaTablero(estado):
    import copy
    return copy.deepcopy(estado)  # Asegura una copia profunda

# Colocar piezas en el tablero fichas plateadas
tablero2 = ObtenerCopiaTablero(tablero1)
for y in range(1):
    for x in range(len(tablero2[y])):
        tablero2[y][x] = piece.Conejo_P(1, "plateado", x, y)
tablero2[1][0] = piece.Piece("gato", 2, "plateado", 0, 1)      
tablero2[1][7] = piece.Piece("gato", 2, "plateado", 7, 1)
tablero2[1][1] = piece.Piece("perro", 3, "plateado", 1, 1)     
tablero2[1][6] = piece.Piece("perro", 3, "plateado", 6, 1)
tablero2[1][2] = piece.Piece("caballo", 4, "plateado", 2, 1)
tablero2[1][5] = piece.Piece("caballo", 4, "plateado", 5, 1)
tablero2[1][3] = piece.Piece("camello", 5, "plateado", 3, 1) 
tablero2[1][4] = piece.Piece("elefante", 6, "plateado", 4, 1) 

# Cargar imágenes de las piezas plateadas
imagenCone = pygame.image.load('iconos/conejo_plateado.png').convert_alpha()
imagenCone = pygame.transform.scale(imagenCone, (TAM_CELDA, TAM_CELDA))
imagenElef = pygame.image.load('iconos\elefante_plateado.png').convert_alpha()
imagenElef = pygame.transform.scale(imagenElef, (TAM_CELDA, TAM_CELDA))
imagenCame = pygame.image.load('iconos\camello_plateado.png').convert_alpha()
imagenCame = pygame.transform.scale(imagenCame, (TAM_CELDA, TAM_CELDA))
imagenPerro = pygame.image.load('iconos\perro_plateado.png').convert_alpha()
imagenPerro = pygame.transform.scale(imagenPerro, (TAM_CELDA, TAM_CELDA))
imagengato = pygame.image.load('iconos\gato_plateado.png').convert_alpha()
imagengato = pygame.transform.scale(imagengato, (TAM_CELDA, TAM_CELDA))
imagenCabal = pygame.image.load('iconos\caballo_plateado.png').convert_alpha()
imagenCabal = pygame.transform.scale(imagenCabal, (TAM_CELDA, TAM_CELDA))

# Colocar piezas en el tablero fichas doradas
y = 7
for x in range(len(tablero2[y])):
    tablero2[y][x] =  piece.Conejo(1, "dorado", x, y)
tablero2[6][0] = piece.Piece("gato", 2, "dorado", 0, 6)      
tablero2[6][7] = piece.Piece("gato", 2, "dorado", 7, 6) 
tablero2[6][1] = piece.Piece("perro", 3, "dorado", 1, 6)     
tablero2[6][6] = piece.Piece("perro", 3, "dorado", 6, 6)
tablero2[6][2] = piece.Piece("caballo", 4, "dorado", 2, 6)
tablero2[6][5] = piece.Piece("caballo", 4, "dorado", 5, 6)
tablero2[6][3] = piece.Piece("camello", 5, "dorado", 3, 6) 
tablero2[6][4] = piece.Piece("elefante", 6, "dorado", 4, 6)  

# Cargar imágenes de las piezas doradas
imagenConeD = pygame.image.load('iconos/conejo_dorado.png').convert_alpha()
imagenConeD = pygame.transform.scale(imagenConeD, (TAM_CELDA, TAM_CELDA))
imagenElefD = pygame.image.load('iconos\elefante_dorado.png').convert_alpha()
imagenElefD = pygame.transform.scale(imagenElefD, (TAM_CELDA, TAM_CELDA))
imagenCameD = pygame.image.load('iconos\camello_dorado.png').convert_alpha()
imagenCameD = pygame.transform.scale(imagenCameD, (TAM_CELDA, TAM_CELDA))
imagenPerroD = pygame.image.load('iconos\perro_dorado.png').convert_alpha()
imagenPerroD = pygame.transform.scale(imagenPerroD, (TAM_CELDA, TAM_CELDA))
imagengatoD = pygame.image.load('iconos\gato_dorado.png').convert_alpha()
imagengatoD = pygame.transform.scale(imagengatoD, (TAM_CELDA, TAM_CELDA))
imagenCabalD = pygame.image.load('iconos\caballo_dorado.png').convert_alpha()
imagenCabalD = pygame.transform.scale(imagenCabalD, (TAM_CELDA, TAM_CELDA))

# Diccionario con imágenes de las piezas
imagenes_animales = {
    "plateado": {
        "conejo": imagenCone,
        "elefante": imagenElef,
        "camello": imagenCame,
        "perro": imagenPerro,
        "gato": imagengato,
        "caballo": imagenCabal
    },
    "dorado": {
        "conejo": imagenConeD,
        "elefante": imagenElefD,
        "camello": imagenCameD,
        "perro": imagenPerroD,
        "gato": imagengatoD,
        "caballo": imagenCabalD
    }
}


def imprimir_tablero(tablero):
    for row in tablero:
        print(" ".join(str(cell) if cell != " " else "." for cell in row))

# Función para pintar el tablero
def Pintar(tablero):
    for y in range(len(tablero)):
        for x in range(len(tablero[y])):
            # Dibuja celdas vacías
            if tablero[y][x] == " ":
                pygame.draw.rect(pantalla, CAFE, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA))
                pygame.draw.rect(pantalla, VINOTINTO, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)
            elif isinstance(tablero[y][x], piece.Piece):
                # Dibuja celda con una pieza
                pygame.draw.rect(pantalla, CAFE, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA))
                pygame.draw.rect(pantalla, VINOTINTO, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)

                # Obtener la pieza, el animal y el color
                pieza = tablero[y][x]
                animal = pieza.animal
                color = pieza.color

                # Verificar que haya una imagen para el color y el animal
                if color in imagenes_animales and animal in imagenes_animales[color]:
                    pantalla.blit(imagenes_animales[color][animal], (x * TAM_CELDA, y * TAM_CELDA))
            elif tablero[y][x] == "0":
                pygame.draw.rect(pantalla, VINOTINTO, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA))
                pygame.draw.rect(pantalla, VINOTINTO, (x * TAM_CELDA, y * TAM_CELDA, TAM_CELDA, TAM_CELDA), 1)

    pygame.display.flip()   

# Variable para controlar si es el turno del jugador o de la IA
es_turno_jugador = True

# Bucle principal
Pintar(tablero2)
imprimir_tablero(tablero2)
movimientos_restantes = 4  # Máximo de movimientos por turno
movimiento_conejo_realizado = False  # Variable para controlar el movimiento de los conejos

# Variable para controlar si se ha mostrado el mensaje del turno del jugador
mensaje_mostrado = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if es_turno_jugador:
            # Imprimir el mensaje solo una vez al inicio del turno del jugador
            if not mensaje_mostrado:
                print("Es tu turno. Realiza tus movimientos.")  # Mensaje único
                mensaje_mostrado = True
            
            # Turno del jugador
            # Dentro del bucle principal, en el turno del jugador
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del mouse
                    if pos1 is None:  # Primer clic, selecciona la pieza
                        pos1 = event.pos
                    elif pos2 is None and pos1 is not None:  # Segundo clic, intenta mover la pieza
                        pos2 = event.pos
                        posicion1, posicion2, _ = obtener_posicion(pos1, pos2)
                        print(f"Posiciones capturadas: {posicion1}, {posicion2}")
                        
                        # Obtener la pieza en la posición inicial
                        pieza = tablero2[posicion1[1]][posicion1[0]]

                        # Verificar si la pieza seleccionada pertenece al jugador
                        if isinstance(pieza, piece.Piece) and pieza.color == "dorado":
                            # Movimiento permitido solo para fichas doradas
                            if pieza.animal == "conejo" and not movimiento_conejo_realizado:
                                # Movimiento específico para conejos
                                tablero2 = reglas.mover_ficha(tablero2, posicion1, posicion2)
                                Pintar(tablero2)
                                movimientos_restantes -= 1
                                movimiento_conejo_realizado = True
                            else:
                                # Movimiento general para otras piezas
                                tablero2 = reglas.mover_ficha(tablero2, posicion1, posicion2)
                                Pintar(tablero2)
                                movimientos_restantes -= 1
                        else:
                            print("¡Movimiento inválido! No puedes mover piezas de la IA.")

                        # Limpiar posiciones clickeadas
                        pos1 = None
                        pos2 = None

                        # Verificar si el jugador agotó sus movimientos
                        if movimientos_restantes == 0:
                            print("Movimientos agotados. Turno finalizado.")
                            movimientos_restantes = 4
                            es_turno_jugador = False
                            mensaje_mostrado = False
                            movimiento_conejo_realizado = False

            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key) == "1":
                    if pos1 is None:  # Primer clic
                        pos1 = pygame.mouse.get_pos()
                    elif pos2 is None:  # Segundo clic
                        pos2 = pygame.mouse.get_pos()
                    elif pos3 is None:
                        pos3 = pygame.mouse.get_pos()
                        posicion1, posicion2, posicion3 = obtener_posicion(pos1, pos2, pos3)
                        print(f"Posiciones capturadas: {posicion1}, {posicion2}, {posicion3}") 
                        tablero2 = reglas.empujar_ficha(tablero2, posicion1, posicion2, posicion3)
                        Pintar(tablero2)
                        pos1 = None
                        pos2 = None
                        pos3 = None
                        movimientos_restantes -= 2
                if pygame.key.name(event.key) == "2":
                    if pos1 is None:  # Primer clic
                        pos1 = pygame.mouse.get_pos()
                    elif pos2 is None:  # Segundo clic
                        pos2 = pygame.mouse.get_pos()
                    elif pos3 is None:
                        pos3 = pygame.mouse.get_pos()
                        posicion1, posicion2, posicion3 = obtener_posicion(pos1, pos2, pos3)
                        print(f"Posiciones capturadas: {posicion1}, {posicion2}, {posicion3}") 
                        tablero2 = reglas.halar_ficha(tablero2, posicion1, posicion2, posicion3)
                        Pintar(tablero2)
                        pos1 = None
                        pos2 = None
                        pos3 = None
                        movimientos_restantes -= 2
                    
                if event.key == pygame.K_RETURN:  # Tecla Enter para finalizar el turno manualmente
                    print("Turno finalizado manualmente.")
                    movimientos_restantes = 4
                    es_turno_jugador = False
                    mensaje_mostrado = False  # Restablecer para el siguiente turno
                    movimiento_conejo_realizado = False  # Restablecer para el siguiente turno
        else:
            print("Es el turno de la IA...")
            movimientos_realizados_ia = 0

            for _ in range(4):  # Máximo 4 movimientos de la IA
                mejor_movimiento = ia.decidir_mejor_movimiento(tablero2, 3, "plateado")
                
                if mejor_movimiento:
                    if mejor_movimiento[0] == "mover":
                        _, pos_inicial, pos_final = mejor_movimiento
                        tablero2 = reglas.mover_ficha(tablero2, pos_inicial, pos_final)
                        print(f"IA movió de {pos_inicial} a {pos_final}")
                    elif mejor_movimiento[0] == "halar":
                        _, pos_ficha, pos_enemigo, pos_resultado = mejor_movimiento
                        tablero2 = reglas.halar_ficha(tablero2, pos_ficha, pos_enemigo, pos_resultado)
                        print(f"IA haló ficha de {pos_enemigo} a {pos_resultado} usando {pos_ficha}")
                    elif mejor_movimiento[0] == "empujar":
                        _, pos_ficha, pos_enemigo, pos_resultado = mejor_movimiento
                        tablero2 = reglas.empujar_ficha(tablero2, pos_ficha, pos_enemigo, pos_resultado)
                        print(f"IA empujó ficha de {pos_enemigo} a {pos_resultado} usando {pos_ficha}")
                    
                    Pintar(tablero2)
                    movimientos_realizados_ia += 1
                else:
                    print("La IA no encontró movimientos válidos.")
                    break  # Salir del bucle si no hay movimientos válidos

                if not mejor_movimiento:
                    print("La IA no encontró movimientos válidos, pasando turno.")
                    break

            # Finalizar turno de la IA
            es_turno_jugador = True
            mensaje_mostrado = False
            movimiento_conejo_realizado = False
            movimientos_restantes = 4
