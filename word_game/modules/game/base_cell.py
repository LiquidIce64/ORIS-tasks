from typing import TYPE_CHECKING

from PyQt6.QtCore import QPoint

if TYPE_CHECKING:
    from .game import Game


class Cell:
    def __init__(self, game: "Game", x: int, y: int, cell_type: int, team: int):
        self.game = game
        self.location = QPoint(x, y)
        self.cell_type = cell_type
        self.team = team
        game.map_cells[game.map_coord(self.location)] = self
        game.map_cells_changed = True

    def select(self): ...
