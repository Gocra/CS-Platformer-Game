import pygame
import sys
import Game
from config import FPS, WINDOW_WIDTH, WINDOW_HEIGHT

class Menu:
    def __init__(self, game_obj, screen, clock):
        self.screen = screen
        self.clock = clock
        self.game_obj = game_obj
        self.running = True

        self.background = None

        self.left_button_down = False

        self.buttons = []

    def run(self):

        while self.running:
            self.clock.tick(FPS) # makes loop run at same speed every time

            events = pygame.event.get()

            left_click = False
            mouse_pos = pygame.mouse.get_pos()

            # check for user input
            for event in events:
                if event.type == pygame.QUIT:   # user closed the window
                    pygame.quit() # close the window
                    sys.exit(0) # close the program
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    left_click = True
                    self.left_button_down = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.left_button_down = False
                if event.type == pygame.WINDOWFOCUSLOST:        # user has clicked off of application
                    pygame.mixer.music.pause()
                if event.type == pygame.WINDOWFOCUSGAINED:      # user has clicked on the application
                    pygame.mixer.music.unpause()

            for button in self.buttons:
                button.update(left_click, mouse_pos)
            
            if self.should_hover():
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # handle button events in the child class
            self.update(left_click, mouse_pos)
            
            # render
            # buffer - renders over previous frame to clear the screen
            self.screen.fill((0,0,0))

            if self.background != None:
                self.screen.blit(self.background, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

            for button in self.buttons:
                button.render(self.screen)
            
            self.render()
            
            pygame.display.update()

    def add_button(self, *buttons):
        for button in buttons:
            self.buttons.append(button)

    def should_hover(self):
        for button in self.buttons:
            if button.is_hovered:
                return True
        return False

    def update(self): pass
    def render(self): pass
