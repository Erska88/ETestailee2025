

print("Tervetuloa matopeliin!")



import pygame

pygame.init()
import random
import sys
import time
from pygame.locals import *
import os
import pickle
import datetime

# Vakiot
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
FPS = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Pelin alustus
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Matopeli')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
highscore_file = 'highscore.pkl'
print("Tervetuloa matopeliin2!")

if os.path.exists(highscore_file):
    print("Tervetuloa matopeliin3!")

    with open(highscore_file, 'rb') as f:
        highscore = pickle.load(f)
else:
    print("Tervetuloa matopeliin4!")
    highscore = 0 

score = 0
start_time = time.time()
game_over = False
direction = 'RIGHT'
snake = [(CELL_WIDTH // 2, CELL_HEIGHT // 2)]

def place_food():
    while True:
        x = random.randint(0, CELL_WIDTH - 1)
        y = random.randint(0, CELL_HEIGHT - 1)
        if (x, y) not in snake:
            return (x, y)
food = place_food()
def save_highscore(score):
    with open(highscore_file, 'wb') as f:
        pickle.dump(score, f)
def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
while True:
    print("Tervetuloa matopeliin6!")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
    if not game_over:
        head_x, head_y = snake[0]
        if direction == 'UP':
            head_y -= 1
        elif direction == 'DOWN':
            head_y += 1
        elif direction == 'LEFT':
            head_x -= 1
        elif direction == 'RIGHT':
            head_x += 1
        new_head = (head_x, head_y)
        if (head_x < 0 or head_x >= CELL_WIDTH or
            head_y < 0 or head_y >= CELL_HEIGHT or
            new_head in snake):
            game_over = True
        else:
            snake.insert(0, new_head)
            if new_head == food:
                score += 10
                food = place_food()
            else:
                snake.pop()
    screen.fill(BLACK)
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    draw_text(f'Score: {score}', WHITE, 10, 10)
    draw_text(f'Highscore: {highscore}', WHITE, 400, 10)
    if game_over:
        draw_text('Game Over! Press R to Restart', RED, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        if score > highscore:
            highscore = score
            save_highscore(highscore)
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            score = 0
            start_time = time.time()
            game_over = False
            direction = 'RIGHT'
            snake = [(CELL_WIDTH // 2, CELL_HEIGHT // 2)]
            food = place_food()
    pygame.display.update()
    clock.tick(FPS)
with open(highscore_file, 'wb') as f:
    pickle.dump(highscore, f)
print("Uusi korkein pistemäärä tallennettu:", highscore)
print("Korkein pistemäärä:", highscore)
 
