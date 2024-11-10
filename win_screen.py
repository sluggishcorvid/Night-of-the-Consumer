import pygame

 # Function to display a "Game Win" message
def display_win_screen(display, restart_button, restart_rect):
    font = pygame.font.Font("Melted Monster.ttf", 50)
    message_text = font.render("All fruit eaten! You win!", True, (255, 255, 191))
    message_rect = message_text.get_rect(center=(400, 400))
    display.blit(message_text, message_rect)
    display.blit(restart_button, restart_rect)
    pygame.display.flip()