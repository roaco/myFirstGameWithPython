import pygame
import random
 
# Inicializar Pygame
pygame.init()
 
# Establecer el tamaño de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")
 
# Definir los colores que se utilizarán en el juego
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
 
# Definir la paleta del jugador
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([80, 10])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - 40
        self.rect.y = SCREEN_HEIGHT - 50
        self.speed = 0
 
    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
 
    def move_left(self):
        self.speed = -10 # Definimos velocidad de la barra
 
    def move_right(self):
        self.speed = 10 # Definimos velocidad de la barra
 
    def stop(self):
        self.speed = 0
 
# Definir el bloque
class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([48, 20])
        self.image.fill(color)
        self.rect = self.image.get_rect()
 
# Crear los bloques
all_sprites_list = pygame.sprite.Group()
block_list = pygame.sprite.Group()
for i in range(16): #Se establece la cantidad de filas
    for j in range(5): # Se establece la cantidad de columnas
        block = Block(RED)
        block.rect.x = i * (block.rect.width + 2) + 10
        block.rect.y = j * (block.rect.height + 2) + 10
        block_list.add(block)
        all_sprites_list.add(block)
 
# Crear la paleta del jugador
player_paddle = Paddle()
all_sprites_list.add(player_paddle)
 
# Definir la pelota
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - 5
        self.rect.y = SCREEN_HEIGHT - 70
        self.speed_x = 4 #DEFINIMOS VELOCIDAD DE LA PELOTA
        self.speed_y = -4 #DEFINIMOS VELOCIDAD DE LA PELOTA
 
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        elif self.rect.top < 0:
            self.speed_y = -self.speed_y
        elif self.rect.bottom > SCREEN_HEIGHT:
            pygame.quit()
            quit()
 
        # Colisión de la pelota con la paleta
        if pygame.sprite.collide_rect(self, player_paddle):
            self.speed_y = -self.speed_y
            self.speed_x +=  0.001 #DEFINIMOS AUMENTO EN LA VELOCIDAD DE LA PELOTA
            self.speed_y += - 0.001 #DEFINIMOS AUMENTO EN LA VELOCIDAD DE LA PELOTA
            
        # Colisión de la pelota con los bloques
        blocks_hit_list = pygame.sprite.spritecollide(self, block_list, True)
        for block in blocks_hit_list:
            global score
            score += 1
        if len(blocks_hit_list) > 0:
            self.speed_y = -self.speed_y
 
# Crear la pelota
ball = Ball()
all_sprites_list.add(ball)


# Definir el marcador y variables del juego
score = 0
life = 3
font = pygame.font.Font(None, 36)
 
# Bucle principal del juego
game_over = False
clock = pygame.time.Clock()
 
while not game_over:
    # Procesamiento de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_paddle.move_left()
            elif event.key == pygame.K_RIGHT:
                player_paddle.move_right()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player_paddle.speed < 0:
                player_paddle.stop()
            elif event.key == pygame.K_RIGHT and player_paddle.speed > 0:
                player_paddle.stop()
 
    # Actualizar objetos del juego
    all_sprites_list.update()
    
    
    
    
    
    
 
    # Verificar si la pelota ha golpeado la parte inferior de la pantalla
    if ball.rect.bottom > SCREEN_HEIGHT:
        life -= 1
        game_over = True
 
    # Dibujar objetos del juego
    screen.fill(BLACK)
    all_sprites_list.draw(screen)
    score_text = font.render("Score: {}".format(score), True, WHITE)
    life_text = font.render("Life: {}".format(life), True, WHITE)
    screen.blit(score_text, [10, 10])
    screen.blit(life_text, [10, 40])
    pygame.display.flip()
 
    # Establecer el límite de fotogramas
    clock.tick(60)
 
# Cerrar Pygame
pygame.quit()