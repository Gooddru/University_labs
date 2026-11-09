import pathlib
import random  # Подключил для создания судоку
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    group_size = len(values) // n
    groups = []
    for group_index in range(n):
        start = group_size * group_index
        groups.append(values[start : start + group_size])
    return groups
    pass


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]  # Возвращаем все значения строки
    pass


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    col = []
    for i in range(
        0, len(grid)
    ):  # Проходимся по всем элементам и добавляем в список все значения из столбца
        col.append(grid[i][pos[1]])
    return col  # Возвращаем список значений столбцов
    pass


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    # Определяем начальные координаты
    block_row = (pos[0] // 3) * 3
    block_col = (pos[1] // 3) * 3
    block = []
    for row_offset in range(3):
        for col_offset in range(3):
            block.append(grid[block_row + row_offset][block_col + col_offset])
    return block
    pass


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    # Проходим по всем столбцам и строчкам
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":  # Если точка, то есть пустая клетка
                return i, j  # Возвращаем индексы этой клетки
    return None  # Возвращаем None, если не найдено пустых клеток
    pass


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    values = set(str(i) for i in range(1, 10))
    values = values - set(get_row(grid, pos))
    values = values - set(get_col(grid, pos))
    values = values - set(get_block(grid, pos))
    return values
    pass


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    # Ищем первую пустую клетку
    empty_positions = find_empty_positions(grid)
    # Если нет пустых клеток, возвращаем текущее решение
    if not empty_positions:
        return grid
    else:
        row, col = empty_positions  # Иначе продолжаем с первой найденной пустой клеткой
    # Проходим каждое значение от 1 до 9 на этой позиции
    for i in range(1, 10):
        if str(i) in find_possible_values(
            grid, (row, col)
        ):  # Для проверки можно ли его поставить и будет ли это решением
            grid[row][col] = str(i)  # Устанавливаем их на позицию
            if solve(grid):  # Рекурсивно продолжаем решать оставшуюся часть пазла
                return grid  # Если решение найдено, возвращаем его
            # Если решение не найдено, оставляем клетку такой же(пустой)
            grid[row][col] = "."
    # Если для данной конфигурации не найдено решение, возвращаем None
    return None
    pass


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles

    # Проверка на пустое решение
    if not solution:
        return False

    # Набор для проверки судоку, т.к. 9х9, то от 1 до 9
    valid_set = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

    # Проверка всех строк, столбцов и блоков
    for i in range(9):
        # Проверка строки
        if set(solution[i]) != valid_set:
            return False
        # Проверка столбца
        if set(get_col(solution, (0, i))) != valid_set:
            return False
        # Проверка блока
        if set(get_block(solution, (i // 3 * 3, i % 3 * 3))) != valid_set:
            return False

    return True
    pass


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    # Генерируем полный решённый судоку
    grid = [["." for _ in range(9)] for _ in range(9)]
    solve(grid)  # Заполняем сетку решением судоку

    # Преобразуем решённый судоку в частично заполненный
    all_positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(all_positions)  # Перемешиваем все позиции

    # Количество ячеек, которые нужно очистить
    num_to_remove = 81 - N

    # Убираем числа, заменяя их точками '.', делая клетку пустой
    for i in range(num_to_remove):
        row, col = all_positions[i]
        grid[row][col] = "."
    # Возвращаем  судоку
    return grid
    pass


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
