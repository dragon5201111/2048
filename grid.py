import pygame

from drawableobserver import DrawableObserver


class Grid(DrawableObserver):

    def __init__(self,
                 line_adapter,
                 tile_factory,
                 start_pos=(0, 0),
                 width_height=(200, 300),
                 rows_columns=(3, 3),
                 line_width=5,
                 color=(0, 0, 0)):

        if width_height[0] % 2 == 0 or width_height[1] % 2 == 0:
            raise ValueError("Grid width and height must be odd.")

        if line_width % 2 == 0:
            raise ValueError("Line width must be odd.")

        self.line_adapter = line_adapter
        self.tile_factory = tile_factory
        self.x, self.y = start_pos
        self.width, self.height = width_height
        self.rows, self.columns = rows_columns
        self.line_width = line_width
        self.color = color

        self.rect = pygame.Rect(start_pos, width_height)
        self.tiles = [[None for _ in range(self.columns)] for _ in range(self.rows)]

    def get_cell_position(self, row, column):
        x = self.x + self.line_width + (column * (self.line_width + self.get_cell_width()))
        y = self.y + self.line_width + (row * (self.line_width + self.get_cell_height()))
        return x, y

    def get_cell_width(self):
        return (self.width - (self.line_width * (self.columns + 1))) // self.columns

    def get_cell_height(self):
        return (self.height - (self.line_width * (self.rows + 1))) // self.rows

    def add_tile(self, row, column, number):
        new_tile = self.tile_factory.create_tile(number=number, width_height=(self.get_cell_width(), self.get_cell_height()))
        self.tiles[row][column] = new_tile

    def draw_tile(self, row, column, surface):
        tile = self.tiles[row][column]

        if tile:
            tile.draw(surface, self.get_cell_position(row, column))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, width=self.line_width)
        self.draw_lines(surface)
        self.add_tile(0, 0, 2)
        self.draw_tile(0, 0, surface)

    def handle_event(self, surface, event):
        print(f"Grid responding to {event}")

    def draw_lines(self, surface):
        for i in range(1, self.columns):
            column_x = self.x + i * (self.line_width + self.get_cell_width())
            self.line_adapter.draw_vertical(surface=surface, start_pos=(column_x, self.y), length=self.height)

        for i in range(1, self.rows):
            row_y = self.y + i * (self.line_width + self.get_cell_height())
            self.line_adapter.draw_horizontal(surface=surface, start_pos=(self.x, row_y), length=self.width)
