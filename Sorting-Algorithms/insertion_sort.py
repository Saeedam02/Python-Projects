"""
insertion_sort.py

Insertion Sort builds the sorted list one element at a time. It takes each
element and "inserts" it into its correct position among the already-sorted
elements to its left, shifting larger elements right to make room.

Time complexity:
    Worst/average case: O(n^2)
    Best case (already sorted): O(n)
Space complexity:
    O(1) -- sorts in place

Good in practice for small lists or nearly-sorted data (e.g. it's often used
as the base case inside faster hybrid sorts like Timsort).
"""

from typing import List
import random


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of comparable elements in ascending order using insertion
    sort. Returns the same list object, sorted in place.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # shift elements greater than key one position to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", insertion_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", insertion_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", insertion_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", insertion_sort(reverse_sorted))
