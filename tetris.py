import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Constantes del juego
ANCHO_VENTANA = 800
ALTO_VENTANA = 650
ANCHO_TABLERO = 10
ALTO_TABLERO = 20
TAMAÑO_CELDA = 30
OFFSET_X = 50
OFFSET_Y = 20  # Movemos el tablero más arriba

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CYAN = (0, 255, 255)
AZUL = (0, 0, 255)
NARANJA = (255, 165, 0)
AMARILLO = (255, 255, 0)
VERDE = (0, 255, 0)
MORADO = (128, 0, 128)
ROJO = (255, 0, 0)
GRIS = (128, 128, 128)
AZUL_OSCURO = (20, 20, 60)
ROSA = (255, 20, 147)

# Formas de las piezas de Tetris
FORMAS = [
    # I - Pieza lineal
    [['.....',
      '..#..',
      '..#..',
      '..#..',
      '..#..'],
     ['.....',
      '.....',
      '####.',
      '.....',
      '.....']],
    
    # O - Cuadrado
    [['.....',
      '.....',
      '.##..',
      '.##..',
      '.....']],
    
    # T - Forma T
    [['.....',
      '.....',
      '.#...',
      '###..',
      '.....'],
     ['.....',
      '.....',
      '.#...',
      '.##..',
      '.#...'],
     ['.....',
      '.....',
      '.....',
      '###..',
      '.#...'],
     ['.....',
      '.....',
      '.#...',
      '##...',
      '.#...']],
    
    # S - Forma S
    [['.....',
      '.....',
      '.##..',
      '##...',
      '.....'],
     ['.....',
      '.#...',
      '.##..',
      '..#..',
      '.....']],
    
    # Z - Forma Z
    [['.....',
      '.....',
      '##...',
      '.##..',
      '.....'],
     ['.....',
      '..#..',
      '.##..',
      '.#...',
      '.....']],
    
    # J - Forma J
    [['.....',
      '.#...',
      '.#...',
      '##...',
      '.....'],
     ['.....',
      '.....',
      '#....',
      '###..',
      '.....'],
     ['.....',
      '.##..',
      '.#...',
      '.#...',
      '.....'],
     ['.....',
      '.....',
      '###..',
      '..#..',
      '.....']],
    
    # L - Forma L
    [['.....',
      '..#..',
      '..#..',
      '.##..',
      '.....'],
     ['.....',
      '.....',
      '###..',
      '#....',
      '.....'],
     ['.....',
      '##...',
      '.#...',
      '.#...',
      '.....'],
     ['.....',
      '.....',
      '..#..',
      '###..',
      '.....']]
]

COLORES_FORMAS = [CYAN, AMARILLO, MORADO, VERDE, ROJO, AZUL, NARANJA]

class Pieza:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.forma = random.choice(FORMAS)
        self.color = COLORES_FORMAS[FORMAS.index(self.forma)]
        self.rotacion = 0

    def imagen(self):
        return self.forma[self.rotacion]

    def rotar(self):
        self.rotacion = (self.rotacion + 1) % len(self.forma)

class Tetris:
    def __init__(self):
        self.tablero = [[0 for _ in range(ANCHO_TABLERO)] for _ in range(ALTO_TABLERO)]
        self.pieza_actual = self.nueva_pieza()
        self.siguiente_pieza = self.nueva_pieza()
        self.puntuacion = 0
        self.lineas_completadas = 0
        self.nivel = 1
        self.velocidad_caida = 500  # milisegundos
        self.tiempo_ultima_caida = pygame.time.get_ticks()
        self.game_over = False
        
        # Inicializar música
        try:
            # Crear una melodía simple usando tonos
            self.inicializar_musica()
        except:
            print("No se pudo cargar la música")

    def nueva_pieza(self):
        return Pieza(ANCHO_TABLERO // 2 - 2, 0)
    
    def inicializar_musica(self):
        # Inicializar el mixer para sonidos
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Crear sonidos simples para efectos
        self.sonido_linea = self.crear_sonido_linea()
        self.sonido_rotar = self.crear_sonido_rotar()
        
        # Reproducir música de fondo
        self.reproducir_musica_fondo()
    
    def crear_sonido_linea(self):
        # Crear un sonido simple para cuando se completa una línea
        import numpy as np
        duracion = 0.3
        sample_rate = 22050
        frames = int(duracion * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            # Sonido de línea completada (ascendente)
            freq = 440 + (time * 200)
            wave = 4096 * np.sin(freq * 2 * np.pi * time) * (1 - time/duracion)
            arr[i] = [wave, wave]
        
        return pygame.sndarray.make_sound(arr.astype(np.int16))
    
    def crear_sonido_rotar(self):
        # Crear un sonido simple para rotación
        import numpy as np
        duracion = 0.1
        sample_rate = 22050
        frames = int(duracion * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            time = float(i) / sample_rate
            # Sonido de rotación (corto y agudo)
            wave = 2048 * np.sin(800 * 2 * np.pi * time) * (1 - time/duracion)
            arr[i] = [wave, wave]
        
        return pygame.sndarray.make_sound(arr.astype(np.int16))
    
    def reproducir_musica_fondo(self):
        # Crear una melodía simple de fondo
        import numpy as np
        duracion = 4.0  # 4 segundos de música que se repetirá
        sample_rate = 22050
        frames = int(duracion * sample_rate)
        arr = np.zeros((frames, 2))
        
        # Melodía simple de Tetris (notas aproximadas)
        notas = [659, 494, 523, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 523, 587, 659, 523, 440, 440]
        tiempo_nota = duracion / len(notas)
        
        for nota_idx, freq in enumerate(notas):
            inicio = int(nota_idx * tiempo_nota * sample_rate)
            fin = int((nota_idx + 1) * tiempo_nota * sample_rate)
            
            for i in range(inicio, min(fin, frames)):
                time = float(i - inicio) / sample_rate
                # Crear onda con envelope
                envelope = 1 - (time / tiempo_nota) * 0.5
                wave = 1024 * np.sin(freq * 2 * np.pi * time) * envelope
                arr[i] = [wave, wave]
        
        # Convertir a sonido y reproducir en bucle
        musica = pygame.sndarray.make_sound(arr.astype(np.int16))
        pygame.mixer.Sound.play(musica, loops=-1)  # Reproducir infinitamente

    def es_posicion_valida(self, pieza, dx=0, dy=0, rotacion=None):
        if rotacion is None:
            rotacion = pieza.rotacion
        
        forma = pieza.forma[rotacion]
        
        for i, fila in enumerate(forma):
            for j, celda in enumerate(fila):
                if celda == '#':
                    x = pieza.x + j + dx
                    y = pieza.y + i + dy
                    
                    if x < 0 or x >= ANCHO_TABLERO or y >= ALTO_TABLERO:
                        return False
                    
                    if y >= 0 and self.tablero[y][x]:
                        return False
        
        return True

    def colocar_pieza(self, pieza):
        forma = pieza.imagen()
        for i, fila in enumerate(forma):
            for j, celda in enumerate(fila):
                if celda == '#':
                    x = pieza.x + j
                    y = pieza.y + i
                    if y >= 0:
                        self.tablero[y][x] = pieza.color

    def limpiar_lineas(self):
        lineas_a_limpiar = []
        for i, fila in enumerate(self.tablero):
            if all(celda != 0 for celda in fila):
                lineas_a_limpiar.append(i)
        
        for i in reversed(lineas_a_limpiar):
            del self.tablero[i]
            self.tablero.insert(0, [0 for _ in range(ANCHO_TABLERO)])
        
        lineas_limpiadas = len(lineas_a_limpiar)
        if lineas_limpiadas > 0:
            try:
                self.sonido_linea.play()
            except:
                pass
        
        self.lineas_completadas += lineas_limpiadas
        self.puntuacion += lineas_limpiadas * 100 * self.nivel
        
        # Aumentar nivel cada 10 líneas
        self.nivel = self.lineas_completadas // 10 + 1
        self.velocidad_caida = max(50, 500 - (self.nivel - 1) * 50)

    def mover_pieza(self, dx, dy):
        if self.es_posicion_valida(self.pieza_actual, dx, dy):
            self.pieza_actual.x += dx
            self.pieza_actual.y += dy
            return True
        return False

    def rotar_pieza(self):
        nueva_rotacion = (self.pieza_actual.rotacion + 1) % len(self.pieza_actual.forma)
        if self.es_posicion_valida(self.pieza_actual, rotacion=nueva_rotacion):
            self.pieza_actual.rotacion = nueva_rotacion
            try:
                self.sonido_rotar.play()
            except:
                pass

    def caida_automatica(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_ultima_caida > self.velocidad_caida:
            if not self.mover_pieza(0, 1):
                self.colocar_pieza(self.pieza_actual)
                self.limpiar_lineas()
                self.pieza_actual = self.siguiente_pieza
                self.siguiente_pieza = self.nueva_pieza()
                
                if not self.es_posicion_valida(self.pieza_actual):
                    self.game_over = True
            
            self.tiempo_ultima_caida = tiempo_actual

    def dibujar_tablero(self, pantalla):
        # Dibujar tablero
        for y in range(ALTO_TABLERO):
            for x in range(ANCHO_TABLERO):
                rect = pygame.Rect(x * TAMAÑO_CELDA + OFFSET_X, y * TAMAÑO_CELDA + OFFSET_Y, 
                                 TAMAÑO_CELDA, TAMAÑO_CELDA)
                if self.tablero[y][x]:
                    pygame.draw.rect(pantalla, self.tablero[y][x], rect)
                    # Añadir efecto de brillo
                    pygame.draw.rect(pantalla, BLANCO, rect, 1)
                else:
                    # Celdas vacías con transparencia
                    pygame.draw.rect(pantalla, (40, 40, 40, 100), rect)
                    pygame.draw.rect(pantalla, (80, 80, 80), rect, 1)

    def dibujar_pieza(self, pantalla, pieza):
        forma = pieza.imagen()
        for i, fila in enumerate(forma):
            for j, celda in enumerate(fila):
                if celda == '#':
                    x = (pieza.x + j) * TAMAÑO_CELDA + OFFSET_X
                    y = (pieza.y + i) * TAMAÑO_CELDA + OFFSET_Y
                    rect = pygame.Rect(x, y, TAMAÑO_CELDA, TAMAÑO_CELDA)
                    pygame.draw.rect(pantalla, pieza.color, rect)
                    # Añadir efecto de brillo a la pieza activa
                    pygame.draw.rect(pantalla, BLANCO, rect, 2)

    def dibujar_siguiente_pieza(self, pantalla):
        # Dibujar siguiente pieza
        forma = self.siguiente_pieza.imagen()
        for i, fila in enumerate(forma):
            for j, celda in enumerate(fila):
                if celda == '#':
                    x = 450 + j * 20
                    y = 100 + i * 20
                    rect = pygame.Rect(x, y, 20, 20)
                    pygame.draw.rect(pantalla, self.siguiente_pieza.color, rect)
                    pygame.draw.rect(pantalla, BLANCO, rect, 1)

    def dibujar_info(self, pantalla, fuente):
        # Información del juego
        texto_puntuacion = fuente.render(f"Puntuación: {self.puntuacion}", True, BLANCO)
        texto_lineas = fuente.render(f"Líneas: {self.lineas_completadas}", True, BLANCO)
        texto_nivel = fuente.render(f"Nivel: {self.nivel}", True, BLANCO)
        texto_siguiente = fuente.render("Siguiente:", True, BLANCO)
        
        pantalla.blit(texto_puntuacion, (450, 200))
        pantalla.blit(texto_lineas, (450, 230))
        pantalla.blit(texto_nivel, (450, 260))
        pantalla.blit(texto_siguiente, (450, 70))

def dibujar_fondo_degradado(pantalla):
    # Crear un fondo degradado bonito
    for y in range(ALTO_VENTANA):
        # Degradado de azul oscuro a negro
        ratio = y / ALTO_VENTANA
        r = int(20 * (1 - ratio))
        g = int(20 * (1 - ratio))
        b = int(60 * (1 - ratio))
        color = (r, g, b)
        pygame.draw.line(pantalla, color, (0, y), (ANCHO_VENTANA, y))

def main():
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Tetris")
    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 36)
    fuente_grande = pygame.font.Font(None, 72)
    
    juego = Tetris()
    
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            
            elif evento.type == pygame.KEYDOWN and not juego.game_over:
                if evento.key == pygame.K_LEFT:
                    juego.mover_pieza(-1, 0)
                elif evento.key == pygame.K_RIGHT:
                    juego.mover_pieza(1, 0)
                elif evento.key == pygame.K_DOWN:
                    juego.mover_pieza(0, 1)
                elif evento.key == pygame.K_UP:
                    juego.rotar_pieza()
                elif evento.key == pygame.K_SPACE:
                    # Caída rápida
                    while juego.mover_pieza(0, 1):
                        pass
            
            elif evento.type == pygame.KEYDOWN and juego.game_over:
                if evento.key == pygame.K_r:
                    juego = Tetris()  # Reiniciar juego
        
        if not juego.game_over:
            juego.caida_automatica()
        
        # Dibujar todo
        dibujar_fondo_degradado(pantalla)
        
        # Dibujar borde del tablero con efecto brillante
        borde_rect = pygame.Rect(OFFSET_X - 2, OFFSET_Y - 2, 
                               ANCHO_TABLERO * TAMAÑO_CELDA + 4, 
                               ALTO_TABLERO * TAMAÑO_CELDA + 4)
        pygame.draw.rect(pantalla, ROSA, borde_rect, 3)
        pygame.draw.rect(pantalla, BLANCO, borde_rect, 1)
        
        juego.dibujar_tablero(pantalla)
        
        if not juego.game_over:
            juego.dibujar_pieza(pantalla, juego.pieza_actual)
        
        juego.dibujar_siguiente_pieza(pantalla)
        juego.dibujar_info(pantalla, fuente)
        
        if juego.game_over:
            texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
            texto_reiniciar = fuente.render("Presiona R para reiniciar", True, BLANCO)
            pantalla.blit(texto_game_over, (ANCHO_VENTANA // 2 - 150, ALTO_VENTANA // 2 - 50))
            pantalla.blit(texto_reiniciar, (ANCHO_VENTANA // 2 - 120, ALTO_VENTANA // 2))
        
        # Instrucciones con mejor estilo
        instrucciones = [
            "🎮 Controles:",
            "← → Mover",
            "↓ Bajar",
            "↑ Rotar", 
            "Espacio: Caída rápida"
        ]
        
        for i, instruccion in enumerate(instrucciones):
            color = ROSA if i == 0 else BLANCO
            fuente_usar = fuente if i == 0 else pygame.font.Font(None, 24)
            texto = fuente_usar.render(instruccion, True, color)
            pantalla.blit(texto, (450, 350 + i * 25))
        
        pygame.display.flip()
        reloj.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()