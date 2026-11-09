import unittest
from typing import Sequence, Union

import numpy as np


def create_even_mask(array: Union[np.ndarray, Sequence[int]]) -> bool:
    """
    Создает булеву маску для четных чисел в массиве.

    """
    return np.asarray(array) % 2 == 0


def longest_even_sequence(array: Union[np.ndarray, Sequence[int]]) -> int:
    """
    Находит длину самой длинной последовательности чётных чисел в массиве.
    """
    # Преобразуем входной массив в numpy array
    array = np.asarray(array)

    # Если массив пустой, то возвращаем 0.
    if array.size == 0:
        return 0

    # Создаем булеву маску, где True означает, что число в массиве чётное, иначе False.
    even_mask = create_even_mask(array)

    # Если в массиве нет ни одного чётного числа, возвращаем 0.
    if not np.any(even_mask):
        return 0

    # Находим индексы, где меняется последовательность чётности (с True на False или наоборот).
    # Для этого вычисляем разницу между соседними элементами маски (приведя её к int) и находим
    # индексы, где эта разница не равна 0
    diff_indices = np.where(np.diff(even_mask.astype(int)))[0] + 1

    # Добавляем индексы начала (0) и конца массива, чтобы учесть все последовательности.
    all_indices = np.concatenate(([0], diff_indices, [len(array)]))

    # Вычисляем длины всех последовательностей (и чётных, и нечётных).
    sequence_lengths = np.diff(all_indices)

    # Выбираем только длины последовательностей, которые начинаются с чётного числа.
    even_sequence_lengths = sequence_lengths[even_mask[all_indices[:-1]]]

    # Если есть хотя бы одна последовательность чётных чисел, возвращаем длину самой длинной, иначе 0.
    if len(even_sequence_lengths) > 0:
        return np.max(even_sequence_lengths)
    else:
        return 0


if __name__ == "__main__":
    input_str = input("Введите числа через пробел: ")
    # Преобразуем введенную строку в список целых чисел.
    input_list = [int(x) for x in input_str.split()]
    # Создаем NumPy массив из списка.
    input_arr = np.array(input_list, dtype=int)
    # Вызываем функцию для вычисления самой длинной последовательности чётных чисел.
    result = longest_even_sequence(input_arr)
    # Выводим результат.
    print(f"Самая длинная последовательность четных чисел в введенном массиве: {result}")
