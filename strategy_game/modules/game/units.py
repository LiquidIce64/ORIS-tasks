from __future__ import annotations
from typing import TYPE_CHECKING

from PyQt6.QtCore import QPoint

if TYPE_CHECKING:
    from .game import Game
    from .game_server import GameServer


class Unit:
    UNIT_TYPE = 0
    NAME = ""
    COST = 15
    ATTACK_DAMAGE = 3
    MAX_HEALTH = 10

    def __init__(self, game: "Game" | "GameServer", x: int, y: int, team: int):
        self.game = game
        self.location = QPoint(x, y)
        self.team = team
        self.health = self.MAX_HEALTH
        self.has_moved = False
        self.can_select = True
        game.map_units[game.map_coord(self.location)] = self
        game.map_units_changed = True

    def select(self):
        if not self.can_select or self.game.current_team != self.team:
            self.game.clear_selection()
            return

        self.game.selected_tile = self.location
        self.game.possible_moves.clear()
        for move_x, move_y, can_move, can_attack in self.get_moves():
            move_check = self.check_move(move_x, move_y)
            if move_check == -1: continue
            if move_check == 0 and can_move and not self.has_moved:
                self.game.possible_moves[move_x, move_y] = False
            if move_check == 1 and can_attack:
                self.game.possible_moves[move_x, move_y] = True
        self.game.selection_changed = True

    def get_moves(self):
        for off_x in range(-1, 2):
            for off_y in range(-1, 2):
                yield (self.location.x() + off_x, self.location.y() + off_y,
                       True, True)

    def check_move(self, x: int, y: int):
        if x < 0 or x >= self.game.map_size or\
           y < 0 or y >= self.game.map_size or\
           x == self.location.x() and y == self.location.y(): return -1
        i = self.game.map_coord(x, y)
        if (unit := self.game.map_units[i]) is not None:
            return -1 if unit.team == self.team else 1
        if (cell := self.game.map_cells[i]) is not None:
            return 0 if cell.team == self.team else (1 if cell.DAMAGEABLE else 0)
        return 0

    def move(self, x: int, y: int, is_attack=False):
        self.game.clear_selection()
        if is_attack:
            i = self.game.map_coord(x, y)
            if (unit := self.game.map_units[i]) is not None: unit.apply_damage(self.ATTACK_DAMAGE)
            elif (cell := self.game.map_cells[i]) is not None: cell.apply_damage(self.ATTACK_DAMAGE)
            self.has_moved = True
            self.can_select = False
        else:
            self.game.map_units[self.game.map_coord(x, y)] = self
            self.game.map_units[self.game.map_coord(self.location)] = None
            self.location = QPoint(x, y)
            self.has_moved = True

            if self.team == self.game.current_team:
                self.game.selected_tile = self.location
                for move_x, move_y, can_move, can_attack in self.get_moves():
                    if not can_attack: continue
                    move_check = self.check_move(move_x, move_y)
                    if move_check == 1:
                        self.game.possible_moves[move_x, move_y] = True
                if len(self.game.possible_moves) == 0:
                    self.can_select = False
                    self.game.clear_selection()
        self.game.map_units_changed = True

    def apply_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.game.map_units[self.game.map_coord(self.location)] = None
            self.game.map_units_changed = True


class Settler(Unit):
    NAME = "Settler"

    def move(self, x: int, y: int, is_attack=False):
        super().move(x, y, is_attack)
        i = self.game.map_coord(x, y)
        if not is_attack and self.game.map_borders[i] != self.team + 1:
            self.game.map_borders[i] = self.team + 1
            self.game.map_borders_changed = True
            self.apply_damage(2)


class Warrior(Unit):
    UNIT_TYPE = 1
    NAME = "Warrior"
    COST = 25
    ATTACK_DAMAGE = 5
    MAX_HEALTH = 15


class Swordsman(Unit):
    UNIT_TYPE = 2
    NAME = "Swordsman"
    COST = 50
    ATTACK_DAMAGE = 15
    MAX_HEALTH = 15


class Archer(Unit):
    UNIT_TYPE = 3
    NAME = "Archer"
    COST = 35
    ATTACK_DAMAGE = 8
    MAX_HEALTH = 15

    def get_moves(self):
        for off_x in range(-2, 3):
            for off_y in range(-2, 3):
                yield (self.location.x() + off_x, self.location.y() + off_y,
                       max(abs(off_x), abs(off_y)) < 2, True)


class ShieldBearer(Unit):
    UNIT_TYPE = 4
    NAME = "ShieldBearer"
    COST = 40
    MAX_HEALTH = 40


UNIT_TYPES = {
    0: Settler,
    1: Warrior,
    2: Swordsman,
    3: Archer,
    4: ShieldBearer
}
