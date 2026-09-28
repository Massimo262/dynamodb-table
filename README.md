# sparse_table

Preprocesses a sequence for O(1) idempotent range queries (min, max, gcd, bitwise-and/or) using a sparse table.

## Usage

```python
from sparse_table import SparseTable

t = SparseTable([5, 2, 8, 1, 3, 9, 4], min)
print(t.query(0, 6))   # 1
print(t.query(2, 4))   # 1
print(len(t))          # 7
```

## Why

A sparse table trades O(n log n) preprocessing time and O(n log n) memory for O(1) per query. The catch: the operation must be **idempotent** — `f(x, x) == x`. Min, max, gcd, and bitwise-and/or qualify; sum, product, and XOR do not. For non-idempotent operations use a prefix-sum array or a segment tree instead.

The table stores precomputed answers for every block of length 2^k. A range query is answered by overlapping two such blocks that together cover the range; the overlap is harmless precisely because the operation is idempotent.

## Edge cases

- Empty input is accepted; calling `query` on an empty table raises `IndexError`.
- `query(left, right)` is inclusive on both ends. `left > right` raises `IndexError`.
- The constructor takes a defensive copy of the input, so mutating the original sequence afterward has no effect.

## Exported names

- `SparseTable(data, op)` — constructor. `data` is any sequence; `op` is an associative, idempotent binary callable.
- `SparseTable.query(left, right)` — inclusive range query, returns the result of `op` over `data[left..right]`.
- `SparseTable.__len__` — returns the length of the original sequence.
