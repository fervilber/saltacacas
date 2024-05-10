# programa juego sencillo en python
# 
# pip install pygame
 
import pygame
import sys

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego salta kks")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración del reloj
clock = pygame.time.Clock()
FPS = 60

# Clase Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Limitar movimiento en los bordes
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0

    def jump(self):
        self.speed_y = -15

    def move_left(self):
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5

    def stop(self):
        self.speed_x = 0

# Clase Plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/platform.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear plataformas
platform1 = Platform(100, 500)
platform2 = Platform(400, 400)
platform3 = Platform(250, 300)

platforms.add(platform1, platform2, platform3)
all_sprites.add(platform1, platform2, platform3)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.stop()

    # Actualizar sprites
    all_sprites.update()

    # Manejar colisiones
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.y = hits[0].rect.top - player.rect.height
        player.speed_y = 0

    # Dibujar en la pantalla
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

    # Controlar FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()
