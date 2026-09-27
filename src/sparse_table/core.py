"""Sparse Table for idempotent range queries.

A sparse table preprocesses an array in O(n log n) time and then answers
idempotent range queries (min, max, gcd, bitwise-and/or) in O(1). The
operation must be idempotent — f(x, x) == x — because the query overlaps
two intervals of equal length rather than splitting the range cleanly.
Non-idempotent operations like sum or product give wrong answers here;
use a prefix-sum array or segment tree for those.

The table stores 2^k-length block answers for every starting position.
A range query [l, r] is answered by taking the larger of two precomputed
blocks that together cover [l, r] with overlap. The overlap is harmless
precisely because the operation is idempotent.
"""

from __future__ import annotations

from typing import Callable, List, Sequence, TypeVar

T = TypeVar("T")


class SparseTable:
    """Preprocesses a sequence for O(1) idempotent range queries.

    Parameters
    ----------
    data:
        The sequence to query. A defensive copy is taken so later mutation
        of the input has no effect on the table.
    op:
        An associative, idempotent binary operation. Idempotence
        (f(x, x) == x) is required for correctness; associativity is
        required so that overlapping blocks compose consistently.

    Notes
    -----
    Empty input is supported: ``query`` on an empty table raises
    ``IndexError`` before doing anything else, and ``len(table)`` is 0.
    Single-element ranges are handled by the level-0 row directly.
    """

    __slots__ = ("_data", "_op", "_table", "_log")

    def __init__(self, data: Sequence[T], op: Callable[[T, T], T]) -> None:
        self._data: List[T] = list(data)
        self._op = op
        n = len(self._data)

        if n == 0:
            self._log: List[int] = [0]
            self._table: List[List[T]] = []
            return

        # Precompute floor(log2(i)) for every index up to n so that query
        # time is a pure array lookup with no function calls.
        self._log = [0] * (n + 1)
        for i in range(2, n + 1):
            self._log[i] = self._log[i // 2] + 1

        k = self._log[n] + 1
        # table[k][i] = op over data[i : i + 2**k]
        self._table = [self._data]
        for level in range(1, k):
            prev = self._table[level - 1]
            step = 1 << (level - 1)
            # The last valid start for a block of length 2**level.
            last = n - (1 << level) + 1
            row = [self._op(prev[i], prev[i + step]) for i in range(last)]
            self._table.append(row)

    def query(self, left: int, right: int) -> T:
        """Return ``op`` applied over ``data[left : right + 1]`` (inclusive).

        Raises
        ------
        IndexError
            If the table is empty or ``left``/``right`` are out of range,
            or if ``left > right``.
        """
        n = len(self._data)
        if n == 0:
            raise IndexError("query on empty sparse table")
        if left < 0 or right >= n or left > right:
            raise IndexError(f"range [{left}, {right}] out of bounds for length {n}")

        length = right - left + 1
        k = self._log[length]
        row = self._table[k]
        a = row[left]
        b = row[right - (1 << k) + 1]
        # The two blocks overlap; idempotence makes the overlap harmless.
        return self._op(a, b)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"SparseTable(len={len(self._data)})"
