import pygame as pg
import pygame_widgets as pgw
from pygame_widgets.slider import Slider
from pygame_widgets.button import Button
from pygame_widgets.textbox import TextBox
from pygame_widgets.selection import Checkbox

from rich import print, inspect



class SettingSurface:
    
    def __init__(self, width, height, pos_x, pos_y, bgcolor=None):
        self.width = width
        self.height = height
        self.size = width, height
        self.x = pos_x
        self.y = pos_y
        self.pos = pos_x, pos_y
        if not bgcolor:
            self.bgcolor = (30, 30, 50)
            self.original = pg.Surface(self.size)
            self.original.fill(self.bgcolor)
        
        self.surface = self.original.copy()
        self.random_choice = False
        self.controls()
    
    
    def controls(self):
        # виджеты настроек
        btn_width = self.width // 5
        x1, y1 = self.width-5-btn_width*2-5, self.height * .97 - 30
        x2, y2 = self.width-5-btn_width, self.height * .97 - 30
        self.start_btn = Button(self.surface, x1, y1, btn_width, 30, text='start', radius=3)
        self.stop_btn = Button(self.surface, x2, y2, btn_width, 30, text='stop', radius=3)
        
        width_input_size = self.width * 0.2
        height_input_size = 30
        
        space_hor = int(self.width * 0.02)
        space_vert = int(self.height * 0.02)
        
        x, y = space_hor, space_vert
        self.input_columns = TextBox(self.surface, x, y, width_input_size, height_input_size, placeholderText='столб')
        x = self.input_columns.getX() + self.input_columns.getWidth() + space_hor
        self.input_rows = TextBox(self.surface, x, y, width_input_size, height_input_size, placeholderText='строк')
        x = self.input_rows.getX() + self.input_rows.getWidth() + space_hor * 2
        self.create_btn = Button(self.surface, x, y, btn_width, 30, text='создать', radius=3)
        
        x = space_hor
        y = self.create_btn.getHeight() + self.create_btn.getY() + space_vert
        width = self.width * 0.75
        self.random_or_manual = Checkbox(self.surface, x, y, width, 50,
                                       ('добавить случ клетки',), boxColour=(255, 20,20), 
                                       colour=self.bgcolor, textColour=(200, 200, 200))
    
    
    def is_random_choice(self):
        # прверка установле ли чекбокс
        selected = self.random_or_manual.getSelected()
        return len(selected) > 0
    
    
    def get_matrix_size(self):
        # получение размеров матрицы из полей ввода input_rows и input_columns
        if self.input_columns.isEnabled() and self.input_rows.isEnabled():
            width, height = 10, 10
            try:
                width = int(self.input_columns.getText())
                width = 100 if width > 100 else width
            except: pass
            try:
                height = int(self.input_rows.getText())
                height = 100 if height > 100 else height
            except: pass
            return width, height
        return 10, 10
    
    
    def draw(self, surface):
        
        surface.blit(self.surface, self.pos)
    
    









if __name__ == "__main__":
    ...







