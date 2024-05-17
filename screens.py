# screens.py

import sys
import pygame
#from main import *
from classes import *
from settings import *
from functions import read_high_score

def show_start_screen(screen, start_screen, player1_image, player2_image, player3_image):
    high_score_player, high_score = read_high_score()
    screen.blit(start_screen, (0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render('Press 1 for Player 1, 2 for Player 2, or 3 for Player 3', True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    
    if high_score_player:
        high_score_text = font.render(f'High Score: {high_score} by {high_score_player}', True, BLACK)
    else:
        high_score_text = font.render(f'High Score: {high_score}', True, BLACK)
    
    screen.blit(high_score_text,  (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 90))
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


def show_level_transition(screen, level):
    screen.fill((0, 0, 0))  # Fondo negro
    font = pygame.font.Font(None, 74)
    text = font.render(f'LEVEL {level}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Esperar 3 segundos