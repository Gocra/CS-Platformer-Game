import pygame
import webbrowser as wb
from config import LINK_COLOR
from util import draw_text

class Link():
    def __init__(self, pos, text, font, URL):
        self.rect = pygame.Rect(pos[0], pos[1], font.size(text)[0], font.size(text)[1])
        self.text = text
        self.font = font
        self.URL = URL
        self.is_hovered = False

    def update(self, left_click, mouse_pos):
        self.is_hovered = False
        if self.rect.collidepoint(mouse_pos):
            self.is_hovered = True
            if left_click:
                wb.open(self.URL)

    def render(self, screen):
        draw_text(screen, self.text, self.font, self.rect, LINK_COLOR)
