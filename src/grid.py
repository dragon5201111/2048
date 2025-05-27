import random
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
                 color=(0, 0, 0),
                 tile_starter_number=2):

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
        self.tile_starter_number = tile_starter_number

    def get_cell_position(self, row, column):
        x = self.x + self.line_width + (column * (self.line_width + self.get_cell_width()))
        y = self.y + self.line_width + (row * (self.line_width + self.get_cell_height()))
        return x, y

    def get_cell_width(self):
        return (self.width - (self.line_width * (self.columns + 1))) // self.columns

    def get_cell_height(self):
        return (self.height - (self.line_width * (self.rows + 1))) // self.rows

    def add_tile(self, row, column, number):
        new_tile = self.tile_factory.create_tile(number=number,
                                                 width_height=(self.get_cell_width(), self.get_cell_height()))
        self.tiles[row][column] = new_tile

    def move_tile(self, old_row, old_column, new_row, new_column):
        tile = self.tiles[old_row][old_column]
        self.tiles[old_row][old_column] = None
        self.tiles[new_row][new_column] = tile

    def get_tile(self, row, column):
        return self.tiles[row][column]

    def remove_tile(self, row, column):
        self.tiles[row][column] = None

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, width=self.line_width)
        self.draw_lines(surface)
        self.draw_tiles(surface)

    def draw_lines(self, surface):
        for i in range(1, self.columns):
            column_x = self.x + i * (self.line_width + self.get_cell_width())
            self.line_adapter.draw_vertical(surface=surface, start_pos=(column_x, self.y), length=self.height)

        for i in range(1, self.rows):
            row_y = self.y + i * (self.line_width + self.get_cell_height())
            self.line_adapter.draw_horizontal(surface=surface, start_pos=(self.x, row_y), length=self.width)

    def draw_tiles(self, surface):
        for row in range(self.rows):
            for column in range(self.columns):
                tile = self.tiles[row][column]

                if tile:
                    self.draw_tile(row, column, surface)

    def draw_tile(self, row, column, surface):
        tile = self.tiles[row][column]

        if tile:
            tile.draw(surface, self.get_cell_position(row, column))

    def handle_event(self, surface, event):
        if event.type != pygame.KEYDOWN:
            return

        self.reset_has_merged()
        grid_changed = self.shift_tiles(event.key)

        if grid_changed:
            self.place_random_tile()

        if self.is_grid_full() and not grid_changed:
            self.reset_grid()

    def reset_has_merged(self):
        for row in range(self.rows):
            for column in range(self.columns):

                tile = self.tiles[row][column]
                if tile:
                    tile.set_has_merged(False)

    def shift_tiles(self, event_key):
        direction_data = self.get_direction_data(event_key)
        if direction_data is None:
            return False

        d_row, d_column, row_range, column_range = direction_data

        grid_changed = False

        for row in row_range:
            for column in column_range:
                if self.is_valid_tile(row, column):
                    if self.process_tile_shift(row, column, d_row, d_column):
                        grid_changed = True

        return grid_changed

    def get_direction_data(self, event_key):
        if event_key == pygame.K_LEFT:
            return 0, -1, range(self.rows), range(1, self.columns)

        elif event_key == pygame.K_RIGHT:
            return 0, 1, range(self.rows), range(self.columns - 2, -1, -1)

        elif event_key == pygame.K_UP:
            return -1, 0, range(1, self.rows), range(self.columns)

        elif event_key == pygame.K_DOWN:
            return 1, 0, range(self.rows - 2, -1, -1), range(self.columns)

        else:
            return None

    def process_tile_shift(self, start_row, start_column, d_row, d_column):
        current_tile = self.tiles[start_row][start_column]
        current_row, current_column = start_row, start_column
        tile_changed = False

        while True:
            next_row = current_row + d_row
            next_column = current_column + d_column

            if not self.is_valid_tile_position(next_row, next_column):
                break

            next_tile = self.tiles[next_row][next_column]
            if next_tile is None:
                # Moving
                self.move_tile(current_row, current_column, next_row, next_column)
                current_row, current_column = next_row, next_column
                tile_changed = True
            else:
                # Merging
                if self.can_merge_tiles(current_tile, next_tile):
                    self.merge_tiles(current_row, current_column, next_tile)
                    tile_changed = True
                break
        return tile_changed

    def merge_tiles(self, current_row, current_column, next_tile):
        next_tile.set_number(next_tile.get_number() * 2)
        next_tile.set_has_merged(True)
        self.remove_tile(current_row, current_column)

    def can_merge_tiles(self, tile_one, tile_two):
        return (tile_one.get_number() == tile_two.get_number() and
                not tile_one.has_merged and not tile_two.has_merged)

    def is_valid_tile(self, row, column):
        return self.is_valid_tile_position(row, column) and self.tiles[row][column] is not None

    def is_valid_tile_position(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.columns

    def reset_grid(self):
        self.tiles = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        self.place_random_tile()
        self.place_random_tile()

    def place_random_tile(self):
        if self.is_grid_full():
            return

        empty_cells = self.get_empty_cells()
        row, col = random.choice(empty_cells)

        self.add_tile(row, col, self.tile_starter_number)

    def get_empty_cells(self):
        return [(row, col) for row in range(self.rows)
                for col in range(self.columns)
                if self.tiles[row][col] is None]

    def is_grid_full(self):
        return all(self.tiles[row][col] is not None
                   for row in range(self.rows)
                   for col in range(self.columns))
