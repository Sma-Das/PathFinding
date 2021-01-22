import cv2
import numpy as np
from queue import PriorityQueue
from dataclasses import dataclass


# maze = cv2.imread("Maze_Pictures/tiny.png", 0)
# rows, columns = maze.shape[:2]
# EMPTY, WALL = 255, 0


def neighbors(row: int, column: int, maze: np.ndarray) -> tuple[tuple[int]]:
    yield maze[row+1][column], maze[row-1][column]
    yield maze[row][column+1],  maze[row][column-1]


# def find_nodes(maze: np.ndarray):
#     open_set = PriorityQueue()
#     open_set.put((0, 0, maze[0].tolist().index(EMPTY)))
#     count = 1
#     for row in range(1, rows-1):
#         for column in range(1, columns-1):
#             (up, down), (left, right) = neighbors(row, column, maze)
#             if (up or down) and (left or right) and maze[row][column] == EMPTY:
#                 open_set.put((count, row, column))
#                 count += 1
#     open_set.put((count, rows-1, maze[rows-1].tolist().index(EMPTY)))  # End
#     return open_set


@dataclass
class state:
    EMPTY: int = 255
    WALL: int = 0


class FindNodes:
    def __init__(self, image: str):
        self.maze = cv2.imread(image)
        if not self.maze:
            raise ValueError("No picture supplied")
        self.rows, self.columns = self.maze.shape[:2]

    def neighbors(self, row: int, column: int) -> tuple[tuple[int]]:
        yield self.maze[row+1][column], self.maze[row-1][column]
        yield self.maze[row][column+1],  self.maze[row][column-1]

    def find_nodes(self) -> PriorityQueue:
        nodes = PriorityQueue()
        nodes.put((0, 0, self.maze[0].tolist().index(state.EMPTY)))  # Start
        count = 1
        for row in range(1, self.rows-1):
            for column in range(1, self.columns-1):
                (up, down), (left, right) = neighbors(row, column, self.maze)
                if (up or down) and (left or right) and self.maze[row][column] == state.EMPTY:
                    nodes.put((count, row, column))
                    count += 1
        nodes.put((count, self.rows-1, self.maze[self.rows-1].tolist().index(state.EMPTY)))  # End
        return nodes
