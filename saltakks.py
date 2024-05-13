# ultima version del juego 
import pygame
import sys
import random
import csv
from datetime import datetime

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego saltacacas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configuración del reloj
clock = pygame.time.Clock()
FPS = 60

# Cargar música y sonidos
#pygame.mixer.music.load('assets/background_music.mp3')
#pygame.mixer.music.play(-1)  # Reproducir en bucle
jump_sound = pygame.mixer.Sound('assets/cartoon-jump-6462.mp3')
shit_sound = pygame.mixer.Sound('assets/uh-ohh-38886.mp3')


# Cargar Fondo
#background = pygame.image.load('assets/fondo2.png')
#background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar Fondo alargado
background = pygame.image.load('assets/fondo_largo3.png')
background_width = background.get_width()
background_height = background.get_height()
background = pygame.transform.scale(background, (background_width, SCREEN_HEIGHT))
background_width = background.get_width()
background_height = background.get_height()

# Cargar Corazón
heart_image = pygame.image.load('assets/heart.png')
heart_image = pygame.transform.scale(heart_image, (40, 40))  # Ajustar tamaño del corazón

# Cargar Game Over
game_over_image = pygame.image.load('assets/game_over.png')
game_over_image = pygame.transform.scale(game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar Pantalla de Inicio e Imágenes de Jugadores
start_screen = pygame.image.load('assets/start_screen.png')
start_screen = pygame.transform.scale(start_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
player1_image = pygame.image.load('assets/player1.png').convert_alpha()
player1_image = pygame.transform.scale(player1_image, (60, 60))
player2_image = pygame.image.load('assets/player2.png').convert_alpha()
player2_image = pygame.transform.scale(player2_image, (60, 60))
player3_image = pygame.image.load('assets/player3.png').convert_alpha()
player3_image = pygame.transform.scale(player3_image, (60, 60))


# Función para crear fichero de puntuaciones máximas
def check_create_csv(file_name='high_scores.csv'):
    try:
        with open(file_name, 'r') as file:
            pass  # El archivo ya existe, no hacer nada
    except FileNotFoundError:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Player', 'Score'])  # Cabecera del CSV

def save_score(player_name, score, file_name='high_scores.csv'):
    scores = []
    try:
        # Leer las puntuaciones existentes
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            scores = list(reader)
    except FileNotFoundError:
        # Si el archivo no existe, crear uno nuevo más adelante
        pass

    # Añadir la nueva puntuación
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scores.append([date_str, player_name, str(score)])

    # Ordenar las puntuaciones de mayor a menor
    scores.sort(key=lambda x: int(x[2]), reverse=True)

    # Mantener solo las 20 mejores puntuaciones
    scores = scores[:20]

    # Escribir las puntuaciones ordenadas en el archivo
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Player', 'Score'])  # Escribir la cabecera
        writer.writerows(scores)

# Función para leer la puntuación más alta
def read_high_score(file_name='high_scores.csv'):
    try:
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            high_score = 0
            high_score_player = ''
            for row in reader:
                score = int(row[2])
                if score > high_score:
                    high_score = score
                    high_score_player = row[1]
        return high_score_player, high_score
    except FileNotFoundError:
        return 0

# Función para mostrar la pantalla de inicio
def show_start_screen():
    high_score_player, high_score = read_high_score()
    screen.blit(start_screen, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render('Press 1,2 or 3 to select Player', True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    #high_score_text = font.render(f'High Score: {high_score}', True, BLACK) # pinta la max puntuacion
    if high_score_player:
        high_score_text = font.render(f'High Score: {high_score} by {high_score_player}', True, BLACK)
    else:
        high_score_text = font.render(f'High Score: {high_score}', True, BLACK)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 90))
    pygame.display.flip()
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return player1_image, "Player 1"
                elif event.key == pygame.K_2:
                    return player2_image, "Player 2"
                elif event.key == pygame.K_3:
                    return player3_image, "Player 3"

# Seleccionar jugador
#player_image = show_start_screen()
player_image, player_name = show_start_screen()

# Variables de desplazamiento
background_x = 0
scroll_speed = 1  # Velocidad de desplazamiento del fondo

# Función para dibujar el fondo desplazado
def draw_background():
    global background_x
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + background_width, 0))
    background_x -= scroll_speed
    if background_x <= -background_width:
        background_x = 0  # Reiniciar desplazamiento al final de la imagen

# Clase Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image  # Usar la imagen seleccionada
        self.collision_image = pygame.image.load('assets/player_collision.png').convert_alpha()
        self.collision_image = pygame.transform.scale(self.collision_image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.lives = 4
        self.invulnerable = False  # Estado de invulnerabilidad
        self.invulnerable_time = 0  # Temporizador de invulnerabilidad
        self.points = 0  # Puntos del jugador

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
        self.image = pygame.image.load('assets/patinete.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (random.randint(100, 200) , 20))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = random.randint(-5, -2)  # Velocidad horizontal

    def update(self):
        self.rect.x += self.speed_x

        # Reiniciar posición cuando sale de la pantalla
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

# Clase Enemigo, las cacas
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

# Clase Fruta
class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y, fruit_type, speed_x):
        super().__init__()
        if fruit_type == 'bocadillo':
            self.image = pygame.image.load('assets/bocadillo.png').convert_alpha()
            self.value = 3
        else:
            self.image = pygame.image.load(f'assets/{fruit_type}.png').convert_alpha()
            self.value = 1
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = speed_x

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()

# Asegurar la creación del archivo CSV
check_create_csv()

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fruits = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear plataformas
platform1 = Platform(100, random.randint(400, 550) )#500)
platform2 = Platform(400, random.randint(100, 350) )#400)
#platform3 = Platform(250, 300)

platforms.add(platform1, platform2) #, platform3)
all_sprites.add(platform1, platform2) #, platform3)

# Función para crear enemigos
def create_enemy():
    x = SCREEN_WIDTH
    y = random.randint(0, SCREEN_HEIGHT - 50)
    enemy = Enemy(x, y)
    enemies.add(enemy)
    all_sprites.add(enemy)

# Crear enemigos
#create_enemy()
#create_enemy()  # Crear más enemigos si es necesario
# Crear un número aleatorio de enemigos al inicio del juego
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
        img_rect.x = x + 35 * i  # Espacio entre los corazones
        img_rect.y = y
        surface.blit(image, img_rect)

# Función para dibujar puntos
def draw_points(surface, points, x, y):
    font = pygame.font.Font(None, 48)  # Fuente grande
    text = font.render(f'Puntuación: {points}', True, RED)
    text_rect = text.get_rect()
    text_rect.topright = (x, y)
    surface.blit(text, text_rect)

# Inicializar temporizador de frutas
fruit_timer = 0
fruit_interval = 100  # Intervalo para crear frutas (en fotogramas)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
                jump_sound.play()
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
        fruit_timer = 0  # Reiniciar el temporizador

    # Manejar colisiones con plataformas
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.y = hits[0].rect.top - player.rect.height
        player.speed_y = 0

    # Manejar colisiones con enemigos
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_hits and not player.invulnerable:
        player.lives -= 1
        print(f"Vidas: {player.lives}")
        player.image = player.collision_image  # Cambiar a imagen de colisión
        player.become_invulnerable(120)  # 2 segundos de invulnerabilidad
        shit_sound.play()
        pygame.time.set_timer(pygame.USEREVENT, 1000)  # Temporizador de 0.5 segundos para restaurar la imagen original
        if player.lives == 0:
            print("Game Over")
            save_score(player_name, player.points)  # Guardar la puntuación al finalizar el juego
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
        print(f"Puntos: {player.points}")

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

