# import cv2
from cv2 import imread, imwrite, imshow, waitKey, cvtColor, COLOR_GRAY2RGB
from dataclasses import dataclass
from collections import deque
from functools import lru_cache


@dataclass
class state:
    EMPTY: int = 255
    WALL: int = 0
    NODE_CLR: int = 127


class FindNodes:
    def __init__(self, image: str, extension: str = ".png"):
        self.maze = imread(image, 0)
        if self.maze is None:
            raise ValueError("No picture supplied")
        self.fast_maze = deque(map(deque, self.maze))
        # print(self.fast_maze)
        self.rows, self.columns = self.maze.shape[:2]
        self.name = image.split(extension)[0]
        self.name = "Solved/" + self.name.split("/")[-1]
        self.start = (0, self.maze[0].tolist().index(state.EMPTY))
        self.end = (self.rows - 1, self.maze[self.rows - 1].tolist().index(state.EMPTY))

    def neighbours(self, row: int, column: int) -> tuple[tuple[int]]:
        return \
            self.fast_maze[row + 1][column], self.fast_maze[row - 1][column], \
            self.fast_maze[row][column + 1], self.fast_maze[row][column - 1]

    def find_nodes(self, draw=True) -> list:
        self.nodes = deque([self.start, self.end])
        for row in range(1, self.rows - 1):
            for column in range(1, self.columns - 1):
                up, down, left, right = self.neighbours(row, column)
                if (up or down) and (left or right) and self.fast_maze[row][column] == state.EMPTY:
                    self.nodes.append((row, column))
        if draw:
            self.draw_nodes()
        return self.nodes

    def draw_nodes(self, write=False, show=False, make_nodes=False):
        self.img_node = self.maze.copy()
        for row, column in self.nodes:
            self.img_node[row][column] = state.NODE_CLR

        if write:
            imwrite(f"{self.name}_node.png", self.img_node)
        if show:
            print("Press esc to exit")
            imshow(f"{self.name}_node.png", self.img_node)
            waitKey(0)

    @lru_cache
    def find_neighbours(self, row: int, column):

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

        r, c = self.img_node[row], self.img_node[:, column]  # Column or row
        cardinals = deque([
            (search(c, row, -1), column,),  # Up
            (search(c, row, 1), column, ),  # Down
            (row, search(r, column, -1),),  # left
            (row, search(r, column, 1), ),  # right
        ])
        # for i, var in enumerate(cardinals):
        # if var[0] is None or var[1] is None:
        # cardinals[i] = None

        # return cardinals
        return [var for var in cardinals if var[0] is not None and var[1] is not None]

    @property
    def length(self):
        if not hasattr(self, "nodes"):
            return 0
        else:
            return len(self.nodes)

    def draw_solved(self, nodes: deque, path_length: int = 100, show=False, write=False):
        if not nodes:
            raise ValueError("No nodes supplied")
        solved = cvtColor(self.maze, COLOR_GRAY2RGB)

        def color(i, length):  # BGR
            return (B := 255*i//length, 0, 255-B)
        path_length += len(nodes)
        count = 0
        curr = nodes.popleft()
        while nodes:
            prev, curr = curr, nodes.popleft()
            pr, pc = prev
            cr, cc = curr
            if pr > cr:
                pr, cr = cr, pr
            if pc > cc:
                pc, cc = cc, pc

            for r in range(pr, cr+1):
                solved[r][pc] = color(count, path_length)
                count += 1
            for c in range(pc, cc+1):
                solved[pr][c] = color(count, path_length)
                count += 1
            count -= 1
        if write:
            imwrite(f"{self.name}_solved.png", solved)
        if show:
            imshow(f"{self.name}_solved.png", solved)
            waitKey(0)
