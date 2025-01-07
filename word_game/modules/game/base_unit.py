from typing import TYPE_CHECKING

from PyQt6.QtCore import QPoint

if TYPE_CHECKING:
    from .game import Game


class Unit:
    def __init__(self, game: "Game", x: int, y: int, unit_type: int, team: int):
        self.game = game
        self.location = QPoint(x, y)
        self.unit_type = unit_type
        self.team = team
        game.map_units[game.map_coord(self.location)] = self
        game.map_units_changed = True
