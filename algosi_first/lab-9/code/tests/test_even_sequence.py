import unittest

import numpy as np

from solutions.even_sequence import longest_even_sequence


class TestLongestEvenSequence(unittest.TestCase):
    def test_empty_array(self):
        # Тест с пустым массивом.
        self.assertEqual(longest_even_sequence(np.array([])), 0)

    def test_no_even_numbers(self):
        # Тест с массивом, не содержащим чётных чисел.
        self.assertEqual(longest_even_sequence(np.array([1, 3, 5, 7])), 0)

    def test_single_even_number(self):
        # Тест с массивом, содержащим только одно чётное число.
        self.assertEqual(longest_even_sequence(np.array([2])), 1)

    def test_single_odd_number(self):
        # Тест с массивом, содержащим только одно нечётное число.
        self.assertEqual(longest_even_sequence(np.array([1])), 0)

    def test_sequence_of_even_numbers(self):
        # Тест с массивом, содержащим последовательность чётных чисел.
        self.assertEqual(longest_even_sequence(np.array([2, 4, 6, 8, 10])), 5)

    def test_sequence_of_even_negative_numbers(self):
        # Тест с массивом, содержащим последовательность отрицательных чётных чисел.
        self.assertEqual(longest_even_sequence(np.array([-2, -4, -6, -8, -10])), 5)

    def test_mixed_even_and_odd(self):
        # Тест с массивом, содержащим смешанные чётные и нечётные числа.
        self.assertEqual(
            longest_even_sequence(np.array([1, 2, 4, 6, 1, 3, 8, 10, 12, 1, 2, 4, 1, 5])), 3
        )

    def test_even_at_start(self):
        # Тест с массивом, где чётные числа находятся в начале.
        self.assertEqual(longest_even_sequence(np.array([2, 4, 1, 3])), 2)

    def test_even_at_end(self):
        # Тест с массивом, где чётные числа находятся в конце.
        self.assertEqual(longest_even_sequence(np.array([1, 3, 2, 4])), 2)

    def test_multiple_even_sequences(
        self,
    ):  # Тест с массивом, где есть несколько последовательностей чётных чисел.
        self.assertEqual(longest_even_sequence(np.array([1, 2, 4, 1, 2, 1, 2, 4, 6])), 3)

    def test_equal_even_numbers(self):
        # Тест с массивом, где есть последовательность одинаковых чётных чисел.
        self.assertEqual(longest_even_sequence(np.array([2, 2, 1, 4, 4, 4])), 3)

    def test_only_even_sequence_with_single_odd(self):
        # Тест с массивом где есть одна последовательность четных и один нечетный элемент
        self.assertEqual(longest_even_sequence(np.array([2, 2, 1])), 2)

    def test_single_even_sequence_with_single_odd(self):
        # Тест с массивом где есть один четный элемент в последовательности, окруженной нечетными элементами
        self.assertEqual(longest_even_sequence(np.array([1, 2, 1])), 1)

    def test_odd_even_odd(self):
        # Тест с массивом вида [нечёт, чёт, нечёт].
        self.assertEqual(longest_even_sequence(np.array([1, 2, 1])), 1)

    def test_negative_odd_numbers(self):
        # Тест с массивом содержащим отрицательные нечетные числа.
        self.assertEqual(longest_even_sequence(np.array([-1, -3, -5, -7])), 0)

    def test_long_even_sequence(self):
        # Тест с длинной последовательностью из 10 чётных чисел.
        self.assertEqual(longest_even_sequence(np.array([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])), 10)

    def test_negative_long_even_sequence(self):
        # Тест с длинной последовательностью из 10 чётных отрицательных чисел.
        self.assertEqual(
            longest_even_sequence(
                np.array([-200, -180, -160, -140, -120, -80, -60, -40, -20, -10])
            ),
            10,
        )

    def test_large_positive_even(self):
        # Тест с большим массивом четных положительных чисел
        large_even_positive = np.arange(2, 2002, 2)
        self.assertEqual(longest_even_sequence(large_even_positive), 1000)

    def test_large_negative_even(self):
        # Тест с большим массивом четных отрицательных чисел
        large_even_negative = np.arange(-2, -2002, -2)
        self.assertEqual(longest_even_sequence(large_even_negative), 1000)

    def test_large_mixed(self):
        # Тест с большим массивом смешанных чисел (поочередно четное и нечетное)
        large_mixed = np.array([i if i % 2 == 0 else 1 for i in range(2000)])
        self.assertEqual(longest_even_sequence(large_mixed), 1)


if __name__ == "__main__":
    unittest.main()
