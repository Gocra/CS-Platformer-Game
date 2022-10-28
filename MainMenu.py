import pygame
import sys
import Game
from Menu import Menu
from Button import Button
from Level import Level
from config import (
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    __MENU_MESSAGE__,
    __GITHUB_CODE_URL__,
    __GITHUB_URL__
)
from util import draw_text
import webbrowser

class MainMenu(Menu):
    def __init__(self, game_obj, screen, clock):
        super().__init__(game_obj, screen, clock)

        # font
        self.menu_message_font = pygame.font.Font("assets/fonts/pixel art.ttf", 14)
        self.button_font = pygame.font.Font("assets/fonts/pixel art.ttf", 28)

        # background
        self.background = pygame.image.load("assets/main_menu_bg.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # assets
        quit_button_asset = pygame.image.load("assets/main_menu_quit_button.png")
        quit_button_asset = pygame.transform.scale(quit_button_asset, (48, 48))

        # github logo
        github_logo = pygame.image.load("assets/github_button.png")
        github_logo_w, github_logo_h = github_logo.get_rect().w, github_logo.get_rect().h
        scale = 2
        github_logo = pygame.transform.scale(github_logo, (github_logo_w * scale, github_logo_h * scale))

        # github logo green (hover)
        github_logo_hover = pygame.image.load("assets/github_button_green.png")
        github_logo_hover = pygame.transform.scale(github_logo_hover, (github_logo_w * scale, github_logo_h * scale))

        # code logo
        code_logo = pygame.image.load("assets/code_button.png")
        code_logo_w, code_logo_h = code_logo.get_rect().w, code_logo.get_rect().h
        scale = 2
        code_logo = pygame.transform.scale(code_logo, (code_logo_w * scale, code_logo_h * scale))

        # code logo green (hover)
        code_logo_hover = pygame.image.load("assets/code_button_green.png")
        code_logo_hover = pygame.transform.scale(code_logo_hover, (code_logo_w * scale, code_logo_h * scale))

        # get new github logo dimensions
        github_logo_w, github_logo_h = github_logo.get_rect().w, github_logo.get_rect().h

        # button positioning variables and calcualtions
        btn_w = 250
        btn_h = int(btn_w / 3.4)
        btn_x = (WINDOW_WIDTH - btn_w) / 2
        btn_padding = 12
        start_y = 260

        # assets
        button_asset = pygame.image.load("assets/button_texture.png")
        button_asset = pygame.transform.scale(button_asset, (btn_w, btn_h))

        # make the buttons
        self.play_button = Button(pygame.Vector2(btn_x,start_y), btn_w, btn_h, font = self.button_font, text = "Play", texture = button_asset)
        self.settings_button = Button(pygame.Vector2(btn_x, start_y + btn_h + btn_padding), btn_w, btn_h, font = self.button_font, text = "Settings", texture = button_asset)
        self.credits_button = Button(pygame.Vector2(btn_x, start_y + 2 * (btn_h + btn_padding)), btn_w, btn_h, font = self.button_font, text = "Credits", texture = button_asset)
        
        self.quit_button = Button(pygame.math.Vector2(WINDOW_WIDTH - 62, 14), 48, 48, texture = quit_button_asset)

        self.github_button = Button(
            pygame.Vector2(WINDOW_WIDTH - github_logo_w - 14, WINDOW_HEIGHT - github_logo_h - 14),
            github_logo_w, github_logo_h,
            texture = github_logo,
            hover_texture = github_logo_hover
        )

        self.github_code_button = Button(
            pygame.Vector2(WINDOW_WIDTH - github_logo_w - 14, WINDOW_HEIGHT - 3 * (github_logo_h - 14) - 6 ),
            github_logo_w, github_logo_h,
            texture = code_logo,
            hover_texture = code_logo_hover
        )
        
        # add all the buttons
        self.add_button(
            self.play_button,
            self.github_button,
            self.settings_button,
            self.credits_button,
            self.github_code_button,
            self.quit_button
        )

    #*args prevents error, settings menu needs args, other menus dont but crash if not because superclass
    def update(self, *args):

        if self.credits_button.is_clicked:
            self.game_obj.current_state = self.game_obj.State.CREDITS_MENU
            self.running = False

        if self.play_button.is_clicked:
            # play level
            self.game_obj.current_state = self.game_obj.State.SELECT_LEVEL_MENU
            self.running = False

        if self.settings_button.is_clicked:
            self.game_obj.current_state = self.game_obj.State.SETTINGS_MENU
            self.running = False
        
        if self.github_button.is_clicked:
            # go to my github page
            webbrowser.open(__GITHUB_URL__, new=2)

        if self.github_code_button.is_clicked:
            # go to my github page
            webbrowser.open(__GITHUB_CODE_URL__, new=2)
        
        if self.quit_button.is_clicked:
            pygame.quit()
            sys.exit(0)
        
    def render(self):
        draw_text(self.screen, __MENU_MESSAGE__, self.menu_message_font, (14, WINDOW_HEIGHT - 28), (255,255,255))
