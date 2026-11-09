class CSRMatrix:
    def __init__(self, rows, cols, values, col_indices, row_pointers):
        """
        Инициализация матрицы в формате CSR (Compressed Sparse Row).

        :param rows: Количество строк в матрице.
        :param cols: Количество столбцов в матрице.
        :param values: Список ненулевых значений матрицы.
        :param col_indices: Список индексов столбцов для каждого значения из values.
        :param row_pointers: Список указателей начала строк в values.
        """
        self.rows = rows
        self.cols = cols
        self.values = values
        self.col_indices = col_indices
        self.row_pointers = row_pointers

    @staticmethod
    def from_dense(dense_matrix_input):
        """
        Создание CSR-матрицы из плотной матрицы.

        :param dense_matrix_input: Вложенный список (двумерный массив), представляющий плотную матрицу.
        :return: Экземпляр CSRMatrix, соответствующий данной плотной матрице.
        """
        rows = len(dense_matrix_input)
        cols = len(dense_matrix_input[0]) if rows > 0 else 0
        values = []
        col_indices = []
        row_pointers = [0]

        for matrix_row in dense_matrix_input:
            for j, value in enumerate(matrix_row):
                if value != 0:
                    values.append(value)
                    col_indices.append(j)
            row_pointers.append(len(values))

        return CSRMatrix(rows, cols, values, col_indices, row_pointers)

    def to_dense(self):
        """
        Преобразование CSR-матрицы в плотное представление.

        :return: Вложенный список (двумерный массив), эквивалентный данной CSR-матрице.
        """
        dense_matrix_output = [[0] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            start = self.row_pointers[i]
            end = self.row_pointers[i + 1]
            for j in range(start, end):
                matrix_col = self.col_indices[j]
                dense_matrix_output[i][matrix_col] = self.values[j]

        return dense_matrix_output

    def trace(self):
        """
        Вычисление следа матрицы (суммы элементов на главной диагонали).

        :return: След матрицы.
        """
        trace_sum = 0
        for i in range(self.rows):
            start = self.row_pointers[i]
            end = self.row_pointers[i + 1]
            for j in range(start, end):
                if self.col_indices[j] == i:
                    trace_sum += self.values[j]
        return trace_sum

    def get_element(self, matrix_row, matrix_col):
        """
        Получение элемента матрицы по индексу строки и столбца (нумерация с 1).

        :param matrix_row: Номер строки (нумерация с 1).
        :param matrix_col: Номер столбца (нумерация с 1).
        :return: Значение элемента матрицы на заданной позиции.
        :raises IndexError: Если индексы выходят за границы матрицы.
        """
        if not (1 <= matrix_row <= self.rows and 1 <= matrix_col <= self.cols):
            raise IndexError("Индексы выходят за границы матрицы.")

        matrix_row -= 1
        matrix_col -= 1
        start = self.row_pointers[matrix_row]
        end = self.row_pointers[matrix_row + 1]
        for j in range(start, end):
            if self.col_indices[j] == matrix_col:
                return self.values[j]
        return 0

    def add(self, matrix):
        """
        Сложение двух матриц в формате CSR.

        :param matrix: Другая матрица в формате CSR.
        :return: Новая CSR-матрица, являющаяся результатом сложения.
        :raises ValueError: Если размеры матриц не совпадают.
        """
        if self.rows != matrix.rows or self.cols != matrix.cols:
            raise ValueError("Размеры матриц не совпадают.")

        dense_self = self.to_dense()
        dense_other_matrix = matrix.to_dense()
        result_dense = [
            [dense_self[i][j] + dense_other_matrix[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]

        return CSRMatrix.from_dense(result_dense)

    def scalar_multiply(self, number):
        """
        Умножение матрицы на скаляр.

        :param number: Скаляр, на который умножается матрица.
        :return: Новая CSR-матрица, являющаяся результатом умножения.
        """
        values = [value * number for value in self.values]
        return CSRMatrix(self.rows, self.cols, values, self.col_indices, self.row_pointers)

    def multiply(self, matrix):
        """
        Умножение двух матриц в формате CSR.

        :param matrix: Другая матрица в формате CSR.
        :return: Новая CSR-матрица, являющаяся результатом умножения.
        :raises ValueError: Если число столбцов первой матрицы не равно числу строк второй.
        """
        if self.cols != matrix.rows:
            raise ValueError("Число столбцов первой матрицы не равно числу строк второй.")

        result_values = []
        result_col_indices = []
        result_row_pointers = [0]

        for i in range(self.rows):
            start_a = self.row_pointers[i]
            end_a = self.row_pointers[i + 1]

            for j in range(matrix.cols):
                dot_product = 0
                for k in range(start_a, end_a):
                    col_idx_a = self.col_indices[k]
                    value_a = self.values[k]

                    for l in range(matrix.row_pointers[col_idx_a], matrix.row_pointers[col_idx_a + 1]):
                        if matrix.col_indices[l] == j:
                            dot_product += value_a * matrix.values[l]

                if dot_product != 0:
                    result_values.append(dot_product)
                    result_col_indices.append(j)

            result_row_pointers.append(len(result_values))

        return CSRMatrix(self.rows, matrix.cols, result_values, result_col_indices, result_row_pointers)

    def determinant_and_inverse(self):
        """
        Вычисление определителя и проверка существования обратной матрицы.

        :return: Кортеж (определитель, строка "Да" или "Нет" в зависимости от существования обратной матрицы).
        :raises ValueError: Если матрица не квадратная.
        """
        if self.rows != self.cols:
            raise ValueError("Матрица должна быть квадратной.")

        matrix = self.to_dense()
        determinant = self._determinant(matrix)
        has_inverse = determinant != 0

        return determinant, "Да" if has_inverse else "Нет"

    def _determinant(self, matrix):
        """
        Рекурсивное вычисление определителя.

        :param matrix: Вложенный список (двумерный массив), представляющий матрицу.
        :return: Определитель матрицы.
        """
        size = len(matrix)
        if size == 1:
            return matrix[0][0]
        if size == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

        determinant = 0
        for c in range(size):
            minor = [matrix_row[:c] + matrix_row[c + 1:] for matrix_row in matrix[1:]]
            determinant += ((-1) ** c) * matrix[0][c] * self._determinant(minor)
        return determinant


if __name__ == "__main__":
    print("Введите размеры первой матрицы (N и M):")
    rows1, cols1 = map(int, input().split())
    print("Введите элементы первой матрицы построчно:")
    dense_matrix_1 = [list(map(float, input().split())) for _ in range(rows1)]

    print("Введите размеры второй матрицы (N и M):")
    rows2, cols2 = map(int, input().split())
    print("Введите элементы второй матрицы построчно:")
    dense_matrix_2 = [list(map(float, input().split())) for _ in range(rows2)]

    csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
    print("Матрица 1 в CSR-формате:")
    print("Values:", csr_matrix_1.values)
    print("Column Indices:", csr_matrix_1.col_indices)
    print("Row Pointers:", csr_matrix_1.row_pointers)

    csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)
    print("Матрица 2 в CSR-формате:")
    print("Values:", csr_matrix_2.values)
    print("Column Indices:", csr_matrix_2.col_indices)
    print("Row Pointers:", csr_matrix_2.row_pointers)

    trace_value = csr_matrix_1.trace()
    print("След первой матрицы:", trace_value)

    print("Введите строку и столбец для получения элемента из первой матрицы (нумерация с 1):")
    row, col = map(int, input().split())
    element = csr_matrix_1.get_element(row, col)
    print(f"Элемент матрицы ({row}, {col}):", element)

    if rows1 == rows2 and cols1 == cols2:
        csr_sum = csr_matrix_1.add(csr_matrix_2)
        print("Сумма матриц:")
        for row in csr_sum.to_dense():
            print(row)
    else:
        print("Невозможно сложить матрицы разного размера.")

    print("Введите скаляр для умножения матрицы:")
    scalar = float(input())
    scalar_product = csr_matrix_1.scalar_multiply(scalar)
    print(f"Матрица после умножения на скаляр {scalar}:")
    for row in scalar_product.to_dense():
        print(row)

    if cols1 == rows2:
        csr_product = csr_matrix_1.multiply(csr_matrix_2)
        print("Произведение матриц:")
        for row in csr_product.to_dense():
            print(row)
    else:
        print("Невозможно умножить матрицы: число столбцов первой не равно числу строк второй.")

    print("Введите размер матрицы N:")
    N = int(input())

    print("Введите элементы матрицы построчно:")
    dense_matrix = [list(map(float, input().split())) for _ in range(N)]

    csr_matrix = CSRMatrix.from_dense(dense_matrix)

    det, inverse_exists = csr_matrix.determinant_and_inverse()
    print(f"Определитель матрицы: {det}")
    print(f"Матрица имеет обратную: {inverse_exists}")
