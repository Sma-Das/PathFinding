from ScanImage import FindNodes
from queue import PriorityQueue
from math import hypot
from collections import deque


def fScore(start, curr):
    ''' score from the start to curr node '''
    s_row, s_col = start
    c_row, c_col = curr
    return (c_row - s_row) + (c_col - s_col)


def gScore(end, curr):
    ''' score from end to curr node '''
    e_row, e_col = end
    c_row, c_col = curr
    return (c_row - e_row) + (c_col - e_col)


def heuristic(start, end):
    s_row, s_column, _ = start
    e_row, e_column, _ = end
    return hypot(s_row - e_row, s_column - e_column)


def reconstruct_path(current, came_from: dict):
    total_path = deque([current])
    while current in came_from:
        current = came_from[current]
        total_path.appendleft(current)
    return total_path


def A_Star(start, end, h, nodes):
    openSet = PriorityQueue()
    openSet.put(start)
    came_from = dict()

    gScore = dict.fromkeys(nodes.keys(), float('inf'))
    gScore[start] = 0

    fScore = dict.fromkeys(nodes.keys(), float('inf'))
    fScore[start] = h(start, end)

    while not openSet.empty():
        current = openSet.get()
        if current == end:
            return reconstruct_path(current, came_from)


if __name__ == '__main__':

    solver = FindNodes("Maze_Pictures/tiny.png")
    nodes = solver.find_nodes()
    print(nodes.qsize())
