from ScanImage import FindNodes
from queue import PriorityQueue
from math import hypot
from collections import deque
from time import time
from sys import argv


class func:
    ''' no native function type '''
    pass


class AStar:
    def __init__(self, maze_name: str):
        self.maze_name = maze_name
        self.NodeClass = FindNodes(maze_name)

    def distance(self, start: tuple, end: tuple) -> int:
        '''
        distance from one node to its direct neighbour
            Args:
                start: tuple[int, int] - [row, column] of the start node
                end: tuple[int, int] - [row, column] of the end node

            Returns:
                int: distance between the nodes

            Note:
                Neighbours are always parallel in one dimension
        '''
        s_row, s_column = start
        e_row, e_column = end
        return abs(s_row-e_row + s_column-e_column)

    def heuristic(self, curr: tuple, end: tuple) -> float:
        '''
        Hypotenuse distance between curr node, and the maze end node
            Args:
                curr: tuple[int, int] - [row, column] of the current node
                end: tuple[int, int] - [row, column] of the end node

            Returns:
                float: Hypotenuse distance between the node and the end

            Note:
                Neighbours are always parallel in one dimension
        '''
        c_row, c_column = curr
        e_row, e_column = end
        return round(hypot(c_row - e_row, c_column - e_column), 2)

    def reconstruct_path(self, curr: tuple, came_from: dict) -> deque:
        '''
        The node-to-node path from curr to the start of the maze
            Args:
                curr: tuple[int, int] - [row, column] of the curr node
                came_from: dict - all the nodes preceding the curr node

            Returns:
                total_path: deque[tuple]
        '''
        total_path = deque([curr])
        while curr in came_from:
            curr = came_from[curr]
            total_path.appendleft(curr)
        return total_path

    def solve(self, heuristic: func = None) -> deque:
        '''
        Uses the A* algorithm, similar to Djkistra's method
            Args:
                heuristic: functin to evaulate score from curr pos to end pos

            Returns:
                deque: The path of the start node to the end node or deque() if no path is found

            Notes:
                https://en.wikipedia.org/wiki/A*_search_algorithm [Accessed: 25/01/2021]
        '''
        if not heuristic:
            heuristic = self.heuristic
        start, end = self.NodeClass.start, self.NodeClass.end

        start_time = time()
        print("Finding nodes...")
        nodes = self.NodeClass.find_nodes()
        total_time = round(time()-start_time, 2)
        print(f"Nodes found, that took {total_time}s and found {len(nodes)} nodes")
        del total_time

        print("Starting to solve")
        openSet = PriorityQueue()
        openSet.put((0, start))
        came_from = dict()

        gScore = dict.fromkeys(nodes, float('inf'))  # Distance from start
        gScore[start] = 0

        fScore = dict.fromkeys(nodes, float('inf'))  # Distance from end
        fScore[start] = heuristic(start, end)
        visited = set()
        try:
            while not openSet.empty():
                _, (current) = openSet.get()
                # print(current)
                if current == end:
                    total_time = round(time()-start_time, 2)
                    print(f"Maze solved! that took {total_time}s")
                    return self.reconstruct_path(current, came_from)

                for neighbour in self.NodeClass.find_neighbours(*current):
                    temp_g_score = gScore[current] + self.distance(neighbour, current)
                    if temp_g_score < gScore[neighbour]:
                        came_from[neighbour] = current
                        gScore[neighbour] = temp_g_score
                        fScore[neighbour] = temp_g_score + heuristic(neighbour, end)

                        if neighbour not in visited:
                            openSet.put((fScore[neighbour], neighbour))
                            visited.add(neighbour)
        except KeyboardInterrupt:
            total_time = round(time()-start_time, 2)
            print(f"\nKeyboard interupt at {total_time}s")
            print("Visited:", len(visited), "nodes")
            quit()

        total_time = round(time()-start_time, 2)
        print(f"Maze not solved, that took {total_time}s")
        return deque()

    def save_maze(self, solved: deque, show=False, write=False):

        def total_path(nodes: deque) -> int:
            '''
            Calculates the length of the path given
                Args:
                    solved: path of the nodes taken

                Returns:
                    total: The length of the path in units

                Notes:
                    Distance is calculated using the distance function
            '''
            if not nodes or (length := len(nodes)) < 2:
                return 0
            left, total = 0, 0
            while left < length:
                total += self.distance(nodes[left-1], nodes[left])
                left += 1
            return total

        length = total_path(solved)
        print(f"The path is {length} units long")
        self.NodeClass.draw_solved(solved, length, show=show, write=write)


def main(Solver):
    if len(argv) != 2:
        raise FileNotFoundError("No picture supplied")
    Solver = Solver(argv[1])
    solved = Solver.solve()
    if not solved:
        return
    show = input("Show pictures? (y/N): ").lower() == 'y'
    save = input("Save pictures? (y/N): ").lower() == 'y'
    Solver.save_maze(solved, show, save)


if __name__ == '__main__':
    main(AStar)
