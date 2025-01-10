from __future__ import annotations
from typing import TYPE_CHECKING

import ctypes
import numpy as np
import OpenGL.GL as gl
from OpenGL.arrays.vbo import VBO

from PyQt6.QtGui import QSurfaceFormat, QImage, QMouseEvent
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtOpenGL import (
    QOpenGLVersionProfile,
    QOpenGLTexture,
    QOpenGLShader,
    QOpenGLShaderProgram,
    QOpenGLFramebufferObject
)

if TYPE_CHECKING:
    from .game import Game


class GameWidget(QOpenGLWidget):
    def __init__(self, game: "Game"):
        self.game = game

        self.prog_map: QOpenGLShaderProgram | None = None
        self.prog_instanced: QOpenGLShaderProgram | None = None

        self.tex_ground: QOpenGLTexture | None = None
        self.tex_units: QOpenGLTexture | None = None
        self.tex_cells: QOpenGLTexture | None = None
        self.tex_selection: QOpenGLTexture | None = None

        self.fbo_render: QOpenGLFramebufferObject | None = None
        self.fbo_scaled: QOpenGLFramebufferObject | None = None
        self.vbo_map: VBO | None = None
        self.vbo_quad: VBO | None = None

        self.buf_borders = None
        self.buf_units = None
        self.buf_cells = None
        self.buf_selection = None
        self.data_units = None
        self.data_cells = None
        self.data_selection = None

        super().__init__()

        min_size = game.map_size * 16
        self.setMinimumSize(min_size, min_size)

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.pos()
        x = pos.x() / self.width()
        y = 1.0 - pos.y() / self.height()
        self.game.on_click(x, y, event.button())

    def initializeGL(self):
        prof = QOpenGLVersionProfile()
        prof.setVersion(4, 3)
        prof.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)

        gl.glEnable(gl.GL_MULTISAMPLE)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        self.initShaders()
        self.initGeometry()
        self.initTextures()

    @staticmethod
    def loadShaderProgram(*shader_filenames: str):
        program = QOpenGLShaderProgram()
        for filename in shader_filenames:
            if filename.endswith("vert"): shader_type = QOpenGLShader.ShaderTypeBit.Vertex
            elif filename.endswith("frag"): shader_type = QOpenGLShader.ShaderTypeBit.Fragment
            else: raise NotImplementedError(f"Unknown shader type ({filename})")
            program.addCacheableShaderFromSourceFile(shader_type, filename)
        return program

    def ScaleFBO(self):
        w = self.width() * self.devicePixelRatio()
        size = 1
        while size < w: size *= 2
        if size != w: size *= 2
        if self.fbo_scaled is None or size != self.fbo_scaled.width():
            self.fbo_scaled = QOpenGLFramebufferObject(size, size)

    def initShaders(self):
        fbo_size = self.game.map_size * 16
        self.fbo_render = QOpenGLFramebufferObject(fbo_size, fbo_size)
        self.ScaleFBO()

        # Map
        self.prog_map = self.loadShaderProgram("shaders:map.vert", "shaders:map.frag")
        self.prog_map.bind()
        self.prog_map.setUniformValue("texture", 0)
        self.prog_map.setUniformValue("map_size", self.game.map_size)
        self.buf_borders = gl.glGenBuffers(1)
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 2, self.buf_borders)

        # Instanced
        self.prog_instanced = self.loadShaderProgram("shaders:instanced.vert", "shaders:instanced.frag")
        self.prog_instanced.bind()
        self.prog_map.setUniformValue("texture", 0)
        self.prog_map.setUniformValue("map_size", self.game.map_size)
        self.buf_units, self.buf_cells, self.buf_selection = gl.glGenBuffers(3)

    def initGeometry(self):
        quad_vertices = np.array([
            +1.0, +1.0, 1.0, 1.0,
            -1.0, +1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0,
            +1.0, -1.0, 1.0, 0.0
        ], dtype=np.float32)

        self.vbo_map = VBO(quad_vertices * self.game.map_size, usage=gl.GL_STATIC_DRAW)
        self.vbo_map.bind()
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(1)
        gl.glVertexAttribPointer(1, 2, gl.GL_FLOAT, gl.GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))

        self.vbo_quad = VBO(quad_vertices, usage=gl.GL_STATIC_DRAW)
        self.vbo_quad.bind()
        gl.glEnableVertexAttribArray(2)
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 4 * 4, ctypes.c_void_p(0))
        gl.glEnableVertexAttribArray(3)
        gl.glVertexAttribPointer(3, 2, gl.GL_FLOAT, gl.GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))

    @staticmethod
    def loadTexture(filename: str):
        texture = QOpenGLTexture(QImage("textures:" + filename))
        texture.setMagnificationFilter(QOpenGLTexture.Filter.Nearest)
        texture.setMinificationFilter(QOpenGLTexture.Filter.Nearest)
        texture.setWrapMode(QOpenGLTexture.WrapMode.Repeat)
        return texture

    def initTextures(self):
        self.tex_ground = self.loadTexture("ground.png")
        self.tex_units = self.loadTexture("units.png")
        self.tex_cells = self.loadTexture("cells.png")
        self.tex_selection = self.loadTexture("selection.png")

    def updateData(self):
        if self.game.map_borders_changed:
            self.game.map_borders_changed = False
            gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.buf_borders)
            gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, self.game.map_borders, gl.GL_DYNAMIC_DRAW)

        if self.game.map_units_changed:
            self.game.map_units_changed = False
            self.data_units = np.array([
                [
                    unit.location.x(),
                    unit.location.y(),
                    unit.UNIT_TYPE,
                    -unit.team - 1 if unit.can_select else unit.team
                ] for unit in self.game.map_units if unit is not None
            ], dtype=np.float32)
            gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.buf_units)
            gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, self.data_units, gl.GL_DYNAMIC_DRAW)

        if self.game.map_cells_changed:
            self.game.map_cells_changed = False
            self.data_cells = np.array([
                [cell.location.x(), cell.location.y(), cell.CELL_TYPE, cell.team]
                for cell in self.game.map_cells if cell is not None
            ], dtype=np.float32)
            gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.buf_cells)
            gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, self.data_cells, gl.GL_DYNAMIC_DRAW)

        if self.game.selection_changed:
            self.game.selection_changed = False
            self.data_selection = np.array(
                [[self.game.selected_tile.x(), self.game.selected_tile.y(), 0, 4]] +
                [
                    [pos[0], pos[1], 0, 6 if is_attack else 5]
                    for pos, is_attack in self.game.possible_moves.items()
                ], dtype=np.float32)
            gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.buf_selection)
            gl.glBufferData(gl.GL_SHADER_STORAGE_BUFFER, self.data_selection, gl.GL_DYNAMIC_DRAW)

    def paintGL(self):
        self.updateData()
        self.fbo_render.bind()
        gl.glViewport(0, 0, self.fbo_render.width(), self.fbo_render.height())
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # Map
        self.prog_map.bind()
        gl.glBindBuffer(gl.GL_SHADER_STORAGE_BUFFER, self.buf_borders)
        self.tex_ground.bind()
        self.vbo_map.bind()
        gl.glDrawArrays(gl.GL_QUADS, 0, 4)

        # Instanced
        self.prog_instanced.bind()
        self.vbo_quad.bind()
        # Cells
        self.tex_cells.bind()
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 3, self.buf_cells)
        gl.glDrawArraysInstanced(gl.GL_QUADS, 0, 4, len(self.data_cells))
        # Units
        self.tex_units.bind()
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 3, self.buf_units)
        gl.glDrawArraysInstanced(gl.GL_QUADS, 0, 4, len(self.data_units))
        # Selection
        self.tex_selection.bind()
        gl.glBindBufferBase(gl.GL_SHADER_STORAGE_BUFFER, 3, self.buf_selection)
        gl.glDrawArraysInstanced(gl.GL_QUADS, 0, 4, len(self.data_selection))

        QOpenGLFramebufferObject.blitFramebuffer(self.fbo_scaled, self.fbo_render)
        gl.glBindFramebuffer(gl.GL_READ_FRAMEBUFFER, self.fbo_scaled.handle())
        gl.glBindFramebuffer(gl.GL_DRAW_FRAMEBUFFER, self.defaultFramebufferObject())
        gl.glBlitFramebuffer(
            0, 0, self.fbo_scaled.width(), self.fbo_scaled.height(),
            0, 0, int(self.width() * self.devicePixelRatio() + 0.5), int(self.height() * self.devicePixelRatio() + 0.5),
            gl.GL_COLOR_BUFFER_BIT, gl.GL_LINEAR
        )

    def resizeGL(self, w, h):
        self.ScaleFBO()
