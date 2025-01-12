from typing import TYPE_CHECKING
from random import choice

from PyQt6.QtCore import QPoint

from units import Settler, Warrior, Swordsman, Archer, ShieldBearer

if TYPE_CHECKING:
    from .game import Game


class Cell:
    CELL_TYPE = 0
    DAMAGEABLE = False

    def __init__(self, game: "Game", x: int, y: int, team: int):
        self.game = game
        self.location = QPoint(x, y)
        self.team = team
        game.map_cells[game.map_coord(self.location)] = self
        game.map_cells_changed = True

    def select(self): ...

    def apply_damage(self, damage: int): ...


class Castle(Cell):
    CELL_TYPE = 0
    DAMAGEABLE = True
    MAX_HEALTH = 50

    def __init__(self, game: "Game", x: int, y: int, team: int):
        super().__init__(game, x, y, team)
        self.health = self.MAX_HEALTH
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                game.map_borders[game.map_coord(x + off_x, y + off_y)] = team + 1
        game.map_borders_changed = True

    def select(self):
        if self.game.current_team != self.team:
            self.game.clear_selection()
            return

        # DEBUG
        unit = choice((
            Settler,
            Warrior,
            Swordsman,
            Archer,
            ShieldBearer
        ))(self.game, self.location.x(), self.location.y(), self.team)

    def apply_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.game.remove_team(self.team)
