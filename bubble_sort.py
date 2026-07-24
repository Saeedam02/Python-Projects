"""
bubble_sort.py

A classic Bubble Sort implementation.

Bubble Sort repeatedly steps through a list, comparing adjacent elements
and swapping them if they're in the wrong order. Each full pass "bubbles"
the largest remaining unsorted element into its correct position at the
end of the list. Includes an early-exit optimization: if a full pass makes
no swaps, the list is already sorted and we stop early.

Time complexity:
    Worst/average case: O(n^2)
    Best case (already sorted): O(n)   -- thanks to the early-exit check
Space complexity:
    O(1) -- sorts in place
"""

from typing import List


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of comparable elements in ascending order using bubble sort.
    Returns the same list object, sorted in place.
    """
    n = len(arr)

    for i in range(n - 1):
        swapped = False

        # After each pass, the last i elements are already in their final
        # sorted position, so we don't need to compare them again.
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break  # list is already sorted, no need for further passes

    return arr


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", bubble_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", bubble_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", bubble_sort(reverse_sorted))

    #Also you can get items from input:
    numbers = list(map(int, input().split()))
    print("\nBefore:",numbers)
    print("After: ", bubble_sort(numbers))
