import pygame
from util import draw_text

class Button:
    def __init__(self, pos, width, height, *, font = None, text = None, texture = None, hover_texture = None):
        self.rect = pygame.Rect(pos, (width, height))
        self.text = text
        self.font = font
        self.texture = texture
        self.hover_texture = hover_texture

        self.o_y = pos.y
        self.o_x = pos.y

        # if self.texture:
        #     self.rect = self.texture.get_rect()
        #     self.rect.x, self.rect.y = pos.x, pos.y

        self.is_hovered = False
        self.is_clicked = False

    def render(self, screen):
        # render button
        if self.is_hovered and self.hover_texture:
            screen.blit(self.hover_texture, self.rect)
        elif self.texture:
            screen.blit(self.texture, self.rect)
        else:
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.text:

            # get text size
            text_w, text_h = self.font.size(self.text)

            # get text position
            pos = pygame.Vector2(
                self.rect.x + ((self.rect.w - text_w) / 2),
                self.rect.y + ((self.rect.h - text_h) / 2)
            )
            
            # draw text
            draw_text(screen, self.text, self.font, pos, (255,255,255))
    
    def update(self, left_click, mouse_pos):
        self.is_hovered = False
        self.is_clicked = False

        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
            if left_click:
                self.is_clicked = True