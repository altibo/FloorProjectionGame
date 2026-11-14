import pygame
import random

class DemoGame:
    def __init__(self, projector):
        self.score = 0
        self.just_scored = False
        self.fields = []
        self.field_size = 120
        self.cols = 6
        self.rows = 4
        self.init_fields(projector.width, projector.height)
        
    def init_fields(self, w, h):
        margin_x = (w - self.cols * self.field_size) // 2
        margin_y = (h - self.rows * self.field_size) // 2
        for r in range(self.rows):
            for c in range(self.cols):
                x = margin_x + c * self.field_size
                y = margin_y + r * self.field_size
                color = (0, 180, 0) if random.random() > 0.4 else (80, 80, 80)
                self.fields.append({"rect": pygame.Rect(x, y, self.field_size-10, self.field_size-10), "active": color[1] > 100, "color": color})
    
    def update(self, positions):
        self.just_scored = False
        # Map camera positions to screen (simplified - assumes rough alignment; add homography later)
        for pos in positions:
            # Rough scale mapping (tune these)
            sx = int(pos[0] * 1280 / 640)
            sy = int(pos[1] * 720 / 480)
            for field in self.fields:
                if field["active"] and field["rect"].collidepoint(sx, sy):
                    field["active"] = False
                    field["color"] = (50, 50, 50)
                    self.score += 10
                    self.just_scored = True
                    break
    
    def draw(self, screen):
        for field in self.fields:
            pygame.draw.rect(screen, field["color"], field["rect"])
            pygame.draw.rect(screen, (255, 255, 255), field["rect"], 2)
