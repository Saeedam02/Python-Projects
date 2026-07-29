"""
insertion_sort.py

INSERTION SORT
--------------
Idea: build the sorted portion of the list one element at a time, from
left to right. For each new element, slide it left past every element
that's bigger than it, until it lands in its correct spot -- exactly like
sorting playing cards in your hand one card at a time.

Time complexity:
    Worst/average case : O(n^2)   -- many shifts needed on random data
    Best case           : O(n)    -- already-sorted input needs zero shifts
Space complexity:
    O(1) -- sorts in place, no extra array needed

When it's actually a good choice:
    - Small lists (the constant factors are tiny, so it can beat O(n log n)
      algorithms for n roughly under ~20-50)
    - Nearly-sorted data
    - As the "base case" inside hybrid sorts like Timsort (used by Python's
      own built-in sort!) and Introsort
"""

from typing import List
import random

def insertion_sort(arr: List[int]) -> List[int]:
    """Sorts `arr` in ascending order, in place, and also returns it."""

    # We consider arr[0] as already "sorted" (a list of one element is
    # trivially sorted), so we start comparing from index 1.
    for i in range(1, len(arr)):
        key = arr[i]        # the element we're about to insert into place
        j = i - 1            # start comparing with the element just before it

        # Shift every element bigger than `key` one step to the right,
        # opening up a gap for `key` to eventually drop into.
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        # `j` has now moved one step past where `key` belongs, so we
        # place it at j + 1.
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
