import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            # Рисуем вертикальные линии через каждые `cell_size` пикселей
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
            # Рисуем горизонтальные линии через каждые `cell_size` пикселей
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            # Обработка событий Pygame, таких как закрытие окна
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        # Создаем матрицу клеток, где значение каждой клетки случайно определяется (если randomize=True)
        cells = [
            [random.randint(0, int(randomize)) for _ in range(self.cell_width)]
            for _ in range(self.cell_height)
        ]
        return cells

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i, row in enumerate(self.grid):
            for j, col in enumerate(row):
                # Если клетка живая (1), рисуем зеленый квадрат, иначе белый (мертвая клетка)
                color = "green" if self.grid[i][j] == 1 else "white"
                coords = (
                    j * self.cell_size + 1,
                    i * self.cell_size + 1,
                    self.cell_size - 1,
                    self.cell_size - 1,
                )
                pygame.draw.rect(self.screen, color, coords)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbours = []
        row, col = cell
        neighbor_offsets = [
            (-1, -1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (1, 0),
            (0, 1),
            (-1, 1),
            (1, -1),
        ]

        for row_offset, col_offset in neighbor_offsets:
            new_row, new_col = row + row_offset, col + col_offset
            # Проверка, что новые координаты находятся в пределах игрового поля.
            if (
                new_row < 0
                or new_row >= self.cell_height
                or new_col < 0
                or new_col >= self.cell_width
            ):
                continue
            neighbours.append(
                self.grid[new_row][new_col]
            )  # Добавляем состояние клетки в список соседей.

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        # Создаем новое поколение клеток с теми же размерами, заполненное нулями
        next_generation = [
            [0 for _ in range(self.cell_width)] for _ in range(self.cell_height)
        ]
        for i, row in enumerate(self.grid):
            for j, _ in enumerate(row):
                # Определяем количество живых соседей
                neighbours = sum(self.get_neighbours((i, j)))

                # Правила игры для перехода в следующее поколение:
                if 2 <= neighbours <= 3:
                    if neighbours == 3 and self.grid[i][j] == 0:
                        next_generation[i][j] = 1  # Клетка рождается, если у нее ровно 3 соседа
                        continue
                    next_generation[i][j] = self.grid[i][j]  # Клетка остается в прежнем состоянии
                    continue
                next_generation[i][j] = 0  # Клетка умирает, если не выполняется условие для выживания

        return next_generation
