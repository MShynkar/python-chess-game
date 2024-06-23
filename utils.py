import pygame
import time

def save_fen(board):
    fen = board.fen()
    with open('chess_position.fen', 'w') as f:
        f.write(fen)
    print("FEN saved to chess_position.fen")

def display_message(screen, font, message, clock_height, width, height):
    screen.fill((255, 255, 255), pygame.Rect(0, height, width, clock_height))
    message_text = font.render(message, True, (0, 0, 0))
    screen.blit(message_text, message_text.get_rect(center=(width // 2, height + clock_height // 2)))
    pygame.display.flip()
    time.sleep(3)
