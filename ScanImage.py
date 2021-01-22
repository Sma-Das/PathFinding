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
    pos: tuple[int, int]
    up: tuple[int, int] = None
    down: tuple[int, int] = None
    left: tuple[int, int] = None
    right: tuple[int, int] = None


class FindNodes:
    def __init__(self, image: str, extension: str = ".png"):
        self.maze = cv2.imread(image, 0)
        if self.maze is None:
            raise ValueError("No picture supplied")
        self.rows, self.columns = self.maze.shape[:2]
        self.name = image.split(extension)[0]

    def neighbors(self, row: int, column: int) -> tuple[tuple[int]]:
        yield self.maze[row+1][column], self.maze[row-1][column]
        yield self.maze[row][column+1],  self.maze[row][column-1]

    def find_nodes(self) -> PriorityQueue:
        self.start = (0, 0, self.maze[0].tolist().index(state.EMPTY))
        nodes = [self.start]
        count = 1
        for row in range(1, self.rows-1):
            for column in range(1, self.columns-1):
                (up, down), (left, right) = self.neighbors(row, column)
                if (up or down) and (left or right) and self.maze[row][column] == state.EMPTY:
                    nodes.append((count, row, column))
                    count += 1
        self.end = (count, self.rows-1, self.maze[self.rows-1].tolist().index(state.EMPTY))
        nodes.append(self.end)
        return nodes

    def draw_nodes(self, nodes: list, write=False, show=False):
        img_node = self.maze.copy()
        for _, row, column in nodes:
            img_node[row][column] = state.NODE_CLR

        if write:
            cv2.imwrite(f"{self.name}_node.png", img_node)
        if show is True:
            cv2.imshow(f"{self.name}_node.png", img_node)
            cv2.waitKey(0)
        return img_node

    def find_neighbours(self, node_row: int, node_col: int, img_node: np.ndarray) -> Node:
        node = Node(pos=(node_row, node_col))
        if (node_row, node_col) == self.start or (node_row, node_col) == self.end:
            return
        left, right = node_col, node_col
        up, down = node_row, node_row

        while left or right:
            if left == 0 or left is None:
                pass
            elif img_node[node_row][left-1] == state.EMPTY:
                left -= 1
            elif img_node[node_row][left-1] == state.NODE_CLR:
                node.left = (node_row, left-1)
                left = None
            elif img_node[node_row][left-1] == state.WALL:
                left = None

            if right == self.columns-1 or right is None:
                pass
            elif img_node[node_row][right+1] == state.EMPTY:
                right += 1
            elif img_node[node_row][right+1] == state.NODE_CLR:
                node.right = (node_row, right+1)
                right = None
            elif img_node[node_row][right+1] == state.WALL:
                right = None

        while up or down:
            if up == 0 or up is None:
                pass
            elif img_node[up-1][node_col] == state.EMPTY:
                up -= 1
            elif img_node[up-1][node_col] == state.NODE_CLR:
                node.up = (up-1, node_col)
                up = None
            elif img_node[up-1][node_col] == state.WALL:
                up = None

            if down == self.rows-1 or down is None:
                pass
            elif img_node[down+1][node_col] == state.EMPTY:
                down += 1
            elif img_node[down+1][node_col] == state.NODE_CLR:
                node.down = (down+1, node_col)
                down = None
            elif img_node[down+1][node_col] == state.WALL:
                down = None

        return node


if __name__ == '__main__':
    solver = FindNodes("Maze_Pictures/tiny.png")
    nodes = solver.find_nodes()
    node_img = solver.draw_nodes(nodes, write=True)
    _, row, column = nodes[17]
    print(solver.find_neighbours(row, column, node_img))
    # _, row, column = nodes[1]
