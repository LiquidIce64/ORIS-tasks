from __future__ import annotations
from typing import overload

import numpy as np

from PyQt6.QtCore import Qt, QObject, QPoint

from game_widget import GameWidget
from units import Unit
from cells import Cell, Castle


class Game(QObject):
    def __init__(self, map_size=16):
        super().__init__()
        self.map_size = map_size

        self.map_borders = np.zeros((map_size * map_size,), dtype=np.int32)
        self.map_units: list[Unit | None] = [None] * (map_size * map_size)
        self.map_cells: list[Cell | None] = [None] * (map_size * map_size)

        self.current_turn = 0
        self.selected_tile = QPoint(-1, -1)
        self.possible_moves: dict[tuple[int, int], bool] = {}

        self.map_borders_changed = True
        self.map_units_changed = True
        self.map_cells_changed = True
        self.selection_changed = True

        Castle(self, 1, 1, 0)
        Castle(self, map_size - 2, map_size - 2, 1)
        Castle(self, map_size - 2, 1, 2)
        Castle(self, 1, map_size - 2, 3)

        self.widget = GameWidget(self)

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

    def on_click(self, x, y, btn: Qt.MouseButton):
        x = int(x * self.map_size)
        y = int(y * self.map_size)
        i = x + self.map_size * y
        if btn == btn.LeftButton:
            if x == self.selected_tile.x() and y == self.selected_tile.y():
                self.clear_selection()
            elif (x, y) in self.possible_moves:
                self.map_units[self.map_coord(self.selected_tile)].move(x, y, self.possible_moves[x, y])
            elif (unit := self.map_units[i]) is not None:
                unit.select()
            elif (cell := self.map_cells[i]) is not None:
                cell.select()
            else:
                self.clear_selection()

            self.widget.repaint()

    def clear_selection(self):
        self.selected_tile = QPoint(-1, -1)
        self.possible_moves.clear()
        self.selection_changed = True

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % 4

        for unit in self.map_units:
            if unit is None: continue
            if unit.team != self.current_turn: continue
            unit.has_moved = False
            unit.can_select = True


if __name__ == '__main__':
    from warnings import filterwarnings

    from PyQt6.QtCore import QDir
    from PyQt6.QtWidgets import QApplication, QMainWindow

    QDir.addSearchPath("textures", "modules/game/textures")
    QDir.addSearchPath("shaders", "modules/game/shaders")

    filterwarnings(action="ignore", message="sipPyTypeDict()", category=DeprecationWarning)


    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.resize(512, 512)
            self.setWindowTitle('OpenGL Test')
            self.game = Game()
            self.setCentralWidget(self.game.widget)

        def resizeEvent(self, event):
            w, h = self.width(), self.height()
            if w == h: return
            new_size = min(w, h)
            self.resize(new_size, new_size)


    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec()
