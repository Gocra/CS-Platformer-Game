import pygame
import sys
import Game
from Menu import Menu
from Button import Button
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    LEVEL_BG_COLOR
)
from Level import Level
from util import draw_text, getFilenamesInFolder
from importLevel import importLevel, convertFromStringImportData, assignTileByIndex

class SelectLevelMenu(Menu):

    def __init__(self, game_obj, screen, clock):
        super().__init__(game_obj, screen, clock)

        #background
        self.background = pygame.image.load("assets/backgrounds/jungle.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # font
        self.font = pygame.font.Font("assets/fonts/pixel art.ttf", 28)

        back_button_asset = pygame.image.load("assets/back_button.png")
        back_button_asset = pygame.transform.scale(back_button_asset, (48, 48))

        # make the buttons
        self.back_button = Button(pygame.Vector2(14,14), 48, 48, font = self.font, texture = back_button_asset)

        # add all the buttons
        self.add_button(
            self.back_button
        )

        # level attributes
        self.setup_level_grid()
        self.levels = []
        self.setup_levels()

    def setup_levels(self):
        levelFilenames = getFilenamesInFolder("levels")

        for i, filename in enumerate(levelFilenames):
            levelFilename = f"levels/{filename}"

            # get which row the level should be on
            row = 0
            j = i
            while j >= self.no_of_cols:
                row+=1
                j -= self.no_of_cols

            xPos = self.grid_start_x + (j * self.level_button_w) + (j * self.dx)
            yPos = self.grid_start_y + (row * self.level_button_h) + (row * self.dy)

            # load level data to get the image
            lm, pa, ea, ita = importLevel(levelFilename)
            lm, pa, ea, ita = convertFromStringImportData(lm, pa, ea, ita)
            levelMap = assignTileByIndex(lm)
            playerArray = pa
            enemyArray = ea
            interactableTilesArray = ita

            # get image of level
            tileSizeOnLevelButton = 6
            levelButtonImage = pygame.Surface([self.level_button_w, self.level_button_h], pygame.SRCALPHA).convert_alpha()

            # background color
            levelButtonImage.fill(LEVEL_BG_COLOR)

            # render level map
            for y, row in enumerate(levelMap):
                for x, tile in enumerate(row):
                    tile = tile.get('tile')
                    if tile != None:
                        currentTile = pygame.transform.scale(tile, (tileSizeOnLevelButton, tileSizeOnLevelButton))
                        levelButtonImage.blit(currentTile, (x * tileSizeOnLevelButton, y * tileSizeOnLevelButton),
                        (0, 0, tileSizeOnLevelButton, tileSizeOnLevelButton))

            selectLevelButton = Button(pygame.Vector2(xPos, yPos), int(self.level_button_w), int(self.level_button_h), texture=levelButtonImage)
            
            self.add_button(selectLevelButton)
            self.levels.append({
                "id":i,
                "file":levelFilename,
                "button": selectLevelButton
            })
        
    def setup_level_grid(self):
        self.no_of_cols = 4     # amount of levels shown per row
        padding = 40            # distance from window edge and grid
        self.dx, self.dy = 20, 20    # difference between level buttons x and y
        lbw, lbh = 4, 3              # aspect ratio of level button width to level button height

        self.grid_start_x, self.grid_end_x = padding, WINDOW_WIDTH - padding
        self.grid_start_y = 2.5 * padding
        grid_w = self.grid_end_x - self.grid_start_x

        self.level_button_w = (grid_w - (self.dx * (self.no_of_cols - 1))) / self.no_of_cols
        self.level_button_h = (self.level_button_w / lbw) * lbh
    
    def render_levels(self):
        for level in self.levels:
            level.get('button').render(self.screen)
    
    #*args prevents error, settings menu needs args, other menus dont but crash if not because superclass
    def update(self, *args):
        if self.back_button.is_clicked:
            self.game_obj.current_state = self.game_obj.State.MAIN_MENU
            self.running = False
        
        for level in self.levels:
            if level.get('button').is_clicked:

                """
                lm levelmap
                pa pa
                ea ea
                ita ita
                """

                # load level data
                lm, pa, ea, ita = importLevel(level.get('file'))
                lm, pa, ea, ita = convertFromStringImportData(lm, pa, ea, ita)
                lm = assignTileByIndex(lm)

                # run level
                level = Level(lm, pa, ea, ita, self.screen, self.clock, level.get('file'))
                level.run()

                # reload music
                pygame.mixer.music.load("assets/music/menu_soundtrack_by_cactusdude.mp3")
                pygame.mixer.music.play(-1)
        
    def render(self):
        # title text
        draw_text(self.screen, "SELECT LEVEL", self.font, (250, 28), (255,255,255))

        # levels
        if len(self.levels) == 0:
            draw_text(self.screen, "No levels found in levels folder".upper(), self.font, (100, 160), (255,0,0))
        else:
            self.render_levels()
