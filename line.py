import pygame


class LineAdapter:
    def __init__(self, color=(0, 0, 0), line_width=5):
        if line_width % 2 == 0:
            raise ValueError("Width must be odd.")
        self.width = line_width
        self.color = color

    def draw_vertical(self, surface, start_pos, length):
        offset = self.width // 2
        x, y = start_pos
        pygame.draw.line(
            surface=surface,
            start_pos=(x + offset, y),
            end_pos=(x + offset, y + length),
            width=self.width,
            color=self.color
        )

    def draw_horizontal(self, surface, start_pos, length):
        offset = self.width // 2
        x, y = start_pos
        pygame.draw.line(
            surface=surface,
            start_pos=(x, y + offset),
            end_pos=(x + length, y + offset),
            width=self.width,
            color=self.color
        )
