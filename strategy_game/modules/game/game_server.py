from __future__ import annotations
from typing import overload, TYPE_CHECKING, Iterable

import numpy as np

from PyQt6.QtCore import QPoint, QObject, QTimer

from .units import Unit, UNIT_TYPES
from .cells import Cell, Castle

if TYPE_CHECKING:
    from strategy_game.modules.room_list_item import ServerRoomListItem


class GameServer(QObject):
    def __init__(self, room: "ServerRoomListItem", map_size=16, starting_money=100):
        super().__init__()
        self.room = room
        self.map_size = map_size
        self.starting_money = starting_money

        self.map_borders = np.zeros((map_size * map_size,), dtype=np.int32)
        self.map_units: list[Unit | None] = [None] * (map_size * map_size)
        self.map_cells: list[Cell | None] = [None] * (map_size * map_size)

        self.remaining_teams: dict[str, int] = {}
        self.current_team = -1
        self.current_team_idx = -1
        self.possible_moves: dict[tuple[int, int], bool] = {}
        self.teams_money: dict[int, int] = {}
        self.teams_castles: dict[int, Castle] = {}

        self.turn_timer = QTimer()
        self.turn_timer.timeout.connect(self.next_turn)

        # Unused attributes left for compatibility
        self.selected_tile = QPoint(-1, -1)
        self.map_borders_changed = True
        self.map_units_changed = True
        self.map_cells_changed = True
        self.selection_changed = True

    def start_game(self, player_list: Iterable[str]):
        self.remaining_teams = {username: team for team, username in enumerate(player_list)}
        self.teams_money = {team: self.starting_money - 9 for team in self.remaining_teams.values()}
        for team, pos in zip(self.remaining_teams.values(), [
            (1, 1),
            (self.map_size - 2, self.map_size - 2),
            (self.map_size - 2, 1),
            (1, self.map_size - 2)
        ]): self.teams_castles[team] = Castle(self, pos[0], pos[1], team)
        self.next_turn()

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

    def clear_selection(self):
        self.selected_tile = QPoint(-1, -1)
        self.possible_moves.clear()
        self.selection_changed = True

    def make_move(self, move_info: dict):
        try:
            unit_idx = move_info["unit"]
            unit: Unit = self.map_units[unit_idx]
            x, y, is_attack = move_info["args"]
            x = int(x)
            y = int(y)
            is_attack = bool(is_attack)
            unit.select()
            if self.possible_moves[x, y] != is_attack: return
            unit.move(x, y, is_attack)
        except: return

        msg = {
            "type": "game-event",
            "game-event": "move",
            "body": {
                "unit": unit_idx,
                "args": (x, y, is_attack)
            }
        }
        for username, team in self.remaining_teams.items():
            if team == self.current_team: continue
            self.room.server.main.comm.send_queue.put((msg, self.room.server.clients[username]))

    def next_turn(self):
        self.turn_timer.stop()
        if len(self.remaining_teams) == 0: return
        self.current_team_idx = (self.current_team_idx + 1) % len(self.remaining_teams)
        next_player = list(self.remaining_teams.keys())[self.current_team_idx]
        next_team = self.remaining_teams[next_player]
        self.current_team = next_team

        msg = {
            "type": "game-event",
            "game-event": "turn",
            "body": next_player
        }
        for username in self.remaining_teams:
            self.room.server.main.comm.send_queue.put((msg, self.room.server.clients[username]))

        for unit, border in zip(self.map_units, self.map_borders):
            if border > 0 and border - 1 == self.current_team: self.teams_money[self.current_team] += 1
            if unit is None: continue
            unit.has_moved = False
            unit.can_select = unit.team == self.current_team
        self.turn_timer.start(120000)

    def create_unit(self, unit_type: int, from_player: str):
        try:
            team = self.remaining_teams[from_player]
            unit_cls = UNIT_TYPES[unit_type]
            if self.teams_money[team] < unit_cls.COST: return
            self.teams_money[team] -= unit_cls.COST
            castle = self.teams_castles[team]
            x, y = castle.location.x(), castle.location.y()
            unit_cls(self, x, y, team)
        except: return

        msg = {
            "type": "game-event",
            "game-event": "create-unit",
            "body": {
                "type": unit_type,
                "pos": (x, y),
                "team": team
            }
        }
        for username, team in self.remaining_teams.items():
            if team == self.current_team: continue
            self.room.server.main.comm.send_queue.put((msg, self.room.server.clients[username]))

    def remove_team(self, team_or_player, remove_player=True):
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
        if remove_player:
            self.room.server.main.comm.send_queue.put(({
                "type": "event",
                "event": "kick",
                "body": "Game over"
            }, self.room.server.clients[username]))
            self.room.server.leave_room(username)

        for i in range(len(self.map_units)):
            if (unit := self.map_units[i]) is not None and unit.team == team: self.map_units[i] = None
            if (cell := self.map_cells[i]) is not None and cell.team == team: self.map_cells[i] = None
            if self.map_borders[i] == team + 1: self.map_borders[i] = 0

        if self.current_team >= team:
            self.current_team_idx -= 1
            if self.current_team == team: self.next_turn()
