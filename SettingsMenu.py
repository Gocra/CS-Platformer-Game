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
)
from util import draw_text
from copy import copy

class SettingsMenu(Menu):
    def __init__(self, game_obj, screen, clock):
        super().__init__(game_obj, screen, clock)

        # font
        self.font = pygame.font.Font("assets/fonts/pixel art.ttf", 28)

        self.background = pygame.image.load("assets/backgrounds/jungle.png")
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))

        back_button_asset = pygame.image.load("assets/back_button.png")
        back_button_asset = pygame.transform.scale(back_button_asset, (48, 48))

        # make the buttons
        self.back_button = Button(pygame.Vector2(14,14), 48, 48, font = self.font, texture = back_button_asset)

        ssb_h, ssb_w = 70, 220
        button_asset = pygame.image.load("assets/button_texture.png")
        button_asset = pygame.transform.scale(button_asset, (ssb_w, ssb_h))

        self.save_settings_button = Button(pygame.Vector2((WINDOW_WIDTH - ssb_w) / 2, WINDOW_HEIGHT-56-ssb_h), ssb_w, ssb_h, font = self.font, text="Save Settings", texture=button_asset)

        # sliders
        self.musicVolumeSlider = Slider(185, label = "Music")
        self.sfxVolumeSlider = Slider(315, label = "Sfx")

        # values
        self.musicVolume = copy(self.game_obj.settings.get("volume").get("music"))
        self.sfxVolume = copy(self.game_obj.settings.get("volume").get("sfx"))

        # add all the buttons
        self.add_button(
            self.back_button,
            self.save_settings_button
        )

        self.currentMusicVolume = copy(self.musicVolume)
        self.currentSfxVolume = copy(self.sfxVolume)
        self.musicVolumeSlider.setValue(self.musicVolume)
        self.sfxVolumeSlider.setValue(self.sfxVolume)
    
    def update(self, left_click, mouse_pos):

        # update sliders
        self.musicVolumeSlider.update(left_click, self.left_button_down, mouse_pos)
        self.sfxVolumeSlider.update(left_click, self.left_button_down, mouse_pos)

        # get values from sliders
        self.musicVolume = self.musicVolumeSlider.value
        self.sfxVolume = self.musicVolumeSlider.value

        pygame.mixer.music.set_volume(self.musicVolume) # change the music volume

        if self.back_button.is_clicked:
            pygame.mixer.music.set_volume(copy(self.currentMusicVolume))
            self.game_obj.current_state = self.game_obj.State.MAIN_MENU
            self.musicVolumeSlider.setValue(self.currentMusicVolume)
            self.sfxVolumeSlider.setValue(self.currentSfxVolume)
            self.running = False

        if self.save_settings_button.is_clicked:
            # change in game settings
            self.game_obj.settings["volume"]["music"] = copy(self.musicVolumeSlider.value)
            self.game_obj.settings["volume"]["sfx"] = copy(self.sfxVolumeSlider.value)

            # update settings file
            update_json_file("settings.json", self.game_obj.settings)

            # back to main menu
            self.game_obj.current_state = self.game_obj.State.MAIN_MENU
            self.running = False
        
    def render(self):
        self.musicVolumeSlider.render(self.screen)
        self.sfxVolumeSlider.render(self.screen)
        draw_text(self.screen, "SETTINGS MENU", self.font, (247, 28), (255,255,255))
