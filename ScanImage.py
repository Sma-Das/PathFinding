import cv2
import numpy as np
from queue import PriorityQueue
from dataclasses import dataclass


@dataclass
class state:
    EMPTY: int = 255
    WALL: int = 0
    NODE_CLR: int = 127


@dataclass
class Node:
    ''' cardinal postitions [row, column, distance] '''
    UP: tuple[int, int, int] = None
    DOWN: tuple[int, int, int] = None
    LEFT: tuple[int, int, int] = None
    RIGHT: tuple[int, int, int] = None

    def __iter__(self):
        yield from [self.UP, self.DOWN, self.LEFT, self.RIGHT]

    def __getitem__(self, pos):
        return pos


class FindNodes:
    def __init__(self, image: str, extension: str = ".png"):
        self.maze = cv2.imread(image, 0)
        if self.maze is None:
            raise ValueError("No picture supplied")
        self.rows, self.columns = self.maze.shape[:2]
        self.name = image.split(extension)[0]

        self.start = (0, self.maze[0].tolist().index(state.EMPTY))
        self.end = (self.rows - 1, self.maze[self.rows - 1].tolist().index(state.EMPTY))

    def neighbours(self, row: int, column: int) -> tuple[tuple[int]]:
        yield self.maze[row + 1][column], self.maze[row - 1][column]
        yield self.maze[row][column + 1], self.maze[row][column - 1]

    def find_nodes(self, draw=True) -> list:
        self.nodes = []
        for row in range(1, self.rows - 1):
            for column in range(1, self.columns - 1):
                (up, down), (left, right) = self.neighbours(row, column)
                if (up or down) and (left or right) and self.maze[row][column] == state.EMPTY:
                    self.nodes.append((row, column))
        self.nodes = [self.start, *self.nodes, self.end]
        if draw:
            self.draw_nodes()
        return self.nodes

    def draw_nodes(self, write=False, show=False, make_nodes=False):
        self.img_node = self.maze.copy()
        nodes = [self.start, *self.nodes, self.end]
        for row, column in nodes:
            self.img_node[row][column] = state.NODE_CLR

        if write:
            cv2.imwrite(f"{self.name}_node.png", self.img_node)
        if show:
            cv2.imshow(f"{self.name}_node.png", self.img_node)
            cv2.waitKey(0)

    def find_neighbours(self, row, column):
        print(row, column, "find_neighbours")

        def search(line, pos, inc):
            length = len(line) - 1
            while True:
                if pos + inc < 0 or pos + inc > length:
                    return
                pos += inc
                val = line[pos]
                if val == state.EMPTY:
                    continue
                elif val == state.NODE_CLR:
                    return pos
                elif val == state.WALL:
                    return

        r, c = self.img_node[row], self.img_node[:, column]
        cardinals = [
            (search(c, row, -1), column,),  # abs(u - row) if u else None),  # Up
            (search(c, row, 1), column, ),  # abs(d - row) if d else None),  # Down
            (row, search(r, column, -1),),  # abs(l - column) if l else None),  # left
            (row, search(r, column, 1), ),  # abs(r - column) if r else None),  # right
        ]

        for i, var in enumerate(cardinals):
            if var[0] is None or var[1] is None:
                cardinals[i] = None
        # else:
        # cardinals[i] = (abs(row - var[0] + column - var[1]), *cardinals[i])

        # return Node(*cardinals)
        return cardinals

    def compile_neighbours(self):
        return {pos: self.find_neighbours(*pos) for pos in self.find_nodes()}

    @property
    def length(self):
        if not hasattr(self, "nodes"):
            return
        else:
            return len(self.nodes)


if __name__ == '__main__':
    solver = FindNodes("Maze_Pictures/tiny.png")
    nodes = solver.find_nodes()
    node_img = solver.draw_nodes(write=True)
    row, column = nodes[1]
    print(row, column)
    print(solver.find_neighbours(8, 7))
    # print(solver.compile_neighbours())
    print(solver.length)
