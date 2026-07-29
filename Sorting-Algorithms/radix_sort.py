"""
radix_sort.py

RADIX SORT
----------
Idea: sort numbers digit by digit, starting from the LEAST significant
digit (the ones place) and working up to the most significant digit.
Crucially, each digit-by-digit pass uses a STABLE sort (counting sort) --
stability is what makes the trick work, because it guarantees that once
a lower-significance digit has placed two numbers in the right relative
order, a later pass on a higher-significance digit won't accidentally
undo that ordering unless it actually needs to.

Example, sorting [170, 45, 75, 90] by ones digit, then tens, then hundreds:
    ones pass:    170, 90, 45, 75      (sorted by last digit: 0,0,5,5)
    tens pass:    170, 90, 45, 75      (sorted by tens digit: 7,9,4,7 -> ...)
    hundreds pass: 045, 075, 090, 170  -> 45, 75, 90, 170

Time complexity:
    O(d * (n + k)) where d = number of digits in the largest number,
    n = number of elements, k = base used (10 for decimal, so k=10 means
    each counting-sort pass is O(n + 10))
    In practice, for fixed-width integers, d is a small constant, so this
    behaves close to O(n) -- genuinely faster than comparison sorts for
    the right kind of data (e.g. sorting large lists of fixed-length IDs
    or postal codes).
Space complexity:
    O(n + k) -- same as the counting sort used internally

Limitation: like counting sort, this version only handles NON-NEGATIVE
integers. Handling negatives is a natural (and common) extension -- e.g.
by sorting negatives and positives separately, or by shifting the whole
array by its minimum value before sorting.
"""

from typing import List
import random

def radix_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of non-negative integers in ascending order using LSD
    (Least Significant Digit first) radix sort. Returns a NEW sorted list.
    """
    if not arr:
        return arr

    max_value = max(arr)

    # Start sorting by the ones place (digit "weight" 1), then tens (10),
    # then hundreds (100), etc. -- stop once the digit place we'd be
    # looking at is bigger than the largest number in the list (meaning
    # every number's higher digits are effectively 0 from here on).
    result = list(arr)
    digit_place = 1
    while max_value // digit_place > 0:
        result = _counting_sort_by_digit(result, digit_place)
        digit_place *= 10

    return result


def _counting_sort_by_digit(arr: List[int], digit_place: int) -> List[int]:
    """
    A counting sort variant that sorts by a single decimal digit, chosen
    by `digit_place` (1 = ones digit, 10 = tens digit, 100 = hundreds
    digit, etc.), instead of by the number's full value.

    This MUST be stable for radix sort to work correctly -- notice we
    walk the input in reverse when building the output, exactly like in
    counting_sort.py.
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # only 10 possible digit values: 0 through 9

    # Count occurrences of each digit at this place value.
    for value in arr:
        digit = (value // digit_place) % 10
        count[digit] += 1

    # Turn into cumulative counts -- same trick as in counting_sort.py.
    for d in range(1, 10):
        count[d] += count[d - 1]

    # Build the output in reverse-input order to preserve stability.
    for value in reversed(arr):
        digit = (value // digit_place) % 10
        count[digit] -= 1
        output[count[digit]] = value

    return output


if __name__ == "__main__":
    sample = [170, 45, 75, 90, 802, 24, 2, 66]
    print("Before:", sample)
    print("After: ", radix_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", radix_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", radix_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", radix_sort(reverse_sorted))
