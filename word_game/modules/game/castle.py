from typing import TYPE_CHECKING

from base_cell import Cell

if TYPE_CHECKING:
    from .game import Game


class Castle(Cell):
    def __init__(self, game: "Game", x: int, y: int, team: int):
        super().__init__(game, x, y, 0, team)
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                game.map_borders[game.map_coord(x + off_x, y + off_y)] = team + 1
        game.map_borders_changed = True
