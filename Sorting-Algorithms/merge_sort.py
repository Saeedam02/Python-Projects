"""
merge_sort.py

MERGE SORT
----------
Idea: a classic "divide and conquer" algorithm.
  1. DIVIDE the list in half, recursively, until you're left with pieces
     of size 0 or 1 (which are trivially already sorted).
  2. CONQUER by merging pairs of sorted pieces back together, always
     picking the smaller of the two "front" elements first, until the
     whole list is one fully sorted piece again.

Time complexity:
    Worst/average/best case : O(n log n)  -- this is guaranteed, no matter
    how the input is arranged (unlike quicksort's unlucky-pivot worst case)
Space complexity:
    O(n) -- needs a temporary array to merge into; this is the trade-off
    for its guaranteed speed and stability

Merge sort is STABLE: two equal elements keep their original relative
order. That matters when you're sorting by one key but want ties broken
by "whichever came first" (e.g. sorting orders by price, keeping same-price
orders in their original arrival order).
"""

from typing import List
import random

def merge_sort(arr: List[int]) -> List[int]:
    """Returns a NEW sorted list (unlike the in-place sorts, merge sort
    naturally builds fresh merged lists at every step)."""

    # Base case: a list of 0 or 1 elements is already sorted.
    if len(arr) <= 1:
        return arr

    # --- DIVIDE ---
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    # --- CONQUER (merge the two now-sorted halves) ---
    return _merge(left_half, right_half)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Merges two already-sorted lists into one sorted list."""
    merged = []
    i = j = 0  # pointers into left and right respectively

    # Repeatedly take the smaller of the two "front" elements.
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:   # "<=" (not "<") keeps it stable
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # One side may still have leftover elements once the other runs out --
    # they're already sorted, so just tack them on at the end.
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", merge_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", merge_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", merge_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", merge_sort(reverse_sorted))
