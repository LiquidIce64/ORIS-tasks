from __future__ import annotations
from typing import overload, TYPE_CHECKING

import numpy as np

from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel

from .gui import Ui_Game

from .game_renderer import GameRenderer
from .units import Unit, UNIT_TYPES
from .cells import Cell, Castle

if TYPE_CHECKING:
    from strategy_game.modules.communication import Communication


class Game(QWidget, Ui_Game):
    def __init__(self, comm: "Communication", map_size=16, starting_money=100):
        super().__init__()
        self.setupUi(self)

        self.comm = comm
        self.map_size = map_size
        self.starting_money = starting_money

        self.map_borders = np.zeros((map_size * map_size,), dtype=np.int32)
        self.map_units: list[Unit | None] = [None] * (map_size * map_size)
        self.map_cells: list[Cell | None] = [None] * (map_size * map_size)

        self.remaining_teams: dict[str, int] = {}
        self.current_team = -1
        self.selected_tile = QPoint(-1, -1)
        self.possible_moves: dict[tuple[int, int], bool] = {}
        self.castle: Castle | None = None
        self.money = starting_money - 9
        self.label_money.setText(str(starting_money))

        self.map_borders_changed = True
        self.map_units_changed = True
        self.map_cells_changed = True
        self.selection_changed = True

        self.renderer = GameRenderer(self)
        self.layout_renderer.addWidget(self.renderer)

        self.frame_selection.setVisible(False)

        self.unit_btns = {}
        coin_pixmap = QPixmap("res:/icons/coin.png")
        for unit_type, unit_cls in UNIT_TYPES.items():
            btn = QPushButton(unit_cls.NAME)
            btn.setEnabled(False)
            btn.clicked.connect(lambda *_, unit=unit_cls: self.unit_btn_clicked(unit))
            icon = QLabel()
            icon.setPixmap(coin_pixmap)
            icon.setMaximumSize(16, 16)
            icon.setScaledContents(True)
            cost = QLabel(str(unit_cls.COST))
            self.layout_castle.addWidget(btn, unit_type + 1, 0)
            self.layout_castle.addWidget(icon, unit_type + 1, 1)
            self.layout_castle.addWidget(cost, unit_type + 1, 2)
            self.unit_btns[unit_type] = btn

    def unit_btn_clicked(self, unit):
        if self.money < unit.COST: return
        x, y = self.castle.location.x(), self.castle.location.y()
        if self.map_units[self.map_coord(x, y)] is not None: return
        self.money -= unit.COST
        unit(self, x, y, self.castle.team)
        self.comm.send_queue.put({
            "type": "game-event",
            "game-event": "create-unit",
            "body": unit.UNIT_TYPE
        })
        self.renderer.repaint()
        self.update_available_money()

    def update_available_money(self):
        self.label_money.setText(str(self.money))
        for unit_type, btn in self.unit_btns.items():
            btn.setEnabled(self.money >= UNIT_TYPES[unit_type].COST)

    def start_game(self, username: str):
        your_team = self.remaining_teams[username]
        for team, pos in zip(self.remaining_teams.values(), [
            (1, 1),
            (self.map_size - 2, self.map_size - 2),
            (self.map_size - 2, 1),
            (1, self.map_size - 2)
        ]):
            castle = Castle(self, pos[0], pos[1], team)
            if team == your_team: self.castle = castle

    @overload
    def map_coord(self, pos: QPoint) -> int: ...
    @overload
    def map_coord(self, x: int, y: int) -> int: ...

    def map_coord(self, *args) -> int:
        """
        map_coord(pos: QPoint)

        map_coord(x: int, y: int)
        """
        if len(args) == 1:
            pos: QPoint = args[0]
            return pos.x() + pos.y() * self.map_size
        else:
            x, y = args
            return x + y * self.map_size

    def on_game_widget_click(self, x, y, btn: Qt.MouseButton):
        x = int(x * self.map_size)
        y = int(y * self.map_size)
        i = x + self.map_size * y
        if btn == btn.LeftButton:
            if x == self.selected_tile.x() and y == self.selected_tile.y():
                self.clear_selection()
            elif (x, y) in self.possible_moves:
                is_attack = self.possible_moves[x, y]
                unit_idx = self.map_coord(self.selected_tile)
                self.map_units[unit_idx].move(x, y, is_attack)
                self.comm.send_queue.put({
                    "type": "game-event",
                    "game-event": "move",
                    "body": {
                        "unit": unit_idx,
                        "args": (x, y, is_attack)
                    }
                })
            elif (unit := self.map_units[i]) is not None:
                unit.select()
            elif (cell := self.map_cells[i]) is not None:
                cell.select()
            else:
                self.clear_selection()
            self.renderer.repaint()

    def on_game_widget_hover(self, x, y):
        if not self.remaining_teams: return
        x = int(x * self.map_size)
        y = int(y * self.map_size)
        if x == self.map_size: x -= 1
        if y == self.map_size: y -= 1
        i = x + self.map_size * y

        if (unit := self.map_units[i]) is not None:
            self.frame_selection.setVisible(True)
            self.label_attack.setVisible(True)
            self.icon_attack.setVisible(True)
            self.progress_health.setVisible(True)
            self.progress_health.setMaximum(unit.MAX_HEALTH)
            self.progress_health.setValue(unit.health)
            self.label_attack.setText(str(unit.ATTACK_DAMAGE))
            self.label_selection_name.setText(unit.NAME)

        elif (cell := self.map_cells[i]) is not None:
            self.frame_selection.setVisible(True)
            self.label_attack.setVisible(False)
            self.icon_attack.setVisible(False)
            if cell.DAMAGEABLE:
                self.progress_health.setVisible(True)
                self.progress_health.setMaximum(cell.MAX_HEALTH)
                self.progress_health.setValue(cell.health)
            else:
                self.progress_health.setVisible(False)
            self.label_selection_name.setText(cell.NAME)

        else: self.frame_selection.setVisible(False)

    def clear_selection(self):
        self.selected_tile = QPoint(-1, -1)
        self.possible_moves.clear()
        self.selection_changed = True

    def make_move(self, move_info: dict):
        try:
            unit: Unit = self.map_units[move_info["unit"]]
            x, y, is_attack = move_info["args"]
            x = int(x)
            y = int(y)
            is_attack = bool(is_attack)
            unit.move(x, y, is_attack)
            self.renderer.repaint()
        except: return

    def next_turn(self, next_team_or_player):
        self.clear_selection()
        if isinstance(next_team_or_player, int):
            self.current_team = next_team_or_player
        else:
            self.current_team = self.remaining_teams[next_team_or_player]

        for unit, border in zip(self.map_units, self.map_borders):
            if border > 0 and border - 1 == self.current_team: self.money += 1
            if unit is None: continue
            unit.has_moved = False
            unit.can_select = unit.team == self.current_team

        if self.current_team != -1: self.update_available_money()

        self.map_units_changed = True
        self.renderer.repaint()

    def create_unit(self, unit_info: dict):
        try:
            x, y = unit_info["pos"]
            unit = UNIT_TYPES[unit_info["type"]](self, x, y, unit_info["team"])
            unit.can_select = False
            self.renderer.repaint()
        except: raise Exception()

    def remove_team(self, team_or_player):
        if isinstance(team_or_player, int):
            team = team_or_player
            for k, v in self.remaining_teams.items():
                if v == team:
                    username = k
                    break
            else: return
        else:
            username: str = team_or_player
            if username not in self.remaining_teams: return
            team = self.remaining_teams[username]
        self.remaining_teams.pop(username)

        for i in range(len(self.map_units)):
            if (unit := self.map_units[i]) is not None and unit.team == team: self.map_units[i] = None
            if (cell := self.map_cells[i]) is not None and cell.team == team: self.map_cells[i] = None
            if self.map_borders[i] == team + 1: self.map_borders[i] = 0
        self.map_units_changed = True
        self.map_cells_changed = True
        self.map_borders_changed = True
        self.renderer.repaint()

    def resizeEvent(self, event):
        new_size = min(self.frame_renderer_outside.width(), self.frame_renderer_outside.height()) - 2
        self.frame_renderer.setMaximumSize(new_size, new_size)
