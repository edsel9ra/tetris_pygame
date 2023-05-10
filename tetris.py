import pygame
import random

pygame.font.init()

#Varaibles Globales de la pantalla
ancho_pantalla = 800 #Ancho de la pantalla
alto_pantalla = 700 #Altura de la pantalla
ancho_zona_juego = 300  #Ancho de la zona el juego
alto_zona_juego = 600  #Altura de la zona del juego
tamanio_bloque = 30 #Tamanio de los bloques
 
plano_x = (ancho_pantalla - ancho_zona_juego) // 2
plano_y = alto_pantalla - alto_zona_juego

#Formato Formas

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

#Figuras Representadas en una lista con indices del 0 al 6
figuras=[S, Z, I, O, J, L, T]
#Color por cada figura en RGB
colores_figuras = [(0, 0, 139), (184, 134, 11), (0, 100, 0), (139, 0, 139), (85, 107, 47), (139, 0, 0), (0, 139, 139)]

class Pieza(object):
    filas = 20  # y
    columnas = 10  # x
 
    def __init__(self, columna, fila, figura):
        self.x = columna
        self.y = fila
        self.figura = figura
        self.color = colores_figuras[figuras.index(figura)]
        self.rotacion = 0  # Realiza 3 tipos de rotaciones, posicion inicial

def crearGrilla(posiciones_bloqueadas={}):
    grilla = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            if (j,i) in posiciones_bloqueadas:
                c = posiciones_bloqueadas[(j,i)]
                grilla[i][j] = c
    return grilla

def convertirFigura(figura):
    posiciones = []
    formato = figura.figura[figura.rotacion % len(figura.figura)]
 
    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                posiciones.append((figura.x + j, figura.y + i))
 
    for i, pos in enumerate(posiciones):
        posiciones[i] = (pos[0] - 2, pos[1] - 4)
 
    return posiciones

def validarEspacio(figura, grilla):
    posiciones_aceptadas = [[(j, i) for j in range(10) if grilla[i][j] == (0,0,0)] for i in range(20)]
    posiciones_aceptadas = [j for sub in posiciones_aceptadas for j in sub]
    formateado = convertirFigura(figura)
 
    for pos in formateado:
        if pos not in posiciones_aceptadas:
            if pos[1] > -1:
                return False
 
    return True

def validarPerdida(posiciones):
    for pos in posiciones:
        x, y = pos
        if y < 1:
            return True
    return False

def obtenerFigura():
    global figuras, colores_figuras
 
    return Pieza(5, 0, random.choice(figuras))

def dibujarTexto(texto, tamanio, color, superficie):
    fuente = pygame.font.SysFont('comicsans', tamanio)
    etiqueta = fuente.render(texto, 1, color)
 
    superficie.blit(etiqueta, (plano_x + ancho_zona_juego/2 - (etiqueta.get_width() / 2), plano_y + alto_zona_juego/2 - etiqueta.get_height()/2))

def dibujarGrilla(superficie, fila, col):
    sx = plano_x #Superficie X
    sy = plano_y #Superficie Y
    for i in range(fila):
        pygame.draw.line(superficie, (128,128,128), (sx, sy+ i*30), (sx + ancho_zona_juego, sy + i * 30)) #Lineas Horizontales
        for j in range(col):
            pygame.draw.line(superficie, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + alto_zona_juego)) #Lineas Verticals

def limpiarFilas(grilla, bloqueado):
    
    inc = 0
    for i in range(len(grilla)-1,-1,-1):
        fila = grilla[i]
        if (0, 0, 0) not in fila:
            inc += 1
            #Adiciona una posicion desde el bloqueado
            ind = i
            for j in range(len(fila)):
                try:
                    del bloqueado[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(bloqueado), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                nueva_llave = (x, y + inc)
                bloqueado[nueva_llave] = bloqueado.pop(key)

def dibujarProximaFigura(figura, superficie):
    fuente = pygame.font.SysFont('comicsans', 30)
    etiqueta = fuente.render('Próxima Figura:', 1, (255,255,255))
 
    sx = plano_x + ancho_zona_juego + 50
    sy = plano_y + alto_zona_juego/2 - 100
    formato = figura.figura[figura.rotacion % len(figura.figura)]
 
    for i, linea in enumerate(formato):
        fila = list(linea)
        for j, columna in enumerate(fila):
            if columna == '0':
                pygame.draw.rect(superficie, figura.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    superficie.blit(etiqueta, (sx + 10, sy- 30))

def dibujarVentana(superficie):
    superficie.fill((0,0,0))
    #Titulo Del Juego
    fuente = pygame.font.SysFont('comicsans', 60)
    etiqueta = fuente.render('TETRIS', 1, (255,255,255))
 
    superficie.blit(etiqueta, (plano_x + ancho_zona_juego / 2 - (etiqueta.get_width() / 2), 30))
 
    for i in range(len(grilla)):
        for j in range(len(grilla[i])):
            pygame.draw.rect(superficie, grilla[i][j], (plano_x + j* 30, plano_y + i * 30, 30, 30), 0)
 
    #Dibuja la grilla y su borde
    dibujarGrilla(superficie, 20, 10)
    pygame.draw.rect(superficie, (255, 0, 0), (plano_x, plano_y, ancho_zona_juego, alto_zona_juego), 5)

def main():
    global grilla
    posiciones_bloqueadas = {}  # (x,y):(255,0,0)
    grilla = crearGrilla(posiciones_bloqueadas)
    cambiar_pieza = False
    ejecutar = True
    pieza_actual = obtenerFigura()
    siguiente_pieza = obtenerFigura()
    reloj = pygame.time.Clock()
    tiempo_caida = 0
    while ejecutar:
        velocidad_caida = 0.3 #Velocidad de caida de la pieza

        grilla = crearGrilla(posiciones_bloqueadas)
        tiempo_caida += reloj.get_rawtime()
        reloj.tick()

        #Caida de las Piezas
        if tiempo_caida/1000 >= velocidad_caida:
            tiempo_caida = 0
            pieza_actual.y += 1
            if not (validarEspacio(pieza_actual, grilla)) and pieza_actual.y > 0:
                pieza_actual.y -= 1
                cambiar_pieza = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutar = False
                pygame.display.quit()
                quit()

              #Mueve la figura hacia la izquierda
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    pieza_actual.x -= 1
                    if not validarEspacio(pieza_actual, grilla):
                        pieza_actual.x += 1

                   #Mueve la figura hacia la derecha
                elif evento.key == pygame.K_RIGHT:
                    pieza_actual.x += 1
                    if not validarEspacio(pieza_actual, grilla):
                        pieza_actual.x -= 1
                elif evento.key == pygame.K_UP:
                    #Gira la figura
                    pieza_actual.rotacion = pieza_actual.rotacion + 1 % len(pieza_actual.figura)
                    if not validarEspacio(pieza_actual, grilla):
                        pieza_actual.rotacion = pieza_actual.rotacion - 1 % len(pieza_actual.figura)

                if evento.key == pygame.K_DOWN:
                    #Empujar la figura hacia abajo 
                    pieza_actual.y += 1
                    if not validarEspacio(pieza_actual, grilla):
                        pieza_actual.y -= 1

        posicion_figura = convertirFigura(pieza_actual)
        #Adiciona una pieza para ser dibujada en la grilla
        for i in range(len(posicion_figura)):
            x, y = posicion_figura[i]
            if y > -1:
                grilla[y][x] = pieza_actual.color

        #Si la figura llega la fondo de la pantalla
        if cambiar_pieza:
            for pos in posicion_figura:
                p = (pos[0], pos[1])
                posiciones_bloqueadas[p] = pieza_actual.color
            pieza_actual = siguiente_pieza
            siguiente_pieza = obtenerFigura()
            cambiar_pieza = False

            limpiarFilas(grilla, posiciones_bloqueadas)

        dibujarVentana(ganar)
        dibujarProximaFigura(siguiente_pieza, ganar)
        pygame.display.update()

        #Valida si el jugador perdio
        if validarPerdida(posiciones_bloqueadas):
            ejecutar = False

    dibujarTexto("Perdiste :(", 40, (255,255,255), ganar)
    pygame.display.update()
    pygame.time.delay(2000)

def main_menu():
    ejecutar = True
    while ejecutar:
        ganar.fill((0, 0, 0))
        dibujarTexto('Presiona cualquier tecla para empezar', 60, (255, 255, 255), ganar)
        pygame.display.update()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutar = False

            if evento.type == pygame.KEYDOWN:
                main()
    pygame.quit()


ganar = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption('Tetris')

main_menu()
