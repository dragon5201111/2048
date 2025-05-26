from game import Game
from grid import Grid
from line import LineAdapter
from tile import *

grid_height = grid_width = game_height = game_width = 801
game = Game(title="2048", width_height=(game_width, game_height))

grid_color = (0, 0, 0)
grid_line_width = 17
grid_rows = grid_columns = 4
grid_start_pos = ((game.width - grid_width) // 2, (game.height - grid_height) // 2)
grid = Grid(
    line_adapter=LineAdapter(line_width=grid_line_width, color=grid_color),
    tile_factory=DefaultTileFactory(),
    rows_columns=(grid_rows, grid_columns),
    start_pos=grid_start_pos,
    line_width=grid_line_width,
    width_height=(grid_width, grid_height),
    color=grid_color
)


game.add_observer(grid)
game.run()
