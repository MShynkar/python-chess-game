import pygame
import chess
import time
from constants import *

def draw_board(screen):
    colors = [LIGHT_BROWN, DARK_BROWN]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board, pieces):
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                screen.blit(pieces[piece.symbol()], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_clocks(screen, font, white_time, black_time, player_turn):
    white_time_str = time.strftime('%M:%S', time.gmtime(white_time))
    black_time_str = time.strftime('%M:%S', time.gmtime(black_time))
    white_color = BLACK if player_turn == chess.WHITE else WHITE
    black_color = BLACK if player_turn == chess.BLACK else WHITE

    white_text = font.render(f'White: {white_time_str}', True, white_color)
    black_text = font.render(f'Black: {black_time_str}', True, black_color)

    screen.fill(WHITE, pygame.Rect(0, HEIGHT, WIDTH, CLOCK_HEIGHT))
    screen.blit(white_text, (20, HEIGHT + 10))
    screen.blit(black_text, (WIDTH - black_text.get_width() - 20, HEIGHT + 10))

def draw_highlights(screen, board, selected_square):
    if selected_square is not None:
        for move in board.legal_moves:
            if move.from_square == selected_square:
                to_square = move.to_square
                col = chess.square_file(to_square)
                row = 7 - chess.square_rank(to_square)
                pygame.draw.circle(screen, HIGHLIGHT_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                                   SQUARE_SIZE // 5)

def draw_button(screen, button_rect, button_text):
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

def draw_analysis(screen, info_font, evaluation, best_line):
    info_rect = pygame.Rect(0, HEIGHT + BUTTON_HEIGHT, WIDTH, INFO_HEIGHT)
    screen.fill(INFO_BG_COLOR, info_rect)

    evaluation = evaluation / 100.0 if evaluation is not None else 0.0
    eval_text = info_font.render(f'Evaluation: {evaluation:.2f}', True, BLACK)
    line_text = info_font.render(f'Best Line: {best_line}', True, BLACK)
    
    eval_text_rect = eval_text.get_rect(topleft=(20, HEIGHT + BUTTON_HEIGHT + 10))
    line_text_rect = line_text.get_rect(topleft=(20, HEIGHT + BUTTON_HEIGHT + 40))

    screen.blit(eval_text, eval_text_rect)
    screen.blit(line_text, line_text_rect)
