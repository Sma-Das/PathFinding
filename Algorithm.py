from ScanImage import FindNodes
from queue import PriorityQueue
from math import hypot
from collections import deque


class func:
    pass


def score_move(start: tuple[int, int], end: tuple[int, int]) -> int:
    s_row, s_column = start
    e_row, e_column = end
    return abs(s_row-e_row + s_column-e_column)


def heuristic(curr: tuple[int, int], end: tuple[int, int]) -> float:
    c_row, c_column = curr
    e_row, e_column = end
    return round(hypot(c_row - e_row, c_column - e_column), 2)


def reconstruct_path(current, came_from: dict):
    total_path = deque([current])
    while current in came_from:
        current = came_from[current]
        total_path.appendleft(current)
    return total_path


def A_Star(NodeClass: FindNodes, heuristic: func):
    # Node format: (row, column)
    start, end = NodeClass.start, NodeClass.end
    nodes = NodeClass.find_nodes()

    openSet = PriorityQueue()
    openSet.put((0, start))
    came_from = dict()

    gScore = dict.fromkeys(nodes, float('inf'))  # Distance from start
    gScore[start] = 0

    fScore = dict.fromkeys(nodes, float('inf'))  # Distance from end
    fScore[start] = heuristic(start, end)
    visited = deque([])
    while not openSet.empty():
        _, (current) = openSet.get()
        if current == end:

            return reconstruct_path(current, came_from), gScore

        for neighbour in NodeClass.find_neighbours(*current):
            if not neighbour:
                continue
            temp_g_score = gScore[current] + score_move(neighbour, current)
            if temp_g_score < gScore[neighbour]:
                came_from[neighbour] = current
                gScore[neighbour] = temp_g_score
                fScore[neighbour] = gScore[neighbour] + heuristic(neighbour, end)

                if neighbour not in visited:
                    openSet.put((fScore[neighbour], neighbour))
                    visited.append(neighbour)
    return False


def total_path(nodes):
    if not nodes or (length := len(nodes)) < 2:
        return 0
    left, total = 0, 0
    while left < length:
        total += score_move(nodes[left-1], nodes[left])
        left += 1
    return total


if __name__ == '__main__':

    maze = FindNodes("Maze_Pictures/combo400.png")
    nodes = maze.find_nodes()
    solved, gScore = A_Star(maze, heuristic)
    total_path(solved)
    maze.draw_solved(solved, total_path(solved), show=False, write=True)
