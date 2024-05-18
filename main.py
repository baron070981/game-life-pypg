import pygame as pg
import pygame_widgets
import numpy as np
import random
from pathlib import Path


from playspace import PlaySpace, Flags
from settingsspace import SettingSpace
from matrixes import Matrix


pg.init()
FPS = 60

SRC = Path(__file__).parent / 'src'

# размер окна
WIN_WIDTH = 1200
WIN_HEIGHT = 700
# главное окно
screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pg.DOUBLEBUF)
screen.fill("purple")

WIN_WIDTH, WIN_HEIGHT = screen.get_width(), screen.get_height()
clock = pg.time.Clock()
running = True # приложение запущено
PLAY_RUN = False # запущена или остановлена игра
GET_SETT = False # 
CREATE = False # создана ли матрица

# размер и позиция прстранства установок и настроек
SETT_SPACE_SIZE = WIN_WIDTH // 3, WIN_HEIGHT-10
SETT_SPACE_POS = 5, 5
SETT_W, SETT_H = SETT_SPACE_SIZE

# размер и позиция игрового поля
PLAY_SPACE_SIZE = (WIN_WIDTH - 15 - SETT_W, WIN_HEIGHT-10)
PLAY_SPACE_POS = (SETT_W + 10, 5)
W, H = PLAY_SPACE_SIZE

ROW, COLS = 10, 10


count_step = 0
matrix = Matrix()


def start_game():
    # запуск игрового процесса
    Flags.PLAY_RUN = True


def stop_game():
    # остановка игрового процесса
    Flags.PLAY_RUN = False


def create_matrix(matrix: Matrix, cols, rows):
    if not Flags.CREATE and not Flags.GET_SETT:
        matrix.mcreate_matrix(cols, rows)
        Flags.CREATE = True
        Flags.GET_SETT = True
    




if __name__ == "__main__":
    ...
    
    bg_image = pg.image.load(SRC / 'background.jpg')
    
    # игровое поле
    play_space = PlaySpace(W, H, PLAY_SPACE_POS[0], PLAY_SPACE_POS[1], background=bg_image)
    
    # поле настройки и установок
    sett_space = SettingSpace(SETT_W, SETT_H, SETT_SPACE_POS[0], SETT_SPACE_POS[1])
    sett_space.start_btn.setOnClick(start_game)
    sett_space.stop_btn.setOnClick(stop_game)
    sett_space.create_btn.setOnClick(onClick=create_matrix)
    
    sett_space.start_btn.disable() # отключение кнопки запуска
    
    while running:
        count_step += 1
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
        screen.fill("purple")
        if not running:
            break
    # =================================
        
        pygame_widgets.update(events)
        
        # если игровой процесс не запущен
        if not Flags.PLAY_RUN:
            
            sett_space.create_btn.enable()
            sett_space.random_or_manual.enable()
            sett_space.input_rows.enable()
            sett_space.input_columns.enable()
            sett_space.stop_btn.disable()
            
            # получение размеров игрового поля (матрицы) из полей ввода
            COLS, ROW = sett_space.get_matrix_size()
            # передача полученных размеров в функцию onClick кнопки create_btn
            sett_space.create_btn.onClickParams = matrix, COLS, ROW
            # если разрешено создавать матрицу и получать ее размеры
            if Flags.CREATE and Flags.GET_SETT:
                # если установлен чекбокс в созданной матрице добавляются "живые клетки"
                if sett_space.is_random_choice():
                    s = matrix.mat.shape[0] * matrix.mat.shape[1] // 3
                    matrix.mrandom(s)
                play_space.set_matrix(matrix.mat)
                play_space.create_surface_matrix()
                Flags.CREATE = False
                Flags.GET_SETT = False
                sett_space.start_btn.enable()
        
        # если игровой процесс запущен
        elif Flags.PLAY_RUN:
            # отключаются все виджеты кроме stop_btn,который включается
            sett_space.create_btn.disable()
            sett_space.random_or_manual.disable()
            sett_space.input_rows.disable()
            sett_space.input_columns.disable()
            sett_space.start_btn.disable()
            sett_space.stop_btn.enable()
            
            # в игровое поле передается матрица из 1 и 0
            play_space.set_matrix(matrix.mat)
            # расчитывается следующее поколение
            matrix.mnext_gen()
        
        
        
        play_space.draw(screen)
        sett_space.draw(screen)
        # изминение состояния клетки по нажатию левой кнопки мыши
        # 1 становится 0 и наоборот
        coords = play_space.listen(events)
        if coords:
            matrix.mreplace_value(coords[0], coords[1])
        
    # =================================
        pg.display.flip()
        pg.time.wait(100)
        clock.tick(FPS)

    pg.quit()







