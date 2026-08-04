"""
shell_sort.py

SHELL SORT
----------
Idea: an improved version of insertion sort.

Insertion sort is efficient when elements are already close to their correct
positions, but it can be slow when a small element is located near the end of
the list because that element must move left one position at a time.

Shell sort solves this by first comparing elements that are far apart.

  1. Start with a large GAP between compared elements.
  2. Perform a modified insertion sort on elements separated by that gap.
  3. Gradually reduce the gap.
  4. Finish with a normal insertion sort when the gap becomes 1.

By the final pass, most elements are already close to their correct positions,
so the insertion-sort step is usually much faster.

Example gap sequence for a list of length 9:
    4 -> 2 -> 1

Time complexity:
    Worst case   : O(n²) with the simple gap-halving sequence used here
    Average case : depends heavily on the chosen gap sequence, but is usually
                   significantly faster than ordinary insertion sort
    Best case    : approximately O(n log n), because several passes are still
                   required even when the input is already sorted

Space complexity:
    O(1) -- Shell sort rearranges the elements directly inside the original
    list and only uses a few temporary variables

Shell sort is NOT STABLE: equal elements may change their original relative
order because elements can move across large gaps.

This implementation sorts the supplied list IN PLACE and also returns it for
convenience.
"""

from typing import List
import random


def shell_sort(arr: List[int]) -> List[int]:
    """Sorts the given list in place using Shell sort and returns it."""

    # Begin with a gap approximately half the size of the list.
    gap = len(arr) // 2

    # Continue until the final insertion-sort pass with gap = 1 is complete.
    while gap > 0:

        # Perform a gap-based insertion sort.
        #
        # Elements at positions such as:
        #   0, gap, 2 * gap, 3 * gap, ...
        # are treated as if they formed a smaller insertion-sort sequence.
        for current_index in range(gap, len(arr)):
            current_value = arr[current_index]
            comparison_index = current_index

            # Move larger gap-separated elements to the right until the
            # correct position for current_value is found.
            while (
                comparison_index >= gap
                and arr[comparison_index - gap] > current_value
            ):
                arr[comparison_index] = arr[comparison_index - gap]
                comparison_index -= gap

            # Insert the saved value into its correct gap-sorted position.
            arr[comparison_index] = current_value

        # Reduce the gap for the next pass.
        gap //= 2

    return arr


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", shell_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", shell_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", shell_sort(reverse_sorted))

    with_duplicates = [5, 3, 8, 3, 1, 5, 2, 8, 1]
    print("\nBefore:", with_duplicates)
    print("After: ", shell_sort(with_duplicates))

    random_values = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", random_values)
    print("After: ", shell_sort(random_values))
  
