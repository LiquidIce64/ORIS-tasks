from __future__ import annotations
from typing import TYPE_CHECKING
from random import choice

from PyQt6.QtCore import QPoint

from .units import Settler, Warrior, Swordsman, Archer, ShieldBearer

if TYPE_CHECKING:
    from .game import Game
    from .game_server import GameServer


class Cell:
    CELL_TYPE = 0
    NAME = ""
    DAMAGEABLE = False

    def __init__(self, game: "Game" | "GameServer", x: int, y: int, team: int):
        self.game = game
        self.location = QPoint(x, y)
        self.team = team
        game.map_cells[game.map_coord(self.location)] = self
        game.map_cells_changed = True

    def select(self): ...

    def apply_damage(self, damage: int): ...


class Castle(Cell):
    CELL_TYPE = 0
    NAME = "Castle"
    DAMAGEABLE = True
    MAX_HEALTH = 50

    def __init__(self, game: "Game" | "GameServer", x: int, y: int, team: int):
        super().__init__(game, x, y, team)
        self.health = self.MAX_HEALTH
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                game.map_borders[game.map_coord(x + off_x, y + off_y)] = team + 1
        game.map_borders_changed = True

    def select(self):
        self.game.clear_selection()
        if self.game.current_team != self.team: return
        # self.game.selected_tile = self.location

        # DEBUG
        unit = choice((
            Settler,
            Warrior,
            Swordsman,
            Archer,
            ShieldBearer
        ))(self.game, self.location.x(), self.location.y(), self.team)
        self.game.comm.send_queue.put({
            "type": "game-event",
            "game-event": "create-unit",
            "body": {
                "type": unit.UNIT_TYPE,
                "pos": (self.location.x(), self.location.y()),
                "team": self.team
            }
        })

    def apply_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.game.remove_team(self.team)


CELL_TYPES = {
    0: Castle
}
