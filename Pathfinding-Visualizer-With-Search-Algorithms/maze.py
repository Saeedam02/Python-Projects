"""
maze.py

Simple random-obstacle maze generation. Not a "perfect maze" generator
(no guarantee of a single unique solution path) -- just randomized walls
at a given density, which is enough to make the algorithm comparisons
visually interesting and is what most viral pathfinding-visualizer repos
actually use.
"""

import random


def generate_random_walls(grid, rows, density=0.28, keep_clear=None):
    """
    Randomly marks `density` fraction of cells as walls.
    `keep_clear` is an optional set of (row, col) positions to never wall off
    (typically the current start/end positions).
    """
    keep_clear = keep_clear or set()
    for row in grid:
        for node in row:
            pos = node.get_pos()
            if pos in keep_clear:
                node.reset()
                continue
            if node.is_start() or node.is_end():
                continue
            if random.random() < density:
                node.make_wall()
            else:
                node.reset()
