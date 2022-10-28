import pygame
from config import *
from util import get_json_from_file
from Game import Game
from MainMenu import MainMenu
from SettingsMenu import SettingsMenu
from SelectLevelMenu import SelectLevelMenu
from CreditsMenu import CreditsMenu

def main():
    game_obj = Game()
    settingsData = get_json_from_file("settings.json")
    game_obj.settings = settingsData.get("settings")
    
    pygame.init()           # setup pygame
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()     # setup sound for pygame
    pygame.mixer.music.set_volume(game_obj.settings.get("volume").get("music"))

    # loading the window icon
    PROGRAM_ICON = pygame.image.load("assets/icon.png")

    # settings the icon and title for the window
    pygame.display.set_icon(PROGRAM_ICON)
    pygame.display.set_caption(WINDOW_TITLE)

    # creating the window and clock
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # create the window
    clock = pygame.time.Clock()     # create clock for syncing FPS

    main_menu = MainMenu(game_obj, screen, clock)
    settings_menu = SettingsMenu(game_obj, screen, clock)
    select_level_menu = SelectLevelMenu(game_obj, screen, clock)
    credits_menu = CreditsMenu(game_obj, screen, clock)

    # load music
    pygame.mixer.music.load("assets/music/menu_soundtrack_by_cactusdude.mp3")
    pygame.mixer.music.play(-1)

    while True:
        if game_obj.current_state == game_obj.State.MAIN_MENU:
            main_menu.running = True
            main_menu.run()

        elif game_obj.current_state == game_obj.State.SETTINGS_MENU:
            settings_menu.running = True
            settings_menu.run()
            
        elif game_obj.current_state == game_obj.State.SELECT_LEVEL_MENU:
            select_level_menu.running = True
            select_level_menu.run()
        
        elif game_obj.current_state == game_obj.State.CREDITS_MENU:
            credits_menu.running = True
            credits_menu.run()

if __name__ == "__main__":
    main()
