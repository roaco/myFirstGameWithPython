import pygame
import random

# Inicializar Pygame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)

# Tamaño de la ventana
ANCHO = 800
ALTO = 600

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Breakout")

# Clase para la pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.velocidad = [random.randint(4,8), random.randint(-8,8)]

    def update(self):
        self.rect.x += self.velocidad[0]
        self.rect.y += self.velocidad[1]

        if self.rect.x > ANCHO - 10 or self.rect.x < 0:
            self.velocidad[0] = -self.velocidad[0]
        if self.rect.y > ALTO - 10 or self.rect.y < 0:
            self.velocidad[1] = -self.velocidad[1]

# Clase para la pala
class Pala(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([75, 10])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = ANCHO // 2 - 37
        self.rect.y = ALTO - 50
        self.velocidad = 0

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > ANCHO - 75:
            self.rect.x = ANCHO - 75

# Clase para los bloques
class Bloque(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([75, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Crear los bloques
bloques = pygame.sprite.Group()
for fila in range(5):
    for columna in range(10):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        bloque = Bloque(color, columna * 75, fila * 20 + 50)
        bloques.add(bloque)

# Crear los sprites
pelota = Pelota()
pala = Pala()
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(pelota)
todos_los_sprites.add(pala)
todos_los_sprites.add(bloques)

# Fuente de texto
fuente = pygame.font.Font(None, 36)

# Variables para el juego
vidas = 3
puntos = 0

# Bucle principal del juego
hecho = False
reloj = pygame.time.Clock()

while not hecho:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            hecho = True
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                pala.velocidad = -8
            elif evento.key == pygame.K_RIGHT:
                pala.velocidad = 8
        elif evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                pala.velocidad = 0

    # Actualizar los sprites
    todos_los_sprites.update()

    # Colisiones de la pelota con la pala
    if pygame.sprite.collide_rect(pelota, pala):
        pelota.velocidad[1] = -pelota.velocidad[+1]

    # Colisiones de la pelota con los bloques
    bloques_rotos = pygame.sprite.spritecollide(pelota, bloques, True)
    if bloques_rotos:
        pelota.velocidad[1] = -pelota.velocidad[1]
        puntos += len(bloques_rotos)
        if len(bloques) == 0:
            hecho = True

    # Si la pelota se va por debajo de la pantalla
    if pelota.rect.y > ALTO:
        vidas -= 1
        if vidas == 0:
            hecho = True
        else:
            pelota.rect.x = ANCHO // 2 - 5
            pelota.rect.y = ALTO // 2 - 5
            pelota.velocidad = [random.randint(4,8), random.randint(-8,8)]

    # Dibujar la pantalla
    pantalla.fill(NEGRO)
    todos_los_sprites.draw(pantalla)

    # Dibujar texto en la pantalla
    texto_vidas = fuente.render("Vidas: {}".format(vidas), True, BLANCO)
    pantalla.blit(texto_vidas, (10, 10))
    texto_puntos = fuente.render("Puntos: {}".format(puntos), True, BLANCO)
    pantalla.blit(texto_puntos, (ANCHO - 150, 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar el número de frames por segundo
    reloj.tick(60)

# Salir del juego
pygame.quit()