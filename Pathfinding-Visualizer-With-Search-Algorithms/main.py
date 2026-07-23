"""
main.py

Interactive Pathfinding & Search Algorithm Visualizer.

Run with:
    python main.py

Controls:
  - Left click:  first click places START, second click places END,
                 every click after that draws WALLS
  - Right click: erase a cell back to empty (also clears start/end if
                 clicked on them)
  - 1 / 2 / 3 / 4:  select algorithm -> BFS / DFS / Dijkstra / A*
  - SPACE:       run the currently selected algorithm
  - M:           generate a random maze (keeps start/end if already placed)
  - C:           clear the entire grid
  - ESC:         quit
"""

import pygame
from node import Node, WHITE, GREY, ORANGE, TURQUOISE
from algorithms import ALGORITHM_REGISTRY
from maze import generate_random_walls

WIDTH = 800
ROWS = 40
STATS_HEIGHT = 60
WINDOW = pygame.display.set_mode((WIDTH, WIDTH + STATS_HEIGHT))
pygame.display.set_caption("Search Algorithm Visualizer — BFS / DFS / Dijkstra / A*")

FONT = None  # initialized after pygame.init() in main()

ALGORITHM_KEYS = {
    pygame.K_1: "BFS",
    pygame.K_2: "DFS",
    pygame.K_3: "Dijkstra",
    pygame.K_4: "A*",
}


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([Node(i, j, gap, rows) for j in range(rows)])
    return grid


def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GREY, (i * gap, 0), (i * gap, width))


def draw_stats_bar(win, width, height, algorithm_name, last_stats):
    pygame.draw.rect(win, (25, 25, 25), (0, width, width, height))
    if last_stats is None:
        text = f"Algorithm: {algorithm_name}  |  press SPACE to run, M for random maze, C to clear"
    elif last_stats["found"]:
        text = (
            f"Algorithm: {algorithm_name}  |  Path FOUND  |  "
            f"nodes explored: {last_stats['nodes_explored']}  |  "
            f"path length: {last_stats['path_length']}  |  "
            f"time: {last_stats['time_s']*1000:.1f} ms"
        )
    else:
        text = (
            f"Algorithm: {algorithm_name}  |  NO PATH FOUND  |  "
            f"nodes explored: {last_stats['nodes_explored']}  |  "
            f"time: {last_stats['time_s']*1000:.1f} ms"
        )
    surface = FONT.render(text, True, (230, 230, 230))
    win.blit(surface, (10, width + height // 2 - 8))


def draw(win, grid, rows, width, algorithm_name, last_stats):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid_lines(win, rows, width)
    draw_stats_bar(win, width, STATS_HEIGHT, algorithm_name, last_stats)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    row = min(max(row, 0), rows - 1)
    col = min(max(col, 0), rows - 1)
    return row, col


def reset_search_colors(grid):
    """Clear any open/closed/path coloring but keep walls, start, and end."""
    for row in grid:
        for node in row:
            if node.is_open() or node.is_closed():
                node.reset()
            elif node.color not in (WHITE, ORANGE, TURQUOISE) and not node.is_wall():
                # covers PURPLE path cells left over from a previous run
                node.reset()


def main():
    global FONT
    pygame.init()
    FONT = pygame.font.SysFont("consolas", 16)

    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None
    current_algorithm = "A*"
    last_stats = None

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(60)
        draw(WINDOW, grid, ROWS, WIDTH, current_algorithm, last_stats)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                if pos[1] >= WIDTH:
                    continue
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.make_wall()

            elif pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                if pos[1] >= WIDTH:
                    continue
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key in ALGORITHM_KEYS:
                    current_algorithm = ALGORITHM_KEYS[event.key]

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    last_stats = None
                    grid = make_grid(ROWS, WIDTH)

                if event.key == pygame.K_m:
                    keep_clear = set()
                    if start:
                        keep_clear.add(start.get_pos())
                    if end:
                        keep_clear.add(end.get_pos())
                    generate_random_walls(grid, ROWS, density=0.28, keep_clear=keep_clear)
                    if start:
                        start.make_start()
                    if end:
                        end.make_end()
                    last_stats = None

                if event.key == pygame.K_SPACE and start and end:
                    reset_search_colors(grid)
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    def draw_callback():
                        # allow the OS to see the window as responsive during the search
                        for e in pygame.event.get(pygame.QUIT):
                            pygame.quit()
                            raise SystemExit
                        draw(WINDOW, grid, ROWS, WIDTH, current_algorithm, last_stats)

                    algorithm_fn = ALGORITHM_REGISTRY[current_algorithm]
                    last_stats = algorithm_fn(draw_callback, grid, start, end)

    pygame.quit()


if __name__ == "__main__":
    main()
