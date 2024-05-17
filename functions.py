# functions.py

import csv
from datetime import datetime
import pygame
import sys

def check_create_csv(file_name='high_scores.csv'):
    try:
        with open(file_name, 'r') as file:
            pass  # El archivo ya existe, no hacer nada
    except FileNotFoundError:
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Player', 'Score'])  # Cabecera del CSV

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
        return None, 0

def get_player_name(screen, prompt):
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(300, 300, 200, 36)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(prompt + text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text

def save_score(player_name, score, screen, file_name='high_scores.csv'):
    scores = []
    try:
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la cabecera
            scores = list(reader)
    except FileNotFoundError:
        pass

    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    scores.append([date_str, player_name, str(score)])

    scores.sort(key=lambda x: int(x[2]), reverse=True)

    # Verificar si la nueva puntuación está entre las 5 mejores
    new_score_index = scores.index([date_str, player_name, str(score)]) # indice de la nueva entrada
    if new_score_index < 5: # verifica si está entre las 5 primeras
        player_name = get_player_name(screen, "Enter your name: ")
        scores[new_score_index] = [date_str, player_name, str(score)]

    scores = scores[:20]

    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Player', 'Score'])
        writer.writerows(scores)

