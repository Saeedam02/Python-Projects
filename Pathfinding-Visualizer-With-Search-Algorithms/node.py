"""
node.py

Represents a single cell in the pathfinding grid. Each node tracks its own
state (empty, wall, start, end, visited/frontier/path during search) via
color, and knows how to find its traversable neighbors.
"""

import pygame

WHITE = (255, 255, 255)      # empty
BLACK = (10, 10, 10)          # wall / barrier
GREY = (200, 200, 200)        # grid lines
ORANGE = (255, 165, 0)        # start
TURQUOISE = (64, 224, 208)    # end
RED = (255, 80, 80)           # closed set (already explored)
GREEN = (0, 200, 100)         # open set (in frontier, not yet explored)
PURPLE = (160, 100, 255)      # final path


class Node:
    def __init__(self, row, col, size, total_rows):
        self.row = row
        self.col = col
        self.x = row * size
        self.y = col * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    # --- state checks ---
    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    # --- state setters ---
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_wall(self):
        self.color = BLACK

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid):
        """Populate self.neighbors with traversable (non-wall) up/down/left/right cells."""
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():  # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():  # right
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        # Needed so nodes can sit in a heapq alongside equal-priority entries
        return False
