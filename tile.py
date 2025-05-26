from abc import ABC, abstractmethod
import pygame


class Tile:
    def __init__(self, number, font, width_height, bg_color, text_color, start_pos=(0, 0)):
        self.number = number
        self.font = font
        self.width, self.height = width_height
        self.bg_color = bg_color
        self.text_color = text_color

        self.rect = pygame.Rect(start_pos, width_height)
        self.text_surface = self.font.render(str(self.number), True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def set_position(self, position):
        self.rect.topleft = position
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface, position):
        self.set_position(position)
        pygame.draw.rect(surface, self.bg_color, self.rect)
        surface.blit(self.text_surface, self.text_rect)


class TileFactory(ABC):
    @abstractmethod
    def create_tile(self, number, width_height):
        pass


class DefaultTileFactory(TileFactory):
    def create_tile(self, number, width_height):
        return Tile(
            number=number,
            font=pygame.font.SysFont(None, 48),
            width_height=width_height, bg_color=(25, 25, 25),
            text_color=(0, 0, 0)
        )
