"""
counting_sort.py

COUNTING SORT
-------------
Idea: this is NOT a comparison-based sort (it never asks "is A bigger than
B?"). Instead, it counts how many times each value appears, then uses
those counts to figure out exactly where each element belongs in the
final sorted output. That's what lets it beat the O(n log n) comparison-
sort lower bound -- but only under a specific condition: it only works on
non-negative integers within a known, reasonably small range.

Time complexity:
    O(n + k) where n = number of elements, k = range of possible values
    (i.e. max_value + 1). This is faster than O(n log n) when k is
    comparable to or smaller than n -- but becomes worse than a
    comparison sort if k is huge (e.g. sorting 10 numbers between 0 and
    10 million would allocate a 10-million-slot counting array for no
    benefit).
Space complexity:
    O(n + k) -- needs both a count array of size k and an output array
    of size n

Counting sort is the key building block used inside radix_sort.py, where
it's applied one digit at a time instead of to the whole number.
"""

from typing import List
import random   

def counting_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of NON-NEGATIVE integers in ascending order.
    Returns a NEW sorted list (this algorithm isn't naturally in-place).
    """
    if not arr:
        return arr

    # Step 1: find the range of values we need to count.
    max_value = max(arr)

    # Step 2: count how many times each value appears.
    # count[v] will end up holding "how many times value v appears in arr".
    count = [0] * (max_value + 1)
    for value in arr:
        count[value] += 1

    # Step 3: turn counts into "cumulative counts" -- count[v] now means
    # "how many elements are <= v". This tells us the LAST index that
    # value v should occupy in the sorted output.
    for v in range(1, len(count)):
        count[v] += count[v - 1]

    # Step 4: build the output array. We walk the input from RIGHT TO LEFT
    # specifically to keep the sort STABLE (equal elements keep their
    # original relative order) -- this also matters for radix_sort.py,
    # which depends on counting_sort being stable to work correctly.
    output = [0] * len(arr)
    for value in reversed(arr):
        count[value] -= 1               # this is value's correct final index
        output[count[value]] = value

    return output


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6, 2, 5]
    print("Before:", sample)
    print("After: ", counting_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", counting_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", counting_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", counting_sort(reverse_sorted))
