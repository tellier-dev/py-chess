import pygame
from pygame import Color


class Overlay:
    def __init__(self, width, height, rgba):
        self.width = width
        self.height = height
        self.__rgba = rgba
        self.__screen = pygame.Surface((width, height), pygame.SRCALPHA)
        self.__screen.fill(self.__rgba)

    @classmethod
    def frompreset(cls, width, height):
        return cls(width, height, Color(18, 18, 18, 216))

    def set_color(self, rgba):
        self.__rgba = rgba

    def add_text(self, text, y, color=Color(255, 255, 255), font_size=32, align_left=False, align_center=False, align_right=False):
        font = pygame.font.SysFont(None, font_size)
        text = font.render(text, True, color)

        if text.get_width() + 10 > self.width:
            return False

        # center as default if no alignment is provided
        align_center = True if (not align_left and not align_center and not align_right) else False

        x = 0
        if align_left:
            x = 5
        elif align_right:
            x = self.width - text.get_width() - 5
        else:
            x = (self.width - text.get_width) / 2

        self.__screen.blit(text, (x, y))

    def screen(self):
        return self.__screen
