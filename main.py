from collections import deque
import tkinter as tk
import time

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

    def get_possible_moves(self, state):
        moves = []
        x, y = self.find_blank_tile(state)
        directions = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}
        for move, (dx, dy) in directions.items():
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_state = [row[:] for row in state]
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
                return path + [current_state]
            state_tuple = tuple(tuple(row) for row in current_state)
            if state_tuple not in explored_set:
                explored_set.add(state_tuple)
                for new_state, move in self.board.get_possible_moves(current_state):
                    new_path = path + [new_state]
                    frontiers_queue.append((new_state, new_path))
        return None


class PuzzleGUI:
    def __init__(self, initial_state):
        self.board = board(initial_state)
        self.game = game_algorithms(self.board)
        self.root = tk.Tk()
        self.root.title("8-Puzzle Solver")
        self.tiles = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

        # Solve Button
        solve_button = tk.Button(self.root, text="Solve with BFS", command=self.solve_puzzle)
        solve_button.grid(row=4, column=0, columnspan=3, pady=10)

    def create_board(self):
        for i in range(3):
            for j in range(3):
                tile_value = self.board.initial_state[i][j]
                tile_text = str(tile_value) if tile_value != 0 else ""
                tile = tk.Label(self.root, text=tile_text, font=("Helvetica", 24), width=4, height=2, borderwidth=2,
                                relief="solid")
                tile.grid(row=i, column=j)
                self.tiles[i][j] = tile

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                tile_value = state[i][j]
                self.tiles[i][j].config(text=str(tile_value) if tile_value != 0 else "")

    def solve_puzzle(self):
        solution_path = self.game.bfs()
        if solution_path:
            for state in solution_path:
                self.update_board(state)
                self.root.update()
                time.sleep(0.5)
        else:
            print("No solution found")

    def run(self):
        self.root.mainloop()


# Initial state for the puzzle
initial_state = [[1, 4, 2], [6, 5, 8], [7, 3, 0]]

# Run the GUI
app = PuzzleGUI(initial_state)
app.run()
