import pygame
import sys
import Game
from util import update_json_file
from Menu import Menu
from Button import Button
from Slider import Slider
from config import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    __MENU_MESSAGE__
)
from util import draw_text
from Link import Link

class CreditsMenu(Menu):
    def __init__(self, game_obj, screen, clock):
        super().__init__(game_obj, screen, clock)

        # font
        self.font = pygame.font.Font("assets/fonts/pixel art.ttf", 28)
        self.linkFont = pygame.font.Font("assets/fonts/pixel art.ttf", 26)
        self.smallFont = pygame.font.Font("assets/fonts/pixel art.ttf", 20)
        self.smallestFont = pygame.font.Font("assets/fonts/pixel art.ttf", 18)

        back_button_asset = pygame.image.load("assets/back_button.png")
        back_button_asset = pygame.transform.scale(back_button_asset, (48, 48))

        self.links = [
            Link((40, 120), "vectorpixelstar itch.io", self.linkFont, "https://vectorpixelstar.itch.io"),
            Link((420, 120), "Tilemap", self.linkFont, "https://vectorpixelstar.itch.io/textures"),

            Link((40, 160), "temok itch.io", self.linkFont, "https://temok.itch.io"),
            Link((420, 160), "Hearts", self.linkFont, "https://temok.itch.io/heart-container-animated-in-pixel-art"),

            Link((40, 200), "iopn itch.io", self.linkFont, "https://iopn.itch.io"),
            Link((420, 200), "UI Buttons", self.linkFont, "https://iopn.itch.io/ui-buttons-pixel-art"),

            Link((40, 240), "kayillustrations itch.io", self.linkFont, "https://kayillustrations.itch.io"),
            Link((420, 240), "Social Media buttons", self.linkFont, "https://kayillustrations.itch.io/social-media-buttons"),

            Link((40, 280), "totuslotus itch.io", self.linkFont, "https://totuslotus.itch.io"),
            Link((420, 280), "Pixel Coins", self.linkFont, "https://totuslotus.itch.io/pixel-coins"),

            Link((40, 320), "adwitr itch.io", self.linkFont, "https://adwitr.itch.io"),
            Link((420, 320), "Button Asset Pack", self.linkFont, "https://adwitr.itch.io/button-asset-pack"),

            Link((40, 360), "svl itch.io", self.linkFont, "https://svl.itch.io"),
            Link((420, 360), "RPG Music Pack", self.linkFont, "https://svl.itch.io/rpg-music-pack-svl"),

            Link((40, 400), "chiphead64 itch.io", self.linkFont, "https://chiphead64.itch.io"),
            Link((420, 400), "Menu Sound Track", self.linkFont, "https://chiphead64.itch.io/menu-soundtrack"),

            Link((40, 440), "Crafton Gaming dafont", self.linkFont, "https://www.dafont.com/craftron-gaming.d6128"),
            Link((420, 440), "Minecraft Font", self.linkFont, "https://www.dafont.com/minecraft.font"),
        ]
    
    def update(self, left_click, mouse_pos):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.game_obj.current_state = self.game_obj.State.MAIN_MENU
            self.running = False

        for link in self.links:
            link.update(left_click, mouse_pos)
        
    def should_hover(self):
        for link in self.links:
            if link.is_hovered:
                return True
        return False

    def render(self):
        # title
        draw_text(self.screen, "CREDITS", self.font, ((WINDOW_WIDTH - self.font.size("CREDITS")[0]) / 2, 28), (255,255,255))

        # me
        draw_text(self.screen, __MENU_MESSAGE__, self.font, ((WINDOW_WIDTH - self.font.size(__MENU_MESSAGE__)[0]) / 2, 70), (255,255,255))

        draw_text(self.screen, "These are clickable links", self.smallestFont, ((WINDOW_WIDTH - self.smallestFont.size("These are clickable links")[0]) / 2, WINDOW_HEIGHT - self.smallestFont.size("PRESS ESC TO EXIT")[1] - 64), (255,255,255))
        draw_text(self.screen, "PRESS ESC TO EXIT", self.smallFont, ((WINDOW_WIDTH - self.smallFont.size("PRESS ESC TO EXIT")[0]) / 2, WINDOW_HEIGHT - self.smallFont.size("PRESS ESC TO EXIT")[1] - 18), (255,255,255))

        for link in self.links:
            link.render(self.screen)
