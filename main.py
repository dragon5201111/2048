from game import Game
from grid import Grid
from line import LineAdapter
from tile import *

grid_height = grid_width = game_height = game_width = 801
game_bg_color = (189, 173, 150)
game = Game(title="2048", bg_color=game_bg_color, width_height=(game_width, game_height))

grid_color = (154, 137, 120)
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

grid.add_tile(0, 0, 2)
grid.add_tile(0, 1, 2)
grid.add_tile(0, 2, 2)
grid.add_tile(0, 3, 2)





game.add_observer(grid)
game.run()
