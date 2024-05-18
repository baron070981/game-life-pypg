import numpy as np
import random
import copy
import time
import os
from abc import ABC, abstractmethod
import itertools
from random import randint

from rich import print, inspect




class Matrix:
    
    def __init__(self):
        self.matrix = np.zeros((3,3), dtype=np.uint8)
    
    
    def __str__(self):
        return f'{self.matrix}'
    
    @property
    def mat(self):
        return self.matrix
    
    
    @classmethod
    def create_matrix(cls, cols, rows, fill_value=0, dtype=np.uint8):
        # создание двумерного массива размером rows X cols заполненого
        # значением fill_value с типом dtype
        fill_value = 0 if fill_value != 1 else 1
        return np.full((rows, cols), fill_value=fill_value, dtype=dtype)
    
    
    def mcreate_matrix(self, cols, rows, fill_value=0, dtype=np.uint8):
        # создание двумерного массива размером rows X cols заполненого
        # значением fill_value с типом dtype
        fill_value = 0 if fill_value != 1 else 1
        self.matrix = np.full((rows, cols), fill_value=fill_value, dtype=dtype)
        return copy.deepcopy(self.matrix)
    
    @classmethod
    def replace_value(cls, matrix: np.array, idx_row, idx_col, copy=False):
        # замена значения по индексам idx_row и idx_col
        # если значение по индексам не равно 0, то оно становится 0
        # если же равно 0, то становится 1
        # если copy = True, возвращает копию массива, не меняет оригинал
        # если copy = False, меняет исходный массив
        if not copy:
            val = matrix[idx_row, idx_col]
            if val != 0: val = 0
            else: val = 1
            matrix[idx_row, idx_col] = val
        else:
            m = copy.deepcopy(matrix)
            val = m[idx_row, idx_col]
            if val != 0: val = 0
            else: val = 1
            m[idx_row, idx_col] = val
            return m
    
    
    def mreplace_value(self, idx_row, idx_col):
        # замена значения по индексам idx_row и idx_col
        # если значение по индексам не равно 0, то оно становится 0
        # если же равно 0, то становится 1
        # если copy = True, возвращает копию массива, не меняет оригинал
        # если copy = False, меняет исходный массив
        val = self.matrix[idx_row, idx_col]
        if val != 0: val = 0
        else: val = 1
        self.matrix[idx_row, idx_col] = val
        return copy.deepcopy(self.matrix)
    
    
    @classmethod
    def get_cell_neighbors(cls, matrix: np.array, idx_row, idx_col) -> tuple:
        # поиск соседних позиций и получение значений из них
        # порядок соседних позиций: с верхней и по часовой стрелке
        # если нет соседа сверху, то начиная со следующего по часовой стрелке
        y, x = idx_row, idx_col
        h, w = matrix.shape[:2]
        m = matrix
        neighs = None
        # top left
        if x == y == 0:
            neighs = m[y,x+1], m[y+1,x+1], m[y+1,x]
        # top right
        elif x == w-1 and y == 0:
            neighs = m[y+1,x], m[y+1,x-1], m[y,x-1]
        # bottom right
        elif x == w-1 and y == h-1:
            neighs = m[y-1,x], m[y,x-1], m[y-1,x-1]
        # bottom left
        elif x == 0 and y == h-1:
            neighs = m[y-1,x], m[y-1,x+1], m[y,x+1]
        # top
        elif x > 0 and x < w-1 and y == 0:
            neighs = m[y,x+1], m[y+1,x+1], m[y+1,x], m[y+1,x-1], m[y,x-1]
        # right
        elif x == w-1 and y > 0  and y < h-1:
            neighs = m[y-1,x], m[y+1,x], m[y+1,x-1], m[y,x-1], m[y-1,x-1]
        # bottom
        elif x > 0 and x < w-1 and y == h-1:
            neighs = m[y-1,x], m[y-1,x+1], m[y,x+1], m[y,x-1], m[y-1,x-1]
        # left
        elif x == 0 and y > 0 and y < h-1:
            neighs = m[y-1,x], m[y-1,x+1], m[y,x+1], m[y+1,x+1], m[y+1,x]
        # center
        else:
            neighs = (m[y-1,x], m[y-1,x+1], m[y,x+1], m[y+1,x+1],
                      m[y+1,x], m[y+1,x-1], m[y,x-1], m[y-1,x-1])
        return neighs
    
    
    def mget_cell_neighbors(self, idx_row, idx_col) -> tuple:
        # поиск соседних позиций и получение значений из них
        # порядок соседних позиций: с верхней и по часовой стрелке
        # если нет соседа сверху, то начиная со следующего по часовой стрелке
        y, x = idx_row, idx_col
        h, w = self.matrix.shape[:2]
        m = self.matrix
        neighs = None
        # top left
        if x == y == 0:
            neighs = m[y,x+1], m[y+1,x+1], m[y+1,x]
        # top right
        elif x == w-1 and y == 0:
            neighs = m[y+1,x], m[y+1,x-1], m[y,x-1]
        # bottom right
        elif x == w-1 and y == h-1:
            neighs = m[y-1,x], m[y,x-1], m[y-1,x-1]
        # bottom left
        elif x == 0 and y == h-1:
            neighs = m[y-1,x], m[y-1,x+1], m[y,x+1]
        # top
        elif x > 0 and x < w-1 and y == 0:
            neighs = m[y,x+1], m[y+1,x+1], m[y+1,x], m[y+1,x-1], m[y,x-1]
        # right
        elif x == w-1 and y > 0  and y < h-1:
            neighs = m[y-1,x], m[y+1,x], m[y+1,x-1], m[y,x-1], m[y-1,x-1]
        # bottom
        elif x > 0 and x < w-1 and y == h-1:
            neighs = m[y-1,x], m[y-1,x+1], m[y,x+1], m[y,x-1], m[y-1,x-1]
        # left
        elif x == 0 and y > 0 and y < h-1:
            neighs = m[y-1,x], m[y-1,x+1], m[y,x+1], m[y+1,x+1], m[y+1,x]
        # center
        else:
            neighs = (m[y-1,x], m[y-1,x+1], m[y,x+1], m[y+1,x+1],
                      m[y+1,x], m[y+1,x-1], m[y,x-1], m[y-1,x-1])
        return neighs
    
    
    @classmethod
    def __get_cell_state(cls, value:int, neighs:tuple|list):
        n = sum(neighs)
        if value == 1 and n not in [2, 3]:
            return 0
        elif value == 1 and n in [2,3]:
            return 1
        elif value == 0 and n == 3:
            return 1
        return 0
    
    @classmethod
    def next_gen(cls, matrix:np.array):
        m = copy.deepcopy(matrix)
        for i, row in enumerate(matrix):
            for j, n in enumerate(row):
                neighs = cls.get_cell_neighbors(matrix, i, j)
                state = cls.__get_cell_state(n, neighs)
                m[i, j] = state
        return m
    
    
    def mnext_gen(self):
        m = copy.deepcopy(self.matrix)
        for i, row in enumerate(self.matrix):
            for j, n in enumerate(row):
                neighs = self.mget_cell_neighbors(i, j)
                state = Matrix.__get_cell_state(n, neighs)
                m[i, j] = state
        self.matrix = copy.deepcopy(m)
        return m
    
    @classmethod
    def get_indexes(cls, rows, cols):
        indexes = []
        for i in range(rows):
            indexes.extend(list(zip([i]*cols, range(cols))))
        return indexes
    
    
    @classmethod
    def random(cls, matrix:np.array, count=1):
        h, w = matrix.shape[:2]
        if count >= h * w:
            raise Exception('параметр count не должен превышать размер массива')
        indexes = cls.get_indexes(h, w)
        for i in range(count):
            n = randint(0, len(indexes)-1)
            y, x = indexes.pop(n)
            matrix[y,x] = 1
    
    
    def mrandom(self, count=1):
        h, w = self.matrix.shape[:2]
        if count >= h * w:
            raise Exception('параметр count не должен превышать размер массива')
        indexes = Matrix.get_indexes(h, w)
        for i in range(count):
            n = randint(0, len(indexes)-1)
            y, x = indexes.pop(n)
            self.matrix[y,x] = 1
    






if __name__ == "__main__":
    ...
    lst = [
        [1,1,0,0],
        [1,0,0,0],
        [0,0,0,0],
        [0,0,0,0],
    ]
    
    
    mat = Matrix.create_matrix(5, 5)
    print(mat)
    print()
    
    Matrix.random(mat, 10)
    print(mat)
    print(np.sum(mat==1))
    
    
    mat = Matrix()
    mat.mcreate_matrix(5, 5)
    print(mat)
    print()
    mat.mrandom(10)
    print(mat)
    print(np.sum(mat.mat==1))
    
    
    
    
    
    
    
    
    
    
    
