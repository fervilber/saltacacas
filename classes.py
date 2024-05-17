# classes.py

import pygame
import random
import os
import sys
from settings import *
#from main import resource_path

# esta funcion es importante de cara a hacer después el ejecutable
# y que la ruta a los archivos siempre funcione
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, collision_image):
        super().__init__()
        self.image = image
        self.collision_image = collision_image
        self.collision_image = pygame.transform.scale(self.collision_image, (PLAYER_BOX+20,PLAYER_BOX+20))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # donde se coloca inicialmente el personaje en la pantalla
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.lives = VIDAS
        self.invulnerable = False  # Estado de invulnerabilidad
        self.invulnerable_time = 0  # Temporizador de invulnerabilidad
        self.points = 0  # Puntos del jugador

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

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
        self.image = pygame.image.load(resource_path('assets/platform.png')).convert_alpha()
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
        self.image = pygame.image.load(resource_path('assets/kk.png')).convert_alpha()
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
            self.image = pygame.image.load(resource_path('assets/bocadillo.png')).convert_alpha()
            self.value = 3
        else:
            self.image = pygame.image.load(resource_path(f'assets/{fruit_type}.png')).convert_alpha()
            self.value = 1
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed_x = speed_x

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.kill()
