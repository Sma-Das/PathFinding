import cv2
from dataclasses import dataclass
from collections import deque


@dataclass
class state:
    EMPTY: int = 255
    WALL: int = 0
    NODE_CLR: int = 127


class FindNodes:
    def __init__(self, image: str, extension: str = ".png"):
        self.maze = cv2.imread(image, 0)
        if self.maze is None:
            raise ValueError("No picture supplied")
        self.rows, self.columns = self.maze.shape[:2]
        self.name = image.split(extension)[0]
        self.name = "Solved/" + self.name.split("/")[-1]
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
            print("Press esc to exit")
            cv2.imshow(f"{self.name}_node.png", self.img_node)
            cv2.waitKey(0)

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
        cardinals = [
            (search(c, row, -1), column,),  # Up
            (search(c, row, 1), column, ),  # Down
            (row, search(r, column, -1),),  # left
            (row, search(r, column, 1), ),  # right
        ]

        for i, var in enumerate(cardinals):
            if var[0] is None or var[1] is None:
                cardinals[i] = None

        return cardinals
        # return [None if var else var for var in cardinals if var[0] is None or var[1] is None]

    @property
    def length(self):
        if not hasattr(self, "nodes"):
            return 0
        else:
            return len(self.nodes)

    def draw_solved(self, nodes: deque, path_length: int = 100, show=False, write=False):
        if not nodes:
            raise ValueError("No nodes supplied")
        solved = cv2.cvtColor(self.maze, cv2.COLOR_GRAY2RGB)

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
            cv2.imwrite(f"{self.name}_solved.png", solved)
        if show:
            cv2.imshow(f"{self.name}_solved.png", solved)
            cv2.waitKey(0)


if __name__ == '__main__':
    node_finder = FindNodes("Maze_Pictures/medium.png")
    node_finder.find_nodes()
    node_finder.draw_nodes(write=True)
