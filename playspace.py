import numpy as np
import pygame as pg
from dataclasses import dataclass

from rich import print

@dataclass
class Cell:
    # класс клетки
    surface: pg.surface.Surface
    global_rect: pg.Rect
    rect: pg.Rect


@dataclass
class Flags:
    PLAY_RUN: bool = False
    CREATE: bool = False
    GET_SETT: bool = False


class PlaySpace:
    
    def __init__(self, width, height, pos_x, pos_y, background=None, empty_color=(50,50,50,100)):
        # width: int - ширина
        # height: int - высота
        # pox_x: int - позиция X
        # pos_y: int - позиция Y
        # background: None | tuple | pg.Surface - задний фон, цвет или изображение
        # empty_color: tuple - цвет пустой клетки
        # matrix: np.array - матрица из 0 и 1
        # show_matrix: list[list[pg.Surface]] - 2D массив для отображения matrix
        # color: tuple - цвет не пустой (живой) клетки
        # clicked_left: bool - нажата ли левая кнопка мыши
        # surface: pg.Surface 
        # original: pg.Surface
        # row: int
        # column: int
        # space_size: int - расстояние между клетками
        # block_size: int - размер клетки
        self.width = width
        self.height = height
        self.size = width, height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = pos_x, pos_y
        self.matrix = np.zeros((3, 3), dtype=np.uint8)
        self.empty_color = empty_color
        self.empty_alpha = self.empty_color[-1] if len(self.empty_color) == 4 else 100
        self.color = (43, 199, 3)
        self.show_matrix = []
        self.clicked_left = False
        self.bgcolor = None
        
        if background is not None and isinstance(background, pg.surface.Surface):
            self.original = background.copy()
            self.original = pg.transform.scale(self.original, (self.width, self.height))
        elif background is not None and isinstance(background, (tuple, set, list)):
            self.original = pg.Surface((width, height))
            self.bgcolor = background
        elif background is None:
            self.original = pg.Surface((width, height))
            self.bgcolor = (200, 200, 100)
        else:
            raise TypeError('параметр background может быть pg.surface.Surface, tuple, list, set или None')
        
        self.surface = self.original.copy()
        self.row, self.column = self.matrix.shape[:2]
        self.rect = self.surface.get_rect(topleft=self.pos)
        
        self.space_size = 1 # размер отступа между клетками
        self.block_size = None # размер клетки
        
    
    
    def set_matrix(self, matrix):
        self.matrix = matrix.copy()
        self.row, self.column = self.matrix.shape[:2]
    
    
    def create_surface_matrix(self):
        # создание матрицы из pg.Surface на основе матрицы из 0 и 1
        self.show_matrix.clear()
        spaces_count_row = self.row + 1
        spaces_count_col = self.column + 1
        
        spaces_size_row = self.space_size * spaces_count_row
        spaces_size_col = self.space_size * spaces_count_col
        h, w = self.matrix.shape[:2]
        size = 0
        if self.width > self.height:
            if w <= h:
                height = self.height - spaces_size_row
                size = height // self.row
            else:
                width = self.width - spaces_size_col
                size = width // self.column
        elif self.height >= self.width and w >= h:
            if w >= h:
                width = self.width - spaces_size_col
                size = width // self.column
            else:
                height = self.height - spaces_size_row
                size = height // self.row
        self.block_size = size # размер каждой клетки
        pos = [self.space_size, self.space_size] # позиция первой клетки
        for i, row in enumerate(self.matrix):
            tmp_row = []
            for j, val in enumerate(row):
                surf = pg.Surface((self.block_size, self.block_size)).convert_alpha()
                if val != 1: surf.fill(self.empty_color)
                else: surf.fill(self.color)
                g_rect = surf.get_rect(topleft=(pos[0]+self.pos_x, pos[1]+self.pos_y))
                rect = surf.get_rect(topleft=(pos[0], pos[1]))
                cell = Cell(surf, g_rect, rect)
                tmp_row.append(cell)
                pos[0] += self.block_size + self.space_size
            self.show_matrix.append(tmp_row)
            pos[0] = self.space_size
            pos[1] += self.block_size + self.space_size
    
    
    def listen(self, events=None):
        # прослушивание событий мыши
        if not events:
            events = pg.event.get()
        events = list(filter(lambda x: x.type == pg.MOUSEBUTTONDOWN, events))
        if events and events[0].button == 1:
            mouse_pos = pg.mouse.get_pos()
            for i, row in enumerate(self.show_matrix):
                for j, cell in enumerate(row):
                    if cell.global_rect.collidepoint(mouse_pos):
                        self.matrix[i,j] = 0 if self.matrix[i,j] == 1 else 1
                        return i, j
    
    
    def draw(self, surface):
        self.surface = self.original.copy()
        if self.bgcolor:
            self.surface.fill(self.bgcolor)
        sz = 0
        for i, row in enumerate(self.show_matrix):
            for j, cell in enumerate(row):
                sz = cell.surface
                if self.matrix[i, j] == 1:
                    cell.surface.fill(self.color)
                else:
                    cell.surface.fill(self.empty_color)
                self.surface.blit(cell.surface, cell.rect)
        surface.blit(self.surface, self.pos)















