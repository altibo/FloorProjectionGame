import pygame
import sys

class Projector:
    def __init__(self, width=1280, height=720):
        # Use second monitor if available, otherwise fullscreen primary
        self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.NOFRAME)
        pygame.display.set_caption("Floor Projection")
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 48)
        
    def draw(self, game=None):
        self.screen.fill((20, 20, 40))  # dark background
        
        if game:
            game.draw(self.screen)
        else:
            text = self.font.render("Floor Projection Ready", True, (200, 200, 200))
            self.screen.blit(text, (self.width//2 - 150, self.height//2))
        
        # Score overlay if available
        if game and hasattr(game, 'score'):
            score_text = self.font.render(f"Score: {game.score}", True, (255, 255, 0))
            self.screen.blit(score_text, (20, 20))
