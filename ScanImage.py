import cv2
import numpy as np
from collections import deque


maze = cv2.imread("Maze_Pictures/medium.png", 0)
rows, columns = maze.shape[:2]
EMPTY, WALL = 255, 0


def neighbors(row, column, maze):
    yield maze[row+1][column], maze[row-1][column]
    yield maze[row][column+1],  maze[row][column-1]


def find_nodes(maze: np.ndarray):
    Node = deque([(0, 0, maze[0].tolist().index(EMPTY))])  # Start
    count = 1
    for row in range(1, rows-1):
        for column in range(1, columns-1):
            (up, down), (left, right) = neighbors(row, column, maze)
            if (up or down) and (left or right) and maze[row][column]:
                Node.append((count, row, column))
                count += 1
    Node.append((count, rows-1, maze[rows-1].tolist().index(EMPTY)))  # End
    return Node


if __name__ == '__main__':
    Nodes = find_nodes(maze)
    for _, row, column in Nodes:
        maze[row][column] = 127
    cv2.imwrite("./maze_Pictures/node_img.png", maze)
    print(Nodes)
    print(type(maze))
    # print(maze)
    print(len(Nodes))
    # cv2.waitKey(0)
