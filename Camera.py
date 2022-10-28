import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE
from util import clamp

class Camera:
    def __init__(self, player, map_height, map_length):
        self.player = player
        self.offset = pygame.math.Vector2(0,0)
        self.offset_f = pygame.math.Vector2(0,0)

        self.CONST = pygame.math.Vector2(
            - WINDOW_WIDTH / 2 + player.rect.w /2, # x axis
            - WINDOW_HEIGHT / 2 + player.rect.h /2 # y axis
        )

        # constraints
        self.MIN_X = 0
        self.MAX_X = map_length - WINDOW_WIDTH
        self.MIN_Y = 0
        self.MAX_Y = map_height - WINDOW_HEIGHT
    
    def scroll(self):
        # get camera offset from players position
        self.offset_f.x += (self.player.rect.x - self.offset_f.x + self.CONST.x) # x axis
        self.offset_f.y += (self.player.rect.y - self.offset_f.y + self.CONST.y) # y axis

        # clamp offset
        self.offset_f.x = clamp(self.MIN_X, self.offset_f.x, self.MAX_X)
        self.offset_f.y = clamp(self.MIN_Y, self.offset_f.y, self.MAX_Y)

        # set camera offset
        self.offset.x, self.offset.y = int(self.offset_f.x), int(self.offset_f.y)