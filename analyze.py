import pygame
import chess
import time
from constants import *
from draw import draw_board, draw_pieces, draw_highlights, draw_button, draw_analysis

import chess.engine

pygame.init()

# Load piece images
pieces = {}
piece_files = {
    'p': 'black_pawn.png',
    'r': 'black_rook.png',
    'n': 'black_knight.png',
    'b': 'black_bishop.png',
    'q': 'black_queen.png',
    'k': 'black_king.png',
    'P': 'white_pawn.png',
    'R': 'white_rook.png',
    'N': 'white_knight.png',
    'B': 'white_bishop.png',
    'Q': 'white_queen.png',
    'K': 'white_king.png'
}
for piece, filename in piece_files.items():
    pieces[piece] = pygame.image.load(f'images/{filename}')

# Initialize chess board
board = chess.Board()

# Set up fonts
font = pygame.font.Font(None, 36)
info_font = pygame.font.Font(None, 28)

def request_analysis(board):
    # Request analysis from chess engine
    with chess.engine.SimpleEngine.popen_uci(PATH_TO_ENGINE) as engine:
        result = engine.analyse(board, chess.engine.Limit(depth=30))
        evaluation = result['score'].relative.score(mate_score=10000)
        best_line_moves = result['pv'][:10]  
        
        temp_board = board.copy()
        best_line = []
        for move in best_line_moves:
            best_line.append(temp_board.san(move))
            temp_board.push(move)

        return evaluation, ' '.join(best_line)

def main():
    # Set up game window
    screen = pygame.display.set_mode((WIDTH, HEIGHT + BUTTON_HEIGHT + INFO_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Chess with Analysis")

    # Set up button
    button_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT + 10, 200, 30))
    button_text = font.render('Request Analysis', True, BUTTON_TEXT_COLOR)
    
    running = True
    selected_square = None
    evaluation = None
    best_line = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    evaluation, best_line = request_analysis(board)
                else:
                    col = event.pos[0] // SQUARE_SIZE
                    row = 7 - (event.pos[1] // SQUARE_SIZE)
                    square = chess.square(col, row)
                    if selected_square is None:
                        if board.piece_at(square) and board.color_at(square) == board.turn:
                            selected_square = square
                    else:
                        move = chess.Move(selected_square, square)
                        if move in board.legal_moves:
                            board.push(move)
                        selected_square = None
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        # Draw game elements
        draw_board(screen)
        draw_highlights(screen, board, selected_square)
        draw_pieces(screen, board, pieces)
        draw_button(screen, button_rect, button_text)
        if evaluation is not None and best_line is not None:
            draw_analysis(screen, info_font, evaluation, best_line)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
