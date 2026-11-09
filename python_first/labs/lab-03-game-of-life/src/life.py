import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создает сетку (двумерный список) с указанными размерами.
        Если randomize=True, то клетки заполняются случайно (0 или 1).
        """
        grid = [
            [random.randint(0, int(randomize)) for _ in range(self.cols)] for _ in range(self.rows)
        ]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Возвращает список значений соседей клетки.
        Рассматриваются 8 соседних клеток, если они находятся в пределах поля.
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
            # Проверка, что соседняя клетка не выходит за границы поля
            if new_row < 0 or new_row >= self.rows or new_col < 0 or new_col >= self.cols:
                continue
            neighbours.append(self.curr_generation[new_row][new_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Вычисляет следующее поколение клеток по правилам игры.
        """
        next_generation = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        for i, row in enumerate(self.curr_generation):
            for j, _ in enumerate(row):
                # Подсчёт количества живых соседей
                neighbours = sum(self.get_neighbours((i, j)))

                # Правила игры: клетка остаётся живой, если у неё 2 или 3 живых соседа
                if 2 <= neighbours <= 3:
                    # Если у клетки ровно 3 соседа, она становится живой
                    if neighbours == 3 and self.curr_generation[i][j] == 0:
                        next_generation[i][j] = 1
                        continue
                    # Иначе клетка сохраняет своё текущее состояние
                    next_generation[i][j] = self.curr_generation[i][j]
                    continue

                # В остальных случаях клетка умирает
                next_generation[i][j] = 0

            return next_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        # Сохраняем текущее поколение как предыдущее
        self.prev_generation = self.curr_generation.copy()
        # Вычисляем следующее поколение
        self.curr_generation = self.get_next_generation()
        # Увеличиваем счетчик поколений
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False
        else:
            return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not self.prev_generation == self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            # Преобразуем строки файла в двумерный список целых чисел
            grid = [list(map(int, row.strip("\n").split())) for row in f.readlines()]
        # Создаем объект GameOfLife с загруженной сеткой
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            # Преобразуем каждую строку сетки в строку чисел и записываем в файл
            for row in self.curr_generation:
                f.write(" ".join(map(str, row)) + "\n")
