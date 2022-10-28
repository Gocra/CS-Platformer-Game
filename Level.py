import pygame
import sys
from config import TILE_SIZE, WINDOW_WIDTH, WINDOW_HEIGHT, FPS, LEVEL_BG_COLOR
from Player import Player
from Camera import Camera
from Enemy import Enemy
from Button import Button
from util import get_json_from_file, draw_text
import ast
import json
from importLevel import importLevel, convertFromStringImportData, assignTileByIndex, convertTileMap2Tiles

count_down_timer_event = pygame.USEREVENT

class Level:
    def __init__(self, levelMap, playerArray, enemyArray, interactableTilesArray, screen, clock, filename):
        # restore defaults on reset
        self.filename = filename

        # get the screen
        self.screen = screen
        self.clock = clock

        # font
        self.font = pygame.font.Font("assets/fonts/pixel art.ttf", 18)
        self.pause_button_font = pygame.font.Font("assets/fonts/pixel art.ttf", 32)
        self.winFont = pygame.font.Font("assets/fonts/pixel art.ttf", 40)
        self.winESCFont = pygame.font.Font("assets/fonts/pixel art.ttf", 24)
        self.infoGraphFont = pygame.font.Font("assets/fonts/pixel art.ttf", 32)

        # load music
        pygame.mixer.music.load("assets/music/cave_theme_1.wav")

        self.map_height = levelMap[-1][0].get('rect').bottom
        self.map_length = levelMap[0][-1].get('rect').right

        self.entityData = get_json_from_file("entities.json")

        self.levelMap = levelMap
        self.playerArray = playerArray
        self.player = Player(self.playerArray[0], self.entityData.get('PLAYER'), self.map_length, self.map_height)
        self.paused = False
        
        # timer
        self.count_down_timer = self.count_down_timer_limit = 3 * 60 # seconds
        pygame.time.set_timer(count_down_timer_event, 1000) # triggers event every 1s (1000ms)

        self.setup_camera()
        self.setup_pause_menu()
        self.setup_enemy_array(enemyArray)
        self.setup_interactable_tiles(interactableTilesArray)

        pause_button_asset = pygame.image.load("assets/pause_button.png")
        pause_button_asset = pygame.transform.scale(pause_button_asset, (48, 48))

        self.pause_button = Button(pygame.math.Vector2(WINDOW_WIDTH - 60, 10), 48, 48, texture = pause_button_asset)

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(160)

    def setup_interactable_tiles(self, interactableTilesArray):
        self.interactableTilesArray = interactableTilesArray
        tilemap = pygame.image.load("assets/interactableTilemap.png")
        self.interactableTiles = convertTileMap2Tiles(tilemap)

    def render_interactable_tiles(self):
        for tile in self.interactableTilesArray:
            rect = tile.get('rect')
            self.screen.blit(self.interactableTiles[tile.get('type')],
                (rect.x - self.camera.offset.x, rect.y - self.camera.offset.y, rect.w, rect.h))

    def setup_enemy_array(self, enemyArray):
        self.enemyArray = []
        for enemy in enemyArray:
            self.enemyArray.append(Enemy(enemy, self.entityData.get("ENEMY"), self.map_length, self.map_height))

    def run(self):

        pygame.mixer.music.play(-1)

        running = True
        while running:
            self.clock.tick(FPS) # makes loop run at same speed every time

            events = pygame.event.get()

            left_click = False
            mouse_pos = pygame.mouse.get_pos()

            # check for user input
            for event in events:
                if event.type == pygame.QUIT:   # user closed the window
                    pygame.quit() # close the window
                    sys.exit(0) # close the program
                if event.type == count_down_timer_event and not self.paused and not self.player.hasWon:
                    self.count_down_timer -= 1 # decrease timer by 1 second
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    left_click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.player.hasWon:
                        running = False
                    else:
                        self.paused = not self.paused
                        self.resume_button.is_hovered = False
                        self.quit_button.is_hovered = False
                if event.type == pygame.WINDOWFOCUSLOST:        # user has clicked off of application
                    self.paused = True
                    pygame.mixer.music.pause()
                if event.type == pygame.WINDOWFOCUSGAINED:      # user has clicked on the application
                    pygame.mixer.music.play()

            
            if not self.player.hasWon:

                # update
                self.pause_button.update(left_click, mouse_pos)

                if self.pause_button.is_clicked:
                    self.paused = not self.paused

                if not self.paused:
                    # update
                    self.player.update(self.levelMap, self.enemyArray, self.interactableTilesArray)

                    for enemy in self.enemyArray:
                        enemy.update(self.levelMap)

                    # handle player
                    if self.count_down_timer <= 0:
                        self.player.instant_death()

                    if self.player.is_out_of_bounds():
                        self.player.instant_death()

                    if self.player.is_dead():
                        self.restart()

                    # handle enemies
                    for enemy in self.enemyArray:
                        if enemy.is_out_of_bounds():
                            enemy.instant_death()

                    for i, enemy in enumerate(self.enemyArray):
                        if enemy.is_dead():
                            self.enemyArray.pop(i)

                    self.camera.scroll()
                else:
                    # update pause buttons
                    for button in self.pause_menu_buttons:
                        button.update(left_click, mouse_pos)
                
                if self.should_hover():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # render
            self.screen.fill((0,0,0)) # buffer - renders over previous frame to clear the screen
            self.screen.fill(LEVEL_BG_COLOR)  # background

            if self.filename == "levels/level1.json":
                self.render_tutorial_infographics()

            self.render_map(self.camera.offset)

            self.player.render(self.screen, self.camera.offset)
            self.player.render_healthbar(self.screen)
            self.player.render_coin_count(self.screen)
            
            for enemy in self.enemyArray:
                enemy.render(self.screen, self.camera.offset)

            self.render_interactable_tiles()
            
            self.render_timer()
            
            if self.paused and not self.player.hasWon:
                # render overlay
                self.screen.blit(self.overlay, (0, 0))

                # render pause menu and buttons
                self.render_pause_menu()

                # handle button events
                if self.resume_button.is_clicked:
                    self.paused = False
                    self.resume_button.is_hovered = False

                if self.quit_button.is_clicked:
                    running = False

            self.pause_button.render(self.screen)

            if self.player.hasWon:
                # dark background
                self.screen.blit(self.overlay, (0, 0))

                # win text
                draw_text(self.screen, "YOU WIN", self.winFont,
                    ((WINDOW_WIDTH - self.winFont.size("YOU WIN")[0]) / 2,
                    (WINDOW_HEIGHT - self.winFont.size("YOU WIN")[1]) / 2 - 100))

                # leave text
                draw_text(self.screen, "Press ESC to exit", self.winESCFont,
                    ((WINDOW_WIDTH - self.winESCFont.size("Press ESC to exit")[0]) / 2,
                    (WINDOW_HEIGHT - self.winESCFont.size("Press ESC to exit")[1]) / 2 + 100))


            # update the window (render everything)
            pygame.display.update()

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

    def render_tutorial_infographics(self):
        draw_text(self.screen, "A - Left", self.infoGraphFont, ((WINDOW_WIDTH -self.infoGraphFont.size("A - Left")[0]) / 2, 100))
        draw_text(self.screen, "D - Right", self.infoGraphFont, ((WINDOW_WIDTH -self.infoGraphFont.size("D - Right")[0]) / 2, 150))
        draw_text(self.screen, "Space - Jump", self.infoGraphFont, ((WINDOW_WIDTH -self.infoGraphFont.size("Space - Jump")[0]) / 2, 200))
        draw_text(self.screen, "ESC - Pause",self.infoGraphFont, ((WINDOW_WIDTH -self.infoGraphFont.size("ESC - Pause")[0]) / 2, 250))

    def restart(self):
        # load level data
        lm, pa, ea, ita = importLevel(self.filename)
        lm, pa, ea, ita = convertFromStringImportData(lm, pa, ea, ita)
        lm = assignTileByIndex(lm)

        """
        lm levelmap
        pa pa
        ea ea
        ita ita
        """

        self.levelMap = lm
        self.playerArray = pa
        self.enemyArray = ea
        self.interactableTilesArray = ita

        self.player = Player(self.playerArray[0], self.entityData.get('PLAYER'), self.map_length, self.map_height)
        self.count_down_timer = self.count_down_timer_limit = 3 * 60 # seconds
        self.setup_camera()
        self.setup_enemy_array(self.enemyArray)
        self.setup_interactable_tiles(self.interactableTilesArray)
        
        self.run()
    
    def render_timer(self):
        draw_text(self.screen, "{:03d}".format(self.count_down_timer), self.font,
        (self.pause_button.rect.x - (3 * 14), 14), (255,255,255))

    def render_map(self, camera_offset):
        for row in self.levelMap:
            for tile in row:

                rect = tile.get("rect")
                tile = tile.get("tile")

                # render tile
                if tile != None:
                    self.screen.blit(tile, (rect.x - camera_offset.x, rect.y - camera_offset.y, rect.w, rect.h))

    def setup_pause_menu(self):
        # button positioning and size attributes
        pause_menu_w = 300
        pause_menu_button_w = 250
        pause_menu_button_h = int(pause_menu_button_w / 3.4)
        button_margin = 20
        pause_menu_vertical_padding = 30

        number_of_buttons = 2
        pause_menu_h = (2 * pause_menu_vertical_padding) + (number_of_buttons * pause_menu_button_h) + (max(0, number_of_buttons - 1) * button_margin)

        # assets
        button_asset = pygame.image.load("assets/button_texture.png")
        button_asset = pygame.transform.scale(button_asset, (pause_menu_button_w, pause_menu_button_h))

        # calculate buttons positioning
        pause_menu_x = (WINDOW_WIDTH - pause_menu_w) / 2
        pause_menu_y = (WINDOW_HEIGHT - pause_menu_h) / 2
        button_x = pause_menu_x + (pause_menu_w - pause_menu_button_w) / 2
        button_start_y = pause_menu_y + pause_menu_vertical_padding

        # create buttons
        self.resume_button = Button(pygame.Vector2(
            button_x, button_start_y),
            pause_menu_button_w,
            pause_menu_button_h,
            text = "Resume",
            font = self.pause_button_font,
            texture = button_asset)

        self.quit_button = Button(pygame.Vector2(
            button_x, button_start_y + pause_menu_button_h + button_margin),
            pause_menu_button_w, pause_menu_button_h,
            text = "Quit",
            font = self.pause_button_font,
            texture = button_asset)

        # append buttons to array
        self.pause_menu_buttons = []
        self.pause_menu_buttons.append(self.resume_button)
        self.pause_menu_buttons.append(self.quit_button)

        # create the rect for the pause menu
        self.pause_menu = pygame.Rect((pause_menu_x, pause_menu_y), (pause_menu_w, pause_menu_h))
    
    def render_pause_menu(self):
        # draw background
        pygame.draw.rect(self.screen, (100,100,100), self.pause_menu)

        # draw buttons
        for button in self.pause_menu_buttons:
            button.render(self.screen)

    def should_hover(self):
        buttons = self.pause_menu_buttons
        buttons.append(self.pause_button)

        for button in buttons:
            if button.is_hovered:
                return True
        return False

    def setup_camera(self):
        self.camera = Camera(self.player, self.map_height, self.map_length)