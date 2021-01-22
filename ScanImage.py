import cv2
import numpy as np
from queue import PriorityQueue
from dataclasses import dataclass


def neighbors(row: int, column: int, maze: np.ndarray) -> tuple[tuple[int]]:
    yield maze[row+1][column], maze[row-1][column]
    yield maze[row][column+1],  maze[row][column-1]


@dataclass
class state:
    EMPTY: int = 255
    WALL: int = 0
    NODE_CLR: int = 127


class FindNodes:
    def __init__(self, image: str, name: str = "maze"):
        self.maze = cv2.imread(image)
        if not self.maze:
            raise ValueError("No picture supplied")
        self.rows, self.columns = self.maze.shape[:2]
        self.name = name

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

    def draw_nodes(self, nodes: PriorityQueue, write=False, show=False):
        img_node = self.maze.copy()
        while nodes.qsize():
            _, row, column = nodes.get()
            img_node[row][column] = state.NODE_CLR
        if write is True:
            cv2.imwrite(f"{self.name}_node.png", img_node)
        if show is True:
            cv2.imshow(f"{self.name}_node.png", img_node)
            cv2.waitKey(0)
