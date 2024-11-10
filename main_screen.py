import pygame, sys

# Creates the title screen
class MainScreen:
    def title_screen(self, display, background, start_button, start_rect, exit_button, exit_rect, directions, directions_rect, main_font, main_font_pos, direction_font, direction_font_pos, direction_font_pos2):
        directionDisplay = False
        """Displays the title screen with interactive image buttons."""
        while True:
            display.blit(background, (0, 0))
            display.blit(start_button, start_rect)
            display.blit(exit_button, exit_rect)
            display.blit(directions, directions_rect)
            title_text = main_font.render("Night of the Consumer",
                                          True,
                                          (255, 255, 191))
            display.blit(title_text, title_text.get_rect(center=main_font_pos))

            if directionDisplay:
                directions_text = direction_font.render(
                    "Use the arrow keys or WASD to move and jump.",
                    True,
                    (255, 255, 191))
                display.blit(directions_text, directions_text.get_rect(center=direction_font_pos))
                directions_text2 = direction_font.render(
                    "Help monster consume all the fruits to win!",
                    True,
                    (255, 255, 191))
                display.blit(directions_text2, directions_text2.get_rect(center=direction_font_pos2))

        # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        return  # Exit title screen to start the game
                    elif exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif directions_rect.collidepoint(event.pos):
                        directionDisplay = True

            pygame.display.flip()


