"""
cocktail_sort.py

COCKTAIL SHAKER SORT
--------------------
Idea: a bidirectional variation of bubble sort.

Bubble sort repeatedly moves the largest unsorted element toward the end of
the list. However, a small element near the end can move toward the beginning
only one position per pass.

Cocktail shaker sort improves this behavior by scanning in both directions:

  1. Scan from LEFT TO RIGHT, moving the largest unsorted element to the end.
  2. Scan from RIGHT TO LEFT, moving the smallest unsorted element to the
     beginning.
  3. Shrink the unsorted section from both ends.
  4. Repeat until no swaps are needed.

Example:
    [5, 2, 8, 1, 4]

Forward pass:
    [2, 5, 1, 4, 8]
                    ^
                    largest element reaches the end

Backward pass:
    [1, 2, 5, 4, 8]
     ^
     smallest element reaches the beginning

Time complexity:
    Worst case   : O(n²)
    Average case : O(n²)
    Best case    : O(n) when the list is already sorted, because the algorithm
                   stops after detecting that no swaps were made

Space complexity:
    O(1) -- the algorithm sorts the original list in place and only uses a
    few temporary variables

Cocktail shaker sort is STABLE because equal elements are not swapped.
Therefore, equal values keep their original relative order.

This implementation sorts the supplied list IN PLACE and also returns it for
convenience.
"""

from typing import List
import random


def cocktail_sort(arr: List[int]) -> List[int]:
    """Sorts the given list in place using cocktail shaker sort and returns it."""

    # The unsorted section is initially the entire list.
    start = 0
    end = len(arr) - 1

    while start < end:
        swapped = False

        # --- FORWARD PASS ---
        # Move the largest value in the unsorted section toward the right.
        for index in range(start, end):
            if arr[index] > arr[index + 1]:
                arr[index], arr[index + 1] = arr[index + 1], arr[index]
                swapped = True

        # If nothing moved, the list is already sorted.
        if not swapped:
            break

        # The final element of the current section is now in its correct place.
        end -= 1

        # Reset before scanning in the opposite direction.
        swapped = False

        # --- BACKWARD PASS ---
        # Move the smallest value in the unsorted section toward the left.
        for index in range(end, start, -1):
            if arr[index - 1] > arr[index]:
                arr[index - 1], arr[index] = arr[index], arr[index - 1]
                swapped = True

        # The first element of the current section is now in its correct place.
        start += 1

        # If the backward pass made no swaps, the remaining section is sorted.
        if not swapped:
            break

    return arr


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", cocktail_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", cocktail_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", cocktail_sort(reverse_sorted))

    with_duplicates = [5, 3, 8, 3, 1, 5, 2, 8, 1]
    print("\nBefore:", with_duplicates)
    print("After: ", cocktail_sort(with_duplicates))

    negative_values = [4, -3, 8, -1, 0, 5, -7, 2]
    print("\nBefore:", negative_values)
    print("After: ", cocktail_sort(negative_values))

    random_values = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", random_values)
    print("After: ", cocktail_sort(random_values))
