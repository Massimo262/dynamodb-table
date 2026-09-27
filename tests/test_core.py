import math
import unittest

from sparse_table import SparseTable


class TestSparseTableMin(unittest.TestCase):
    def test_min_basic(self):
        t = SparseTable([5, 2, 4, 1, 3], min)
        self.assertEqual(t.query(0, 4), 1)
        self.assertEqual(t.query(0, 1), 2)
        self.assertEqual(t.query(3, 4), 1)
        self.assertEqual(t.query(2, 2), 4)

    def test_min_whole_range_power_of_two(self):
        t = SparseTable([7, 3, 9, 1, 8, 2, 6, 4], min)
        self.assertEqual(t.query(0, 7), 1)

    def test_min_whole_range_non_power_of_two(self):
        t = SparseTable([7, 3, 9, 1, 8, 2, 6], min)
        self.assertEqual(t.query(0, 6), 1)

    def test_min_single_element(self):
        t = SparseTable([42], min)
        self.assertEqual(t.query(0, 0), 42)

    def test_min_two_elements(self):
        t = SparseTable([3, 1], min)
        self.assertEqual(t.query(0, 1), 1)
        self.assertEqual(t.query(0, 0), 3)
        self.assertEqual(t.query(1, 1), 1)

    def test_min_all_equal(self):
        t = SparseTable([5, 5, 5, 5], min)
        self.assertEqual(t.query(1, 3), 5)

    def test_min_descending(self):
        t = SparseTable([9, 8, 7, 6, 5, 4, 3, 2, 1], min)
        self.assertEqual(t.query(0, 8), 1)
        self.assertEqual(t.query(0, 3), 6)
        self.assertEqual(t.query(5, 8), 1)

    def test_min_ascending(self):
        t = SparseTable([1, 2, 3, 4, 5, 6, 7, 8, 9], min)
        self.assertEqual(t.query(0, 8), 1)
        self.assertEqual(t.query(4, 7), 5)


class TestSparseTableMax(unittest.TestCase):
    def test_max_basic(self):
        t = SparseTable([5, 2, 8, 1, 3], max)
        self.assertEqual(t.query(0, 4), 8)
        self.assertEqual(t.query(1, 2), 8)
        self.assertEqual(t.query(3, 4), 3)

    def test_max_single(self):
        t = SparseTable([7], max)
        self.assertEqual(t.query(0, 0), 7)


class TestSparseTableGCD(unittest.TestCase):
    def test_gcd_basic(self):
        t = SparseTable([12, 18, 24, 9, 15], math.gcd)
        self.assertEqual(t.query(0, 2), 6)
        self.assertEqual(t.query(0, 4), 3)
        self.assertEqual(t.query(0, 0), 12)

    def test_gcd_all_multiples(self):
        t = SparseTable([6, 12, 18, 24], math.gcd)
        self.assertEqual(t.query(0, 3), 6)


class TestSparseTableBitwiseAnd(unittest.TestCase):
    def test_and_basic(self):
        t = SparseTable([0b1110, 0b1011, 0b1101, 0b0111], lambda a, b: a & b)
        self.assertEqual(t.query(0, 3), 0b0000)
        self.assertEqual(t.query(0, 1), 0b1010)


class TestSparseTableEdgeCases(unittest.TestCase):
    def test_empty_table_raises(self):
        t = SparseTable([], min)
        self.assertEqual(len(t), 0)
        with self.assertRaises(IndexError):
            t.query(0, 0)

    def test_out_of_bounds_left(self):
        t = SparseTable([1, 2, 3], min)
        with self.assertRaises(IndexError):
            t.query(-1, 2)

    def test_out_of_bounds_right(self):
        t = SparseTable([1, 2, 3], min)
        with self.assertRaises(IndexError):
            t.query(0, 3)

    def test_left_greater_than_right(self):
        t = SparseTable([1, 2, 3], min)
        with self.assertRaises(IndexError):
            t.query(2, 1)

    def test_input_not_mutated(self):
        src = [5, 3, 8, 1]
        t = SparseTable(src, min)
        src[0] = 100
        # Table took a defensive copy; mutating the source must not affect it.
        self.assertEqual(t.query(0, 3), 1)

    def test_len(self):
        t = SparseTable([1, 2, 3, 4, 5], min)
        self.assertEqual(len(t), 5)

    def test_repr(self):
        t = SparseTable([1, 2, 3], min)
        self.assertIn("3", repr(t))

    def test_large_range_various_lengths(self):
        # Exercise every power-of-two boundary up to 64.
        data = list(range(1, 65))
        t = SparseTable(data, min)
        for start in range(0, 64, 7):
            for end in range(start, 64):
                self.assertEqual(t.query(start, end), data[start])


class TestSparseTableStrings(unittest.TestCase):
    def test_max_string_by_lex(self):
        words = ["apple", "banana", "cherry", "date"]
        t = SparseTable(words, max)
        self.assertEqual(t.query(0, 3), "date")
        self.assertEqual(t.query(0, 1), "banana")


if __name__ == "__main__":
    unittest.main()
