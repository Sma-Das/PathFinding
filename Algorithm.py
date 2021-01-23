from ScanImage import FindNodes
from queue import PriorityQueue


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


if __name__ == '__main__':

    solver = FindNodes("Maze_Pictures/tiny.png")
    nodes = solver.find_nodes()
    print(nodes.qsize())
