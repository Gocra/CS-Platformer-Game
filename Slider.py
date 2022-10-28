import pygame
from util import clamp, draw_text

class Slider:
    def __init__(self, yPos, *, label = None):
        self.x = 200
        self.y = yPos      
        self.width = 350
        self.height = 60
        self.label = label
        self.font = pygame.font.Font("assets/fonts/pixel art.ttf", 32)

        #slider handle
        self.handleWidth = 40
        self.handle = pygame.Rect(self.x, self.y, 20, self.handleWidth)
       
        # slider guide
        self.guide = pygame.Rect(self.x, self.y + 15, 350, 10)

        # value
        self.lowerLimit = self.x + (self.handleWidth / 2)
        self.upperLimit = self.x + self.width - (self.handleWidth / 2)
        self.sliderLength = self.upperLimit - self.lowerLimit + self.handle.w
        self.value = 0

        # slider handle min max x coordinates
        self.min_x = self.x
        self.max_x = self.x + self.width
        
        self.isHeld = False

    def render(self, screen):
        if self.label != None:
            draw_text(screen, self.label, self.font,  (self.x, self.y - 30), (255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 255), self.guide)
        pygame.draw.rect(screen, (0, 0, 0), self.handle)

    def updateValue(self):
        position = self.handle.center[0] - self.x - (self.handle.w / 2)
        value = position / self.sliderLength
        value = round(value, 2)
        self.value = value

    def update(self, left_click, mouse_down, mouse_pos):
        if left_click and self.handle.collidepoint(mouse_pos):
            self.isHeld = True

        if not mouse_down:
            self.isHeld = False

        if self.isHeld:
            self.handle.x = clamp(self.min_x, mouse_pos[0] - (self.handleWidth / 4), self.max_x - (self.handleWidth / 2))
            self.updateValue()
            
    def setValue(self, value):
        # set value
        self.value = clamp(0, round(value, 2), 1)

        #get new position
        postition = value * self.sliderLength

        # move handle to new position by offset
        self.handle.x = postition + self.x
