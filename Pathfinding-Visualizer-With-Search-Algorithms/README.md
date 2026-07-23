# Search Algorithm & Pathfinding Visualizer

An interactive Pygame app that visualizes and compares four classic search
algorithms — **BFS**, **DFS**, **Dijkstra**, and **A\*** — solving the same
grid maze in real time, side by side in behavior if not in pixels.

This is one of the most searched, most-cloned genres of Python project on
GitHub (search terms like "python pathfinding visualizer" and "A* algorithm
python" get consistent, high search volume), and for good reason: watching
a search algorithm actually explore a maze makes an abstract CS concept
immediately click.

## Demo

*(Add a screen recording GIF here — this is exactly the kind of project
that benefits enormously from one. Tools like ScreenToGif (Windows) or
Kap (Mac) work well.)*

## Features

- **Four algorithms, one interface** — swap between BFS, DFS, Dijkstra, and
  A* with a single keypress and re-run on the exact same maze
- **Fully interactive grid** — click to place start/end points, click-drag
  to draw walls, right-click to erase
- **Random maze generation** — press `M` to instantly generate a new
  obstacle layout
- **Live stats bar** — after each run, see nodes explored, path length, and
  time taken, so you can *see* why A* beats Dijkstra beats BFS beats DFS
  instead of just being told
- **Clean separation of concerns** — algorithms are pure functions with no
  pygame rendering logic baked in, so they're easy to read, test, or reuse
  outside the visualizer

## Quickstart

```bash
git clone https://github.com/Saeedam02/Python-Projects.git
cd Python-Projects/pathfinding-visualizer
pip install -r requirements.txt
python main.py
```

## Controls

| Input | Action |
|---|---|
| Left click | 1st click: place **start** · 2nd click: place **end** · after that: draw **walls** |
| Right click | Erase a cell (clears walls, or removes start/end if clicked on them) |
| `1` `2` `3` `4` | Select algorithm — BFS / DFS / Dijkstra / A* |
| `Space` | Run the selected algorithm |
| `M` | Generate a random maze |
| `C` | Clear the whole grid |
| `Esc` | Quit |

## Why these four algorithms

- **BFS** explores level-by-level and is *guaranteed* to find the shortest
  path on this unweighted grid — the baseline every other algorithm is
  measured against.
- **DFS** dives as deep as possible before backtracking. It'll find *a*
  path, but as the stats bar makes obvious, usually a much longer one. It's
  included specifically because people expect a "search algorithms" project
  to explain why DFS is a bad fit for shortest-pathfinding, not just what it
  does.
- **Dijkstra** is the general-purpose shortest-path algorithm. On this
  uniform-cost grid it explores exactly the same nodes as BFS (mathematically
  equivalent here) — the point is that its priority-queue design generalizes
  to weighted graphs, where BFS breaks down.
- **A\*** adds a Manhattan-distance heuristic on top of Dijkstra, which lets
  it skip large parts of the search space while still guaranteeing the
  shortest path. This is usually the "aha" moment of the demo: same answer,
  visibly fewer cells explored.

## Project structure

```
pathfinding-visualizer/
├── main.py         # Pygame window, event loop, mouse/keyboard controls
├── node.py          # Node class: cell state, color, neighbor lookup
├── algorithms.py     # BFS, DFS, Dijkstra, A* — pure logic, no rendering
├── maze.py            # Random wall/obstacle generator
└── requirements.txt
```

## Possible extensions

- Add weighted terrain (e.g. "mud" cells that cost more to cross) to show
  where BFS/DFS genuinely break down and Dijkstra/A* pull ahead
- Add diagonal movement and an octile-distance heuristic
- Add a "perfect maze" generator (recursive backtracker) for a single
  guaranteed solution path
- Port the grid/algorithm logic to a Streamlit or web version for easier
  sharing (trade-off: smoother step-by-step animation is easier in Pygame)

## License

MIT
