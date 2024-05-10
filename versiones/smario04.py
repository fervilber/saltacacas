import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Plataformas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración del reloj
clock = pygame.time.Clock()
FPS = 60

# Cargar Fondo
background = pygame.image.load('assets/background.png')
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar Corazón
heart_image = pygame.image.load('assets/heart.png')
heart_image = pygame.transform.scale(heart_image, (30, 30))  # Ajustar tamaño del corazón

# Clase Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.lives = 3
        self.invulnerable = False  # Estado de invulnerabilidad
        self.invulnerable_time = 0  # Temporizador de invulnerabilidad

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Actualizar temporizador de invulnerabilidad
        if self.invulnerable:
            self.invulnerable_time -= 1
            if self.invulnerable_time <= 0:
                self.invulnerable = False

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

    def become_invulnerable(self, duration):
        self.invulnerable = True
        self.invulnerable_time = duration

# Clase Plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/platform.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = -3  # Velocidad horizontal

    def update(self):
        self.rect.x += self.speed_x

        # Reiniciar posición cuando sale de la pantalla
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# Clase Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/kk.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = random.randint(-5, -1)  # Velocidad aleatoria hacia la izquierda

    def update(self):
        self.rect.x += self.speed_x
        # Reiniciar posición cuando sale de la pantalla
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            self.speed_x = random.randint(-5, -1)  # Nueva velocidad aleatoria

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear plataformas
platform1 = Platform(100, 500)
platform2 = Platform(400, 400)
platform3 = Platform(250, 300)

platforms.add(platform1, platform2, platform3)
all_sprites.add(platform1, platform2, platform3)

# Función para crear enemigos
def create_enemy():
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT - 50)
    enemy = Enemy(x, y)
    enemies.add(enemy)
    all_sprites.add(enemy)

# Crear enemigos
create_enemy()
create_enemy()  # Crear más enemigos si es necesario

# Función para dibujar vidas
def draw_lives(surface, x, y, lives, image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 35 * i  # Espacio entre los corazones
        img_rect.y = y
        surface.blit(image, img_rect)

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

    # Manejar colisiones con plataformas
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.y = hits[0].rect.top - player.rect.height
        player.speed_y = 0

    # Manejar colisiones con enemigos
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_hits and not player.invulnerable:
        player.lives -= 1
        print(f"Lives left: {player.lives}")
        player.become_invulnerable(120)  # 2 segundos de invulnerabilidad
        if player.lives == 0:
            print("Game Over")
            running = False

    # Dibujar en la pantalla
    screen.blit(background, (0, 0))  # Dibujar el fondo
    all_sprites.draw(screen)
    draw_lives(screen, 10, 10, player.lives, heart_image)  # Dibujar vidas
    pygame.display.flip()

    # Controlar FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()
