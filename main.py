from collections import deque

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, state):
        state_tuple = tuple(tuple(row) for row in state)
        if state_tuple not in self.vertices:
            new_vertex = Vertex(state)
            self.vertices[state_tuple] = new_vertex
        return self.vertices[state_tuple]


class Vertex:
    def __init__(self, state):
        self.state = state
        self.visited = False
        self.neighbours = []

class board:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.size = 3

    def find_blank_tile(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def print_board(self, state):
        for row in state:
            print(row)
        print("----------")

    def get_possible_moves(self, state):
        moves = []
        x, y = self.find_blank_tile(state)
        directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        for move, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_state = [row[:] for row in state]  # Deep copy
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                moves.append((new_state, move))
        return moves

class game_algorithms:
    def __init__(self, board):
        self.board = board

    def goalTest(self, currentState):
        return currentState == self.board.goal_state

    def bfs(self):
        frontiers_queue = deque([(self.board.initial_state, [])])
        explored_set = set()
        while frontiers_queue:
            current_state, path = frontiers_queue.popleft()
            if self.goalTest(current_state):
                self.trace_game_board(path + [current_state])
                return path
            state_tuple = tuple(tuple(row) for row in current_state)
            if state_tuple not in explored_set:
                explored_set.add(state_tuple)
                for new_state, move in self.board.get_possible_moves(current_state):
                    new_path = path + [new_state]
                    frontiers_queue.append((new_state, new_path))
        return None
    def dfs(self):
        pass
    def ldfs(self):
        pass
    def a(self):
      pass
    def manhattan_distance(self):
        pass
    def euclidean_distance(self):
        pass

    def trace_game_board(self, path):
        print("Tracing steps to goal:")
        for state in path:
            self.board.print_board(state)
#main
initial_state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
board = board(initial_state)
board.print_board(board.initial_state)
game = game_algorithms(board)
solution_path = game.bfs()
