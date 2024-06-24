import pygame
import chess
import time
import argparse
from constants import *
from draw import draw_board, draw_pieces, draw_clocks, draw_highlights, draw_button
from utils import save_fen, display_message

parser = argparse.ArgumentParser(description="Two Player Chess Game with Clock")
parser.add_argument('--time', type=int, help="Time for each player (seconds)")
parser.add_argument('--fen', type=str, help="FEN string for the starting position")
args = parser.parse_args()

pygame.init()

TOTAL_TIME = args.time if args.time else 10 * 60

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

screen = pygame.display.set_mode((WIDTH, HEIGHT + CLOCK_HEIGHT + BUTTON_HEIGHT))
pygame.display.set_caption("2-Player Chess with Clock")

board = chess.Board(args.fen) if args.fen else chess.Board()

font = pygame.font.Font(None, 36)
button_rect = pygame.Rect((WIDTH // 2 - 50, HEIGHT + CLOCK_HEIGHT + 10, 100, 30))
button_text = font.render('Save FEN', True, BUTTON_TEXT_COLOR)

def main():
    running = True
    selected_square = None
    player_turn = chess.WHITE

    white_time = TOTAL_TIME
    black_time = TOTAL_TIME
    last_time_update = time.time()

    while running:
        current_time = time.time()
        if player_turn == chess.WHITE:
            white_time -= current_time - last_time_update
        else:
            black_time -= current_time - last_time_update
        last_time_update = current_time

        if white_time <= 0:
            display_message(screen, font, "Black wins on time!", CLOCK_HEIGHT, WIDTH, HEIGHT)
            running = False
        elif black_time <= 0:
            display_message(screen, font, "White wins on time!", CLOCK_HEIGHT, WIDTH, HEIGHT)
            running = False

        if board.is_checkmate():
            winner = "White" if board.turn == chess.BLACK else "Black"
            display_message(screen, font, f"Checkmate! {winner} wins!", CLOCK_HEIGHT, WIDTH, HEIGHT)
            running = False
        elif board.is_stalemate():
            display_message(screen, font, "Stalemate! It's a draw!", CLOCK_HEIGHT, WIDTH, HEIGHT)
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                col = event.pos[0] // SQUARE_SIZE
                row = 7 - (event.pos[1] // SQUARE_SIZE)
                square = chess.square(col, row)

                if button_rect.collidepoint(event.pos):
                    save_fen(board)
                elif selected_square is None:
                    if board.piece_at(square) and board.color_at(square) == player_turn:
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        player_turn = not player_turn
                        last_time_update = time.time()
                    selected_square = None

        draw_board(screen)
        draw_highlights(screen, board, selected_square)
        draw_pieces(screen, board, pieces)
        draw_clocks(screen, font, white_time, black_time, player_turn)
        draw_button(screen, button_rect, button_text)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
