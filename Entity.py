import pygame
from config import TILE_SIZE

class Entity():
    def __init__(self, spritesheet, rect, spriteData, map_length, map_height):
        self.health = self.max_health = spriteData.get('health')
        self.rect = rect

        # constraints
        self.MAP_START = 0
        self.MAP_END = map_length
        self.map_height = map_height

        # movement variables
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.85
        self.speed = spriteData.get('speed')

        # animation variables
        self.facing_right = True
        self.on_ground = False

        # render sprite onto surface
        self.frame_index = 0
        self.animation_speed = 0.15

        # render sprite onto surface
        self.spritesheet = spritesheet
        self.sprite = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()
        self.sprite.blit(self.spritesheet, (0,0), (1 * TILE_SIZE, 1 * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def is_dead(self):
        return self.health <=0
    
    def take_dmg(self):
        self.health -= 1

    def is_out_of_bounds(self):
        if self.rect.y > self.map_height:
            self.instant_death()
    
    def instant_death(self):
        self.health = 0

    def animate(self):
        self.sprite.fill((0,0,0,0)) # remove old image from sprite

        row = 1
        if self.facing_right:
            row = 2

        if self.direction.x == 0:
            self.sprite.blit(self.spritesheet, (0,0), (1 * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        else:
            current_frame = int(self.frame_index)
            if self.frame_index >= 2: self.frame_index = 0
            self.sprite.blit(self.spritesheet, (0,0), (current_frame * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            self.frame_index += self.animation_speed
    
    def handle_vertical_collisions(self, levelMap):
        for y, row in enumerate(levelMap):
            for x, tile in enumerate(row):
                if tile.get('tile') != None:
                    rect = tile.get('rect')
                    if self.rect.colliderect(tile.get('rect')):
                        # find if colliding on top or bottom or player
                        if self.direction.y > 0:
                            # collision at top of player, move player down to the bottom of the obstacle
                            self.rect.bottom = rect.top
                            self.direction.y = 0 # reset gravity
                            self.on_ground = True
                        elif self.direction.y < 0:
                            # collision at bottom, move player up to stand on top of obstacle
                            self.rect.top = rect.bottom
                            self.direction.y = 0 # reset gravity 
                            self.on_ground = False

        if self.on_ground and (self.direction.y < 0 or self.direction.y > 1):
            self.on_ground = False
    
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
    
    # move the sprite vertically
    def handle_vertical_movement(self):
        # gravity
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    # move the sprite horizontally
    def handle_horizontal_movement(self):
        self.rect.x += self.direction.x * self.speed
        if self.direction.x == -1: self.facing_right = False
        elif self.direction.x == 1: self.facing_right = True

    # constrain entity to map
    def constrain_to_map(self):
        self.rect.left = max(self.rect.left, self.MAP_START)
        self.rect.right = min(self.rect.right, self.MAP_END)