from __future__ import annotations
from typing import overload

import numpy as np

from PyQt6.QtCore import Qt, QObject, QPoint

from game_widget import GameWidget
from base_unit import Unit
from base_cell import Cell
from castle import Castle


class Game(QObject):
    def __init__(self, map_size=16):
        super().__init__()
        self.map_size = map_size

        self.map_borders = np.zeros((map_size * map_size,), dtype=np.int32)
        self.map_units: list[Unit | None] = [None] * (map_size * map_size)
        self.map_cells: list[Cell | None] = [None] * (map_size * map_size)
        self.map_borders_changed = True
        self.map_units_changed = True
        self.map_cells_changed = True

        self.selected_tile = QPoint(-1, -1)
        self.possible_moves = []

        Castle(self, 1, 1, 0)
        Castle(self, map_size - 2, map_size - 2, 1)
        Castle(self, map_size - 2, 1, 2)
        Castle(self, 1, map_size - 2, 3)

        # DEBUG
        Unit(self, 4, 1, 1, 0)
        Unit(self, 5, 1, 2, 1)
        Unit(self, 5, 2, 0, 2)
        Unit(self, 4, 2, 9, 3)

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
            self.map_borders[i] = (self.map_borders[i] + 1) % 5
            self.map_borders_changed = True
            self.widget.repaint()


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
