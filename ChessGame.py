

print("Tervetuloa pelaamaan Shakkia!" )

import pygame
pygame.init()

import sys
from pygame.locals import *
import pickle
import time
import random






# Vakiot
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CELL_SIZE = 100

CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE


WHITE_SQUARE = (155, 155, 155)
WHITE_PIECE = (200, 200, 200)
BLACK_SQUARE = (70, 70, 70)
BLACK_PIECE = (50, 50, 50)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 10




# Pelin alustus
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Shakkipeli')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

White_Piece_icons = {
    'pawn': pygame.image.load('white_pawn.png').convert_alpha(),
    'knight': pygame.image.load('white_knight.png').convert_alpha(),
    'bishop': pygame.image.load('white_bishop.png').convert_alpha(),
    'rook': pygame.image.load('white_rook.png').convert_alpha(),
    'queen': pygame.image.load('white_queen.png').convert_alpha(),
    'king': pygame.image.load('white_king.png').convert_alpha()
}

Black_Piece_icons = {
    'pawn': pygame.image.load('black_pawn.png').convert_alpha(),
    'rook': pygame.image.load('black_rook.png').convert_alpha(),
    'knight': pygame.image.load('black_knight.png').convert_alpha(),
    'queen': pygame.image.load('black_queen.png').convert_alpha(),
    'king': pygame.image.load('black_king.png').convert_alpha(),
    'bishop': pygame.image.load('black_bishop.png').convert_alpha()
}

start_time = time.time()
game_over = False

start_square = None
end_square = None
selected_piece = None
selected_square = None


def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

class Piece:
    def __init__(self, name, color, position):
        self.name = name
        self.color = color
        self.position = position  # (x, y) tuple

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.color == 'white':
            if self.name in White_Piece_icons:
                icon = White_Piece_icons[self.name]
                icon = pygame.transform.scale(icon, (CELL_SIZE - 20, CELL_SIZE - 20))
                icon_rect = icon.get_rect(center=rect.center)
                surface.blit(icon, icon_rect)
            else:
                pygame.draw.circle(surface, WHITE_PIECE, rect.center, CELL_SIZE // 3)
        else:
            if self.name in Black_Piece_icons:
                icon = Black_Piece_icons[self.name]
                icon = pygame.transform.scale(icon, (CELL_SIZE - 20, CELL_SIZE - 20))
                icon_rect = icon.get_rect(center=rect.center)
                surface.blit(icon, icon_rect)
            else:
                pygame.draw.circle(surface, BLACK_PIECE, rect.center, CELL_SIZE // 3)

Pieces = [
    Piece('rook', 'white', (0, 0)), 
    Piece('knight', 'white', (1, 0)),
    Piece('bishop', 'white', (2, 0)),
    Piece('queen', 'white', (3, 0)),
    Piece('king', 'white', (4, 0)),
    Piece('bishop', 'white', (5, 0)),
    Piece('knight', 'white', (6, 0)),
    Piece('rook', 'white', (7, 0)),
    Piece('pawn', 'white', (0, 1)),
    Piece('pawn', 'white', (1, 1)),
    Piece('pawn', 'white', (2, 1)),
    Piece('pawn', 'white', (3, 1)),
    Piece('pawn', 'white', (4, 1)),
    Piece('pawn', 'white', (5, 1)),
    Piece('pawn', 'white', (6, 1)), 
    Piece('pawn', 'white', (7, 1)),
    Piece('rook', 'black', (0, 7)),
    Piece('knight', 'black', (1, 7)),
    Piece('bishop', 'black', (2, 7)),
    Piece('queen', 'black', (3, 7)),
    Piece('king', 'black', (4, 7)),
    Piece('bishop', 'black', (5, 7)),
    Piece('knight', 'black', (6, 7)),
    Piece('rook', 'black', (7, 7)),
    Piece('pawn', 'black', (0, 6)),
    Piece('pawn', 'black', (1, 6)),
    Piece('pawn', 'black', (2, 6)),
    Piece('pawn', 'black', (3, 6)),
    Piece('pawn', 'black', (4, 6)),
    Piece('pawn', 'black', (5, 6)),
    Piece('pawn', 'black', (6, 6)), 
    Piece('pawn', 'black', (7, 6))
]


################### Main game loop ####################
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            selected_square = (event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE)
            if(selected_piece is None):
                for myPiece in Pieces:
                    if myPiece.position == selected_square:
                        selected_piece = myPiece
                        print("Piece selected:", myPiece.name, "at", selected_square)
            else:
                # Move the piece to the selected square
                # Check for valid move here (not implemented)

                if(selected_piece.position == selected_square):
                    print("Piece deselected:", selected_piece.name)
                    selected_piece = None
                    selected_square = None
                    break
                elif(selected_piece.name == 'pawn'):
                    if (selected_piece.color == 'white'):
                        
                        if(selected_square[1] == selected_piece.position[1] + 1 and selected_square[0] == selected_piece.position[0]):
                            selected_piece.position = selected_square
                            selected_piece = None
                        else:
                            print("Invalid move for pawn")
                    else:
                        if(selected_square[1] == selected_piece.position[1] - 1 and selected_square[0] == selected_piece.position[0]):
                            selected_piece.position = selected_square
                            selected_piece = None
                        else:
                            print("Invalid move for pawn")

                #selected_piece.position = selected_square
                #selected_piece = None

                #start_square = (event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE)
            #print("Start square selected:", start_square)
            #print("B")
        #print("C")

    if not game_over:
        # Päivitä pelin tila
        pass

    screen.fill(BLACK_SQUARE)
    for x in range(0,8):
        for y in range(0,8):
            if (selected_piece != None and selected_piece.position == (x,y)):
                pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif (x + y) % 2 == 0:
                pygame.draw.rect(screen, WHITE_SQUARE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, BLACK_SQUARE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    for myPiece in Pieces:
        myPiece.draw(screen)
 #   pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
 #   draw_text(f'Score: {score}', WHITE, 10, 10)
 #   draw_text(f'Highscore: {highscore}', WHITE, 400, 10)
    if game_over:
        draw_text('Game Over! Press R to Restart', RED, WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        keys = pygame.key.get_pressed()
        if keys[K_r]:
            score = 0
            start_time = time.time()
            game_over = False
    pygame.display.update()
    clock.tick(FPS)
