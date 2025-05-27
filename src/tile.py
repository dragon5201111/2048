from abc import ABC, abstractmethod
from utility import Util
import pygame
import math


class Tile:
    def __init__(self, number, font, width_height, bg_color_start, bg_color_end,  text_color, start_pos=(0, 0)):
        self.number = number
        self.font = font
        self.width, self.height = width_height
        self.bg_color_start = bg_color_start
        self.bg_color_end = bg_color_end
        self.text_color = text_color

        self.rect = pygame.Rect(start_pos, width_height)
        self.has_merged = False



    def draw(self, surface, position):
        self.rect.topleft = position

        text_surface = self.font.render(str(self.number), True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)

        pygame.draw.rect(surface, self.get_color(), self.rect)
        surface.blit(text_surface, text_rect)


    def get_color(self):
        if self.number <= 2:
            return self.bg_color_start

        power = int(math.log2(self.number)) - 1

        max_power = 11
        t = min(power / max_power, 1.0)

        r, g, b, = Util.interpolate(t, self.bg_color_start, self.bg_color_end)
        return r, g, b

    def get_number(self):
        return self.number

    def set_number(self, number):
        self.number = number

    def set_has_merged(self, has_merged):
        self.has_merged = has_merged


class TileFactory(ABC):
    @abstractmethod
    def create_tile(self, number, width_height):
        pass


class DefaultTileFactory(TileFactory):
    def create_tile(self, number, width_height):
        return Tile(
            number=number,
            font=pygame.font.SysFont(None, 48),
            width_height=width_height,
            bg_color_start=(238, 229, 219),
            bg_color_end=(255, 69, 0),
            text_color=(116, 100, 83)
        )
