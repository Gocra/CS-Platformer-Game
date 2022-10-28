import pygame
from Entity import Entity
from config import *

class Enemy(Entity):
    def __init__(self, enemy, spriteData, map_length, map_height):
        spritesheet = pygame.image.load(f"assets/Enemy/{enemy.get('type') + 1}.png")
        super().__init__(spritesheet, enemy.get('rect'), spriteData, map_length, map_height)
        self.direction.x = -1
    
    def update(self, levelMap):
        self.animate()
        
        # vertical
        self.handle_vertical_movement()
        self.handle_vertical_collisions(levelMap)

        # horizontal
        self.handle_horizontal_movement()
        self.handle_horizontal_collisions(levelMap)
        self.constrain_to_map()
    
    def render(self, screen, camera_offset):
        # draw the enemy on the screen
        screen.blit(self.sprite, (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y, self.sprite.get_rect().w, self.sprite.get_rect().h))
    
    def handle_horizontal_collisions(self, levelMap):
        # obstacles is an array of rects
        # loop through all obstacles
        for y, row in enumerate(levelMap):
            for x, tile in enumerate(row):
                if tile.get('tile') != None:
                    rect = tile.get('rect')
                    # check if colliding
                    if self.rect.colliderect(tile.get('rect')):
                        # find if colliding on left or right or player
                        if self.direction.x < 0: # player moving left
                            self.rect.left = rect.right
                        elif self.direction.x > 0: # player moving right
                            self.rect.right = rect.left
                        
                        self.direction.x *= -1
            
        if self.rect.left <= self.MAP_START or self.rect.left >= self.MAP_END:
            self.direction.x *= -1