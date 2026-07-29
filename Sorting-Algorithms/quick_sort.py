"""
quick_sort.py

QUICK SORT
----------
Idea: another "divide and conquer" algorithm, but instead of splitting
the list evenly in half like merge sort, it picks a "pivot" element and
PARTITIONS the list around it: everything smaller than the pivot goes to
its left, everything bigger goes to its right. The pivot is now in its
final sorted position. Recursively repeat on the left and right chunks.

Time complexity:
    Average case : O(n log n) -- typically the fastest in-place sort in
                    practice, due to good cache locality
    Worst case   : O(n^2)     -- happens if the pivot is consistently the
                    smallest/largest element (e.g. an already-sorted list
                    with a naive "always pick the first element" pivot)
Space complexity:
    O(log n) -- from the recursion stack (no extra array needed for the
    partitioning itself, unlike merge sort)

This implementation picks a RANDOM pivot each time specifically to avoid
the O(n^2) worst case on already-sorted or reverse-sorted input, which is
a very common real-world input pattern (and a classic gotcha if you pick
a fixed pivot like "always the first element").
"""

import random
from typing import List


def quick_sort(arr: List[int]) -> List[int]:
    """Sorts `arr` in ascending order, in place, and also returns it."""
    _quick_sort(arr, 0, len(arr) - 1)
    return arr


def _quick_sort(arr: List[int], low: int, high: int) -> None:
    if low < high:
        # Partition the sub-array arr[low..high] and get the pivot's
        # final resting index.
        pivot_index = _partition(arr, low, high)

        # Recursively sort the elements before and after the pivot.
        # The pivot itself is already in its correct final position,
        # so it's excluded from both recursive calls.
        _quick_sort(arr, low, pivot_index - 1)
        _quick_sort(arr, pivot_index + 1, high)


def _partition(arr: List[int], low: int, high: int) -> int:
    """
    Lomuto partition scheme, with a randomly chosen pivot (swapped to the
    end first) to avoid worst-case behavior on already-sorted input.

    Rearranges arr[low..high] so that everything <= pivot comes before it
    and everything > pivot comes after it, then returns the pivot's final
    index.
    """
    # Pick a random pivot and move it to the end -- this is the one line
    # that protects us from the classic O(n^2) sorted-input worst case.
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]
    pivot = arr[high]

    # `i` tracks the boundary of "elements confirmed <= pivot so far".
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Finally, place the pivot right after the last element that's <= it.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", quick_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", quick_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", quick_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", quick_sort(reverse_sorted))
