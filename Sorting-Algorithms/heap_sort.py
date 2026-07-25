"""
heap_sort.py

Heap Sort first builds a max-heap out of the list (so the largest element
sits at the root), then repeatedly swaps the root with the last unsorted
element and "sifts down" to restore the heap property -- shrinking the
heap by one each time until the whole list is sorted.

Time complexity:
    Worst/average/best case: O(n log n)  -- unlike quicksort, this is
    guaranteed, with no unlucky-pivot worst case
Space complexity:
    O(1) -- sorts in place (the "heap" lives inside the array itself)

Trade-off versus merge sort / quicksort: heap sort has the same O(n log n)
guarantee and doesn't need extra memory, but in practice tends to be a bit
slower due to poor cache locality (heap operations jump around the array).
"""

from typing import List
import random

def heap_sort(arr: List[int]) -> List[int]:
    """
    Sorts a list of comparable elements in ascending order using heap sort.
    Returns the same list object, sorted in place.
    """
    n = len(arr)

    # Build a max-heap: start from the last parent node and sift down.
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)

    # Repeatedly move the current max (root) to the end, then re-heapify
    # the shrinking unsorted prefix.
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down(arr, end, 0)

    return arr


def _sift_down(arr: List[int], heap_size: int, root: int) -> None:
    """Restores the max-heap property for the subtree rooted at `root`."""
    largest = root
    left = 2 * root + 1
    right = 2 * root + 2

    if left < heap_size and arr[left] > arr[largest]:
        largest = left

    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    if largest != root:
        arr[root], arr[largest] = arr[largest], arr[root]
        _sift_down(arr, heap_size, largest)


if __name__ == "__main__":
    sample = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print("Before:", sample)
    print("After: ", heap_sort(sample))

    already_sorted = [1, 2, 3, 4, 5]
    print("\nBefore:", already_sorted)
    print("After: ", heap_sort(already_sorted))

    reverse_sorted = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    print("\nBefore:", reverse_sorted)
    print("After: ", heap_sort(reverse_sorted))

    reverse_sorted = [random.randint(0, 500) for _ in range(100)]
    print("\nBefore:", reverse_sorted)
    print("After: ", heap_sort(reverse_sorted))
