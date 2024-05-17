# main.py

import pygame
import sys
import os
import random
#import csv
#from datetime import datetime
from settings import *
from functions import * #check_create_csv, save_score
from classes import *
import screens

# esta funcion es importante de cara a hacer después el ejecutable
# y que la ruta a los archivos siempre funcione
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Inicialización de Pygame
pygame.init()
clock = pygame.time.Clock()
current_level = 1
# Configuración de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego Salta cacas")

# Cargar música y sonidos
# Cargar sonidos del juego
jump_sound = pygame.mixer.Sound(resource_path('assets/cartoon-jump-6462.mp3'))
shit_sound = pygame.mixer.Sound(resource_path('assets/uh-ohh-38886.mp3'))
# Cargar Música de Fondo
pygame.mixer.music.load(resource_path('assets/hip-hop-rock-beats-118000.mp3'))
# Ajustar el Volumen de la Música de Fondo
pygame.mixer.music.set_volume(0.5)  # Valor entre 0.0 y 1.0
# Reproducir la música de Fondo en bucle
pygame.mixer.music.play(-1)

# Cargar Imágenes
#background = pygame.image.load('assets/background.png')
#background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
heart_image = pygame.image.load(resource_path('assets/heart.png'))
heart_image = pygame.transform.scale(heart_image, (30, 30))
game_over_image = pygame.image.load(resource_path('assets/game_over.png'))
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_screen = pygame.image.load(resource_path('assets/start_screen.png'))
start_screen = pygame.transform.scale(start_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
player1_image = pygame.image.load(resource_path('assets/player1.png')).convert_alpha()
player1_image = pygame.transform.scale(player1_image, (PLAYER_BOX, PLAYER_BOX))
player2_image = pygame.image.load(resource_path('assets/player2.png')).convert_alpha()
player2_image = pygame.transform.scale(player2_image, (PLAYER_BOX, PLAYER_BOX))
player3_image = pygame.image.load(resource_path('assets/player3.png')).convert_alpha()
player3_image = pygame.transform.scale(player3_image, (PLAYER_BOX, PLAYER_BOX))

# Cargar Fondo alargado
background = pygame.image.load(resource_path('assets/background.png'))
background_phase2 = pygame.image.load(resource_path('assets/background_phase2.png'))  # Fondo del nivel 2

background_width = background.get_width()
background_height = background.get_height()
background = pygame.transform.scale(background, (background_width, SCREEN_HEIGHT)) # escala el alto
#background_width = background.get_width()
background_height = background.get_height()

# Función para dibujar el fondo desplazado necesita import screens
def draw_background():
    global background_x
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + background_width, 0))
    background_x -= scroll_speed
    if background_x <= -background_width:
        background_x = 0  # Reiniciar desplazamiento al final de la imagen

# Asegurar la creación del archivo CSV
check_create_csv()

# Seleccionar jugador
player_image, player_name = screens.show_start_screen(screen, start_screen, player1_image, player2_image, player3_image)

# Crear jugador
player = Player(player_image, pygame.image.load(resource_path('assets/player_collision.png')).convert_alpha())

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fruits = pygame.sprite.Group()

all_sprites.add(player)

# Crear plataformas
platform1 = Platform(100, random.randint(400, 550) )
platform2 = Platform(400, random.randint(100, 350) )
platforms.add(platform1, platform2)
all_sprites.add(platform1, platform2)

# Función para crear enemigos
def create_enemy():
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT - 50)
    enemy = Enemy(x, y)
    enemies.add(enemy)
    all_sprites.add(enemy)

# Crear enemigos al inicio del juego
num_enemies = random.randint(2, 5)
for _ in range(num_enemies):
    create_enemy()

# Función para crear frutas
def create_fruit():
    x = SCREEN_WIDTH # lado derecho de la pantalla
    y = random.randint(0, SCREEN_HEIGHT - 30) # cualquier punto de la vertical 
    fruit_type = random.choice(['apple', 'banana', 'grape', 'tomato','bocadillo'])
    speed_x = random.randint(-3, -1)  # Velocidad aleatoria hacia la izquierda
    fruit = Fruit(x, y, fruit_type, speed_x)
    fruits.add(fruit)
    all_sprites.add(fruit)

# Crear frutas
create_fruit()
create_fruit() 
create_fruit()

# Función para dibujar vidas
def draw_lives(surface, x, y, lives, image):
    for i in range(lives):
        img_rect = image.get_rect()
        img_rect.x = x + 35 * i # Espacio entre los corazones
        img_rect.y = y
        surface.blit(image, img_rect)

# Función para dibujar puntos
def draw_points(surface, points, x, y):
    font = pygame.font.Font(None, 48) # Fuente grande
    text = font.render(f'Points: {points}', True, RED)
    text_rect = text.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text, text_rect)

# Inicializar temporizador de frutas
fruit_timer = 0
fruit_interval = 100 # Intervalo para crear frutas (en fotogramas)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                jump_sound.play() # sonido del salto
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.stop()
        elif event.type == pygame.USEREVENT:
            player.image = player_image  # Restaurar a la imagen seleccionada
            pygame.time.set_timer(pygame.USEREVENT, 0)  # Detener el temporizador

    # Actualizar sprites
    all_sprites.update()
    
    # Crear frutas periódicamente
    fruit_timer += 1
    if fruit_timer >= fruit_interval:
        create_fruit()
        fruit_timer = 0
        
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
        player.image = player.collision_image # Cambiar a imagen de colisión
        player.become_invulnerable(120)  # 2 segundos de invulnerabilidad
        shit_sound.play() # Sonido al pisar una caca
        pygame.time.set_timer(pygame.USEREVENT, 1000) # Temporizador de 1 segundos para restaurar la imagen original
        if player.lives == 0:
            print("Game Over")
            save_score(player_name, player.points, screen)  # Guardar y ordenar la puntuación
            # Mostrar pantalla de GAME OVER
            screen.blit(game_over_image, (0, 0))
            draw_points(screen, player.points, (SCREEN_WIDTH // 2) + 100 , (SCREEN_HEIGHT // 2) + 100)  # Dibujar puntos
            pygame.display.flip() 
            pygame.time.wait(3000)  # Esperar 3 segundos antes de cerrar
            running = False

    # Manejar colisiones con frutas
    fruit_hits = pygame.sprite.spritecollide(player, fruits, True)
    for fruit in fruit_hits:
        player.points += fruit.value
        print(f"Points: {player.points}")

    #segunda fase del juego
    if player.points >= 30 and current_level == 1:
        screens.show_level_transition(screen, 2)
        current_level += current_level
        player.lives = player.lives + 3
        FPS = FPS + 30  # Aumentar la velocidad general
        background_width = background_phase2.get_width()
        background_height = background_phase2.get_height()
        background = pygame.transform.scale(background_phase2, (background_width, SCREEN_HEIGHT)) # escala el alto
        background_height = background.get_height()
        
    # Dibujar en la pantalla
    draw_background()  # Dibujar el fondo desplazado
    #screen.blit(background, (0, 0))  # Dibujar el fondo
    all_sprites.draw(screen)
    draw_lives(screen, 10, 10, player.lives, heart_image)  # Dibujar vidas
    draw_points(screen, player.points, SCREEN_WIDTH -10, 10)  # Dibujar puntos
    pygame.display.flip()

    # Controlar FPS
    clock.tick(FPS)

pygame.quit()
sys.exit()
