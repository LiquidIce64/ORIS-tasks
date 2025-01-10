from typing import TYPE_CHECKING

from PyQt6.QtCore import QPoint

if TYPE_CHECKING:
    from .game import Game


class Unit:
    UNIT_TYPE = 0
    ATTACK_DAMAGE = 3
    MAX_HEALTH = 10

    def __init__(self, game: "Game", x: int, y: int, team: int):
        self.game = game
        self.location = QPoint(x, y)
        self.team = team
        self.health = self.MAX_HEALTH
        self.has_moved = False
        self.can_select = True
        game.map_units[game.map_coord(self.location)] = self
        game.map_units_changed = True

    def select(self):
        if not self.can_select or self.game.current_turn != self.team:
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
        unit = self.game.map_units[self.game.map_coord(x, y)]
        if unit is None: return 0
        if unit.team == self.team: return -1
        return 1

    def move(self, x: int, y: int, is_attack=False):
        self.game.clear_selection()
        if is_attack:
            self.game.map_units[self.game.map_coord(x, y)].apply_damage(self.ATTACK_DAMAGE)
            self.has_moved = True
            self.can_select = False
        else:
            self.game.map_units[self.game.map_coord(x, y)] = self
            self.game.map_units[self.game.map_coord(self.location)] = None
            self.location = QPoint(x, y)
            self.has_moved = True

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
    def move(self, x: int, y: int, is_attack=False):
        super().move(x, y, is_attack)
        if not is_attack:
            self.game.map_borders[self.game.map_coord(x, y)] = self.team + 1
            self.game.map_borders_changed = True


class Warrior(Unit):
    UNIT_TYPE = 1
    ATTACK_DAMAGE = 5
    MAX_HEALTH = 15


class Swordsman(Unit):
    UNIT_TYPE = 2
    ATTACK_DAMAGE = 15
    MAX_HEALTH = 15


class Archer(Unit):
    UNIT_TYPE = 3
    ATTACK_DAMAGE = 8
    MAX_HEALTH = 15

    def get_moves(self):
        for off_x in range(-2, 3):
            for off_y in range(-2, 3):
                yield (self.location.x() + off_x, self.location.y() + off_y,
                       max(abs(off_x), abs(off_y)) < 2, True)


class ShieldBearer(Unit):
    UNIT_TYPE = 4
    MAX_HEALTH = 40
