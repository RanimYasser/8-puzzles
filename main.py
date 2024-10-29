from collections import deque

class Node:
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth

class Board:
    def __init__(self, root):
        self.root = root
        self.initial_state = root.state
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.size = 3

    def find_blank_tile(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def get_possible_moves(self, node):
        moves = []
        x, y = self.find_blank_tile(node.state)
        directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

        for move, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_state = [row[:] for row in node.state]
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                moves.append(Node(new_state, parent=node, depth=node.depth + 1))

        return moves


class GameAlgorithms:
    def __init__(self, board):
        self.board = board

    def get_path_to_goal(self, node):  # takes the goal node to get the full path by tracing the parent node
        path_to_goal = []
        while node:
            path_to_goal.append(node.state)
            node = node.parent
        return path_to_goal[::-1]  # Reverse to get the path from start to goal

    def goal_test(self, current_state):
        return current_state == self.board.goal_state

    def bfs(self):
        frontiers_queue = deque([Node(self.board.initial_state)])
        explored_set = set()
        while frontiers_queue:
            current_node = frontiers_queue.popleft()
            current_state_tuple = tuple(tuple(row) for row in current_node.state)
            if self.goal_test(current_node.state):
                return self.get_path_to_goal(current_node)
            if current_state_tuple not in explored_set:
                explored_set.add(current_state_tuple)
                for new_neighbor_node in self.board.get_possible_moves(current_node):
                    new_state_tuple = tuple(tuple(row) for row in new_neighbor_node.state)
                    if new_state_tuple not in explored_set:
                        frontiers_queue.append(new_neighbor_node)
        return None

    def dfs(self, max_depth=None):
        frontiers_stack = [Node(self.board.initial_state)]
        explored_set = set()
        while frontiers_stack:
            current_node = frontiers_stack.pop()
            current_state_tuple = tuple(tuple(row) for row in current_node.state)
            if self.goal_test(current_node.state):
                return self.get_path_to_goal(current_node)
            if current_state_tuple not in explored_set:
                explored_set.add(current_state_tuple)
                if max_depth is None or current_node.depth < max_depth:
                    for new_neighbor_node in self.board.get_possible_moves(current_node):
                        new_state_tuple = tuple(tuple(row) for row in new_neighbor_node.state)
                        if new_state_tuple not in explored_set:
                            frontiers_stack.append(new_neighbor_node)
        return None

    def idfs(self, max_depth):
        for depth_limit in range(max_depth + 1):
            solution_path_idfs = self.dfs(max_depth=depth_limit)
            if solution_path_idfs:
                return solution_path_idfs, depth_limit
        return None

    def print_goal_path(self, path):
        if path:
            print("Path to Goal:")
            for step in path:
                for row in step:
                    print(row)
                print("------")
        else:
            print("No solution found.")


# Example usage
initial_state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
root_node = Node(initial_state)
board = Board(root_node)
algorithms = GameAlgorithms(board)

# Test BFS
print("BFS Solution:")
goal_path_bfs = algorithms.bfs()
algorithms.print_goal_path(goal_path_bfs)

# Test DFS
print("\nDFS Solution:")
goal_path_dfs = algorithms.dfs()
algorithms.print_goal_path(goal_path_dfs)

# Test IDFS
print("\nIDFS Solution:")
goal_path_idfs, depth_used = algorithms.idfs(max_depth=20)
print(f"Depth used in IDFS: {depth_used}")
algorithms.print_goal_path(goal_path_idfs)
