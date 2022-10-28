import pygame
from Entity import Entity
from config import *
import math
from util import draw_text

class Player(Entity):
    def __init__(self, player, spriteData, map_length, map_height):
        
        spritesheet = pygame.image.load(f"assets/Player/{player.get('type') + 1}.png")
        
        super().__init__(spritesheet, player.get('rect'), spriteData, map_length, map_height)
        self.jump_height = spriteData.get('jump_height')
        self.inv_timer = self.inv_timer_limit = spriteData.get('inv_timer_limit')
        self.should_flash = False
        self.hasWon = False

        # healthbar HUD
        self.heart_sprites = {
            "EMPTY" : pygame.image.load("assets/heart_empty.png"),
            "HALF" : pygame.image.load("assets/heart_half.png"),
            "FULL" : pygame.image.load("assets/heart_full.png"),
            "GOLD_FULL" : pygame.image.load("assets/gold_full.png"),
            "GOLD_HALF" : pygame.image.load("assets/gold_half.png"),
        }
        self.healthbar_tl = pygame.Vector2(15,15)    # location of the health bar
        self.heart_sprite_width = self.heart_sprites.get("FULL").get_rect().w
        self.display_hearts = []

        # coins HUD
        self.coin_font = pygame.font.Font("assets/fonts/pixel art.ttf", 18)
        self.coins = 0
        self.coin_sprite = pygame.image.load("assets/coin.png")
        self.coin_sprite = pygame.transform.scale(self.coin_sprite, (TILE_SIZE, TILE_SIZE))

    def reset(self, originalRect):
        self.rect = originalRect
        self.health = self.max_health
        self.inv_timer = self.inv_timer_limit = 80
        self.should_flash = False
        self.facing_right = True
        self.on_ground = False
        self.frame_index = 0
        self.sprite.fill((0,0,0,0))
        self.sprite = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()
        self.sprite.blit(self.spritesheet, (0,0), (1 * TILE_SIZE, 1 * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def update(self, levelMap, enemyArray, interactableTilesArray):
        self.handle_input()  # handle input
        self.animate()
        
        # vertical
        self.handle_vertical_movement()
        self.handle_vertical_collisions(levelMap)

        # horizontal
        self.handle_horizontal_movement()
        self.handle_horizontal_collisions(levelMap)
        self.constrain_to_map()

        self.handle_enemy_collisions(enemyArray)
        self.handle_interactable_tile_collisions(interactableTilesArray)
        self.check_coin_count()
        self.update_heart_arr()

        self.inv_timer = max(0, self.inv_timer - 1)         # decrease timer
        if not self.inv_timer: self.should_flash = False    # timer is over, should not flash

    def render_healthbar(self, screen):
        # render the hearts
        for i in range(len(self.display_hearts)):
            xPos = self.healthbar_tl.x + ((self.heart_sprite_width) * i)
            screen.blit(self.heart_sprites.get(self.display_hearts[i]), (xPos, self.healthbar_tl.y))

    def update_heart_arr(self):
        half_hearts_count = self.health
        self.display_hearts = []

        # get correct heart types
        for _ in range(int(math.ceil(self.max_health / 2))):
            if half_hearts_count - 2 >= 0: half_hearts_count -= 2; self.display_hearts.append("FULL")
            elif half_hearts_count - 1 >= 0: half_hearts_count -= 1; self.display_hearts.append("HALF")
            else: self.display_hearts.append("EMPTY")
        
        # additional golden hearts
        if half_hearts_count > 0:
            for _ in range(int(math.ceil(half_hearts_count / 2))):
                if half_hearts_count - 2 >= 0: half_hearts_count -= 2; self.display_hearts.append("GOLD_FULL")
                elif half_hearts_count - 1 >= 0: half_hearts_count -= 1; self.display_hearts.append("GOLD_HALF")

    def render_coin_count(self, screen):
        screen.blit(self.coin_sprite, (15, 45, TILE_SIZE, TILE_SIZE))
        draw_text(screen, f"x{self.coins}", self.coin_font, (50, 45 + (self.coin_font.size(f"x{self.coins}")[1] / 2)))

    def handle_interactable_tile_collisions(self, interactableTilesArray):
        for i, tile in enumerate(interactableTilesArray):
            if tile.get('rect').colliderect(self.rect):
                tileType = tile.get('type')
                # coins
                if tileType == 3:
                    self.coins+=1
                    interactableTilesArray.pop(i)
                
                # flag - completed level
                if tileType == 0 or tileType == 1:
                    self.hasWon = True

    def check_coin_count(self):
        if self.coins >= 10:
            self.health += 1
            self.coins -= 10

    def handle_enemy_collisions(self, enemyArray):
        for i, enemy in enumerate(enemyArray):
            if enemy.rect.colliderect(self.rect):
                if self.direction.y > 1 and self.rect.bottom < enemy.rect.bottom:
                    enemy.take_dmg()
                    if enemy.is_dead():
                        enemyArray.pop(i)
                else:
                    if self.can_take_dmg():
                        self.take_dmg()

    def can_take_dmg(self):
        return not self.inv_timer > 0

    def take_dmg(self):
        self.health -= 1
        self.inv_timer = self.inv_timer_limit
        self.should_flash = True

    def render(self, screen, camera_offset):
        # draw the player on the screen
        if not self.should_flash or int(repr(self.inv_timer)[-1]) in [0,1,2,3,4,5]: # draw for time, don't draw for time, gives flashing effect
            screen.blit(self.sprite, (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y, self.sprite.get_rect().w, self.sprite.get_rect().h))
            # pygame.draw.rect(screen, (255, 0, 0), (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y, self.sprite.get_rect().w, self.sprite.get_rect().h), 3)

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # horizontal movement
        if keys[pygame.key.key_code("A")]:      # player is moving left
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.key.key_code("D")]:    # player is moving right
            self.direction.x = 1
            self.facing_right = True
        else:                                   # player is not moving
            self.direction.x = 0
        
        # jumping
        if keys[pygame.key.key_code("SPACE")] and self.on_ground:
            self.direction.y = self.jump_height