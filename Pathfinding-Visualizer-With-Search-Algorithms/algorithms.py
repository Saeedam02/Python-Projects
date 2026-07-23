"""
algorithms.py

Implementations of four classic search algorithms, all sharing the same
signature so the visualizer can swap between them freely:

    algorithm(draw_callback, grid, start, end) -> dict of stats

Each one:
  - Colors nodes as they enter the frontier ("open") and once fully
    explored ("closed"), calling draw_callback() after each meaningful
    step so the caller can render/animate it.
  - Reconstructs and colors the final shortest/found path if one exists.
  - Returns stats: whether a path was found, how many nodes were visited,
    the path length, and elapsed time.

These functions have NO pygame dependency beyond what's already on the
Node objects (color state) -- draw_callback is just any zero-argument
function, which makes them straightforward to unit test headlessly.
"""

import time
import heapq
from collections import deque


def _reconstruct_path(came_from, current, draw_callback):
    length = 1
    while current in came_from:
        current = came_from[current]
        if not current.is_start():
            current.make_path()
            length += 1
        draw_callback()
    return length


def _manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def bfs(draw_callback, grid, start, end):
    """Breadth-First Search. Guarantees shortest path on an unweighted grid."""
    t0 = time.perf_counter()
    queue = deque([start])
    came_from = {}
    visited = {start}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        if current == end:
            path_length = _reconstruct_path(came_from, end, draw_callback)
            end.make_end()
            start.make_start()
            return {"found": True, "nodes_explored": nodes_explored,
                    "path_length": path_length, "time_s": time.perf_counter() - t0}

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                if not neighbor.is_end():
                    neighbor.make_open()

        draw_callback()
        if current != start:
            current.make_closed()

    return {"found": False, "nodes_explored": nodes_explored, "path_length": 0,
            "time_s": time.perf_counter() - t0}


def dfs(draw_callback, grid, start, end):
    """Depth-First Search. Finds *a* path, not necessarily the shortest one."""
    t0 = time.perf_counter()
    stack = [start]
    came_from = {}
    visited = {start}
    nodes_explored = 0

    while stack:
        current = stack.pop()
        nodes_explored += 1

        if current == end:
            path_length = _reconstruct_path(came_from, end, draw_callback)
            end.make_end()
            start.make_start()
            return {"found": True, "nodes_explored": nodes_explored,
                    "path_length": path_length, "time_s": time.perf_counter() - t0}

        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                if not neighbor.is_end():
                    neighbor.make_open()

        draw_callback()
        if current != start:
            current.make_closed()

    return {"found": False, "nodes_explored": nodes_explored, "path_length": 0,
            "time_s": time.perf_counter() - t0}


def dijkstra(draw_callback, grid, start, end):
    """Dijkstra's algorithm. Every edge has weight 1 here, so it behaves like
    BFS but demonstrates the general priority-queue-based shortest-path approach."""
    t0 = time.perf_counter()
    count = 0
    open_set = [(0, count, start)]
    came_from = {}
    dist = {node: float("inf") for row in grid for node in row}
    dist[start] = 0
    in_open_set = {start}
    nodes_explored = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        in_open_set.discard(current)
        nodes_explored += 1

        if current == end:
            path_length = _reconstruct_path(came_from, end, draw_callback)
            end.make_end()
            start.make_start()
            return {"found": True, "nodes_explored": nodes_explored,
                    "path_length": path_length, "time_s": time.perf_counter() - t0}

        for neighbor in current.neighbors:
            tentative = dist[current] + 1
            if tentative < dist[neighbor]:
                came_from[neighbor] = current
                dist[neighbor] = tentative
                if neighbor not in in_open_set:
                    count += 1
                    heapq.heappush(open_set, (tentative, count, neighbor))
                    in_open_set.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()

        draw_callback()
        if current != start:
            current.make_closed()

    return {"found": False, "nodes_explored": nodes_explored, "path_length": 0,
            "time_s": time.perf_counter() - t0}


def a_star(draw_callback, grid, start, end):
    """A* search using the Manhattan distance heuristic (admissible on a grid
    with only 4-directional movement), which typically explores far fewer
    nodes than Dijkstra for the same shortest path."""
    t0 = time.perf_counter()
    count = 0
    open_set = [(0, count, start)]
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = _manhattan(start.get_pos(), end.get_pos())
    in_open_set = {start}
    nodes_explored = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        in_open_set.discard(current)
        nodes_explored += 1

        if current == end:
            path_length = _reconstruct_path(came_from, end, draw_callback)
            end.make_end()
            start.make_start()
            return {"found": True, "nodes_explored": nodes_explored,
                    "path_length": path_length, "time_s": time.perf_counter() - t0}

        for neighbor in current.neighbors:
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + _manhattan(neighbor.get_pos(), end.get_pos())
                if neighbor not in in_open_set:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    in_open_set.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()

        draw_callback()
        if current != start:
            current.make_closed()

    return {"found": False, "nodes_explored": nodes_explored, "path_length": 0,
            "time_s": time.perf_counter() - t0}


ALGORITHM_REGISTRY = {
    "BFS": bfs,
    "DFS": dfs,
    "Dijkstra": dijkstra,
    "A*": a_star,
}
