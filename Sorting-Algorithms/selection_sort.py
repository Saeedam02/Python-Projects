"""
selection_sort.py

Selection Sort repeatedly finds the minimum element from the unsorted
portion of the list and swaps it into place at the front of that unsorted
portion. After each pass, one more element is in its final sorted spot.

Time complexity:
    Worst/average/best case: O(n^2)  -- it always scans the remaining
    unsorted portion in full, even if the list is already sorted
Space complexity:
    O(1) -- sorts in place

Notably makes at most O(n) swaps (unlike bubble sort), which makes it
appealing when the cost of writing/swapping elements is high relative to
the cost of comparisons.
"""

from typing import List
import random

def selection_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of comparable elements in ascending order using selection
    sort. Returns the same list object, sorted in place.
    """
    n = len(arr)

    for i in range(n - 1):
        min_idx = i

        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", selection_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", selection_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", selection_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", selection_sort(reverse_sorted))
