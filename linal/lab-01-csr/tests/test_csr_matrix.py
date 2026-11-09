import unittest
from src.csr_matrix import CSRMatrix


class TestCSRMatrix(unittest.TestCase):

    def test_from_dense(self):
        dense_matrix = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        self.assertEqual(csr_matrix.rows, 3)
        self.assertEqual(csr_matrix.cols, 3)
        self.assertEqual(csr_matrix.values, [1, 2, 3])
        self.assertEqual(csr_matrix.col_indices, [0, 1, 2])
        self.assertEqual(csr_matrix.row_pointers, [0, 1, 2, 3])

    def test_to_dense(self):
        csr_matrix = CSRMatrix(3, 3, [1, 2, 3], [0, 1, 2], [0, 1, 2, 3])
        dense_matrix = csr_matrix.to_dense()

        expected_dense = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        self.assertEqual(dense_matrix, expected_dense)

    def test_scalar_multiply(self):
        dense_matrix = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)
        scalar = 2
        result = csr_matrix.scalar_multiply(scalar)

        expected_values = [2, 4, 6]
        self.assertEqual(result.values, expected_values)

    def test_add(self):
        dense_matrix_1 = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        dense_matrix_2 = [
            [0, 1, 0],
            [0, 0, 2],
            [3, 0, 0]
        ]
        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.add(csr_matrix_2)

        expected_dense = [
            [1, 1, 0],
            [0, 2, 2],
            [3, 0, 3]
        ]
        self.assertEqual(result.to_dense(), expected_dense)

    def test_multiply(self):
        dense_matrix_1 = [
            [1, 2],
            [3, 4]
        ]
        dense_matrix_2 = [
            [5, 6],
            [7, 8]
        ]
        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.multiply(csr_matrix_2)

        expected_dense = [
            [19, 22],
            [43, 50]
        ]
        self.assertEqual(result.to_dense(), expected_dense)

    def test_determinant_and_inverse(self):
        dense_matrix = [
            [1, 2],
            [3, 4]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        det, inverse_exists = csr_matrix.determinant_and_inverse()

        self.assertEqual(det, -2)
        self.assertEqual(inverse_exists, "Да")

    def test_get_element(self):
        dense_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        element = csr_matrix.get_element(2, 3)
        self.assertEqual(element, 6)

        with self.assertRaises(IndexError):
            csr_matrix.get_element(4, 2)

    def test_single_element_matrix(self):
        csr_matrix = CSRMatrix(1, 1, [5], [0], [0, 1])
        dense_matrix = csr_matrix.to_dense()

        self.assertEqual(dense_matrix, [[5]])

    def test_non_square_matrix_multiply(self):
        dense_matrix_1 = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        dense_matrix_2 = [
            [7, 8],
            [9, 10]
        ]
        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.multiply(csr_matrix_2)

        expected_dense = [
            [25, 28],
            [57, 64],
            [89, 100]
        ]
        self.assertEqual(result.to_dense(), expected_dense)

    def test_add_different_sizes(self):
        dense_matrix_1 = [
            [1, 0],
            [0, 2]
        ]
        dense_matrix_2 = [
            [3, 4, 5],
            [6, 7, 8]
        ]

        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        with self.assertRaises(ValueError):
            csr_matrix_1.add(csr_matrix_2)

    def test_get_element_out_of_bounds(self):
        dense_matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        with self.assertRaises(IndexError):
            csr_matrix.get_element(0, 3)

        with self.assertRaises(IndexError):
            csr_matrix.get_element(4, 2)

    def test_trace(self):
        dense_matrix = [
            [1, 0, 0],
            [0, 2, 0],
            [0, 0, 3]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        trace_value = csr_matrix.trace()

        self.assertEqual(trace_value, 6)

    def test_trace_zero_matrix(self):
        dense_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        trace_value = csr_matrix.trace()

        self.assertEqual(trace_value, 0)

    def test_determinant_non_square(self):
        dense_matrix = [
            [1, 2],
            [3, 4],
            [5, 6]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        with self.assertRaises(ValueError):
            csr_matrix.determinant_and_inverse()

    def test_determinant_and_inverse_non_invertible(self):
        dense_matrix = [
            [1, 2],
            [2, 4]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        det, inverse_exists = csr_matrix.determinant_and_inverse()

        self.assertEqual(det, 0)
        self.assertEqual(inverse_exists, "Нет")

    def test_determinant_and_inverse_invertible(self):
        dense_matrix = [
            [4, 7],
            [2, 6]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        det, inverse_exists = csr_matrix.determinant_and_inverse()

        self.assertEqual(det, 10)
        self.assertEqual(inverse_exists, "Да")



    def test_zero_matrix_add(self):
        dense_matrix_1 = [
            [1, 2],
            [3, 4]
        ]
        zero_matrix = [
            [0, 0],
            [0, 0]
        ]
        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_zero_matrix = CSRMatrix.from_dense(zero_matrix)

        result = csr_matrix_1.add(csr_zero_matrix)

        self.assertEqual(result.to_dense(), dense_matrix_1)

    def test_zero_matrix_multiply(self):
        dense_matrix = [
            [1, 2],
            [3, 4]
        ]
        zero_matrix = [
            [0, 0],
            [0, 0]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)
        csr_zero_matrix = CSRMatrix.from_dense(zero_matrix)

        result = csr_matrix.multiply(csr_zero_matrix)

        expected_result = [
            [0, 0],
            [0, 0]
        ]
        self.assertEqual(result.to_dense(), expected_result)

    def test_zero_matrix_determinant(self):
        zero_matrix = [
            [0, 0],
            [0, 0]
        ]
        csr_matrix = CSRMatrix.from_dense(zero_matrix)

        det, inverse_exists = csr_matrix.determinant_and_inverse()

        self.assertEqual(det, 0)
        self.assertEqual(inverse_exists, "Нет")

    def test_from_dense_5x5(self):
        dense_matrix = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        self.assertEqual(csr_matrix.rows, 5)
        self.assertEqual(csr_matrix.cols, 5)
        self.assertEqual(csr_matrix.values, [1, 2, 3, 4, 5])
        self.assertEqual(csr_matrix.col_indices, [0, 1, 2, 3, 4])
        self.assertEqual(csr_matrix.row_pointers, [0, 1, 2, 3, 4, 5])

    def test_to_dense_5x5(self):
        csr_matrix = CSRMatrix(5, 5, [1, 2, 3, 4, 5], [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5])
        dense_matrix = csr_matrix.to_dense()

        expected_dense = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        self.assertEqual(dense_matrix, expected_dense)

    def test_add_5x5(self):
        dense_matrix_1 = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        dense_matrix_2 = [
            [0, 1, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 0, 3, 0],
            [0, 0, 0, 0, 4],
            [0, 0, 0, 0, 0]
        ]
        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.add(csr_matrix_2)

        expected_dense = [
            [1, 1, 0, 0, 0],
            [0, 2, 2, 0, 0],
            [0, 0, 3, 3, 0],
            [0, 0, 0, 4, 4],
            [0, 0, 0, 0, 5]
        ]
        self.assertEqual(result.to_dense(), expected_dense)

    def test_multiply_5x5(self):
        dense_matrix_1 = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        dense_matrix_2 = [
            [1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25]
        ]
        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.multiply(csr_matrix_2)

        expected_dense = [
            [1, 2, 3, 4, 5],
            [12, 14, 16, 18, 20],
            [33, 36, 39, 42, 45],
            [64, 68, 72, 76, 80],
            [105, 110, 115, 120, 125]
        ]
        self.assertEqual(result.to_dense(), expected_dense)

    def test_scalar_multiply_5x5(self):
        dense_matrix = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)
        scalar = 2
        result = csr_matrix.scalar_multiply(scalar)

        expected_values = [2, 4, 6, 8, 10]
        self.assertEqual(result.values, expected_values)

    def test_trace_5x5(self):
        dense_matrix = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        trace_value = csr_matrix.trace()

        self.assertEqual(trace_value, 15)

    def test_determinant_and_inverse_5x5(self):
        dense_matrix = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]
        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        det, inverse_exists = csr_matrix.determinant_and_inverse()

        self.assertEqual(det, 120)
        self.assertEqual(inverse_exists, "Да")

    def test_add_sparse_diag_matrices(self):
        dense_matrix_1 = [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ]

        dense_matrix_2 = [
            [0, 0, 0, 0, 6],
            [0, 0, 0, 7, 0],
            [0, 0, 0, 0, 8],
            [0, 0, 9, 0, 0],
            [10, 0, 0, 0, 0]
        ]

        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.add(csr_matrix_2)

        expected_dense = [
            [1, 0, 0, 0, 6],
            [0, 2, 0, 7, 0],
            [0, 0, 3, 0, 8],
            [0, 0, 9, 4, 0],
            [10, 0, 0, 0, 5]
        ]

        self.assertEqual(result.to_dense(), expected_dense)

    def test_multiply_sparse_matrices(self):
        dense_matrix_1 = [
            [1, 0, 0, 4, 0],
            [0, 2, 0, 0, 3],
            [0, 0, 3, 0, 0],
            [0, 4, 0, 0, 0],
            [5, 0, 0, 0, 0]
        ]

        dense_matrix_2 = [
            [0, 0, 1, 0, 0],
            [0, 0, 0, 2, 0],
            [3, 0, 0, 0, 0],
            [0, 4, 0, 0, 0],
            [0, 0, 5, 0, 0]
        ]

        csr_matrix_1 = CSRMatrix.from_dense(dense_matrix_1)
        csr_matrix_2 = CSRMatrix.from_dense(dense_matrix_2)

        result = csr_matrix_1.multiply(csr_matrix_2)

        expected_dense = [
            [0, 16, 1, 0, 0],
            [0, 0, 15, 4, 0],
            [9, 0, 0, 0, 0],
            [0, 0, 0, 8, 0],
            [0, 0, 5, 0, 0]
        ]

        self.assertEqual(result.to_dense(), expected_dense)

    def test_multiply_matrix_by_negative_scalar(self):
        dense_matrix = [
            [1, 0, 0, 4, 0],
            [0, 2, 0, 0, 3],
            [0, 0, 3, 0, 0],
            [0, 4, 0, 0, 0],
            [5, 0, 0, 0, 0]
        ]

        scalar = -2

        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        result = csr_matrix.scalar_multiply(scalar)

        expected_dense = [
            [-2, 0, 0, -8, 0],
            [0, -4, 0, 0, -6],
            [0, 0, -6, 0, 0],
            [0, -8, 0, 0, 0],
            [-10, 0, 0, 0, 0]
        ]

        self.assertEqual(result.to_dense(), expected_dense)

    def test_multiply_matrix_by_scalar(self):
        dense_matrix = [
            [1, 0, 0, 4, 0],
            [0, 2, 0, 0, 3],
            [0, 0, 3, 0, 0],
            [0, 4, 0, 0, 0],
            [5, 0, 0, 0, 0]
        ]

        scalar = 3

        csr_matrix = CSRMatrix.from_dense(dense_matrix)

        result = csr_matrix.scalar_multiply(scalar)

        expected_dense = [
            [3, 0, 0, 12, 0],
            [0, 6, 0, 0, 9],
            [0, 0, 9, 0, 0],
            [0, 12, 0, 0, 0],
            [15, 0, 0, 0, 0]
        ]

        self.assertEqual(result.to_dense(), expected_dense)


if __name__ == '__main__':
    unittest.main()
