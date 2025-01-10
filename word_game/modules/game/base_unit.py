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

    def select(self):
        self.game.selected_tile = self.location
        self.game.possible_moves.clear()
        for move_x, move_y in self.get_moves():
            move_check = self.check_move(move_x, move_y)
            if move_check == -1: continue
            self.game.possible_moves[move_x, move_y] = move_check == 1
        self.game.selection_changed = True

    def get_moves(self):
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                yield self.location.x() + off_x, self.location.y() + off_y

    def check_move(self, x: int, y: int):
        if x < 0 or x >= self.game.map_size or\
           y < 0 or y >= self.game.map_size or\
           x == self.location.x() and y == self.location.y(): return -1
        unit = self.game.map_units[self.game.map_coord(x, y)]
        if unit is None: return 0
        if unit.team == self.team: return -1
        return 1

    def move(self, x: int, y: int):
        self.game.clear_selection()
        self.game.map_units[self.game.map_coord(x, y)] = self
        self.game.map_units[self.game.map_coord(self.location)] = None
        self.location = QPoint(x, y)
        self.game.map_units_changed = True
