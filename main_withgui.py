import heapq
import random
import tkinter as tk
from collections import deque
import time
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

    def get_path_to_goal(self, node):
        path_to_goal = []
        while node:
            path_to_goal.append(node.state)
            node = node.parent
        return path_to_goal[::-1]  # Reverse to get the path from start to goal

    def goal_test(self, current_state):
        return current_state == self.board.goal_state

    def bfs(self):
        start_time = time.time()
        nodes_expanded = 0
        max_depth = 0
        frontiers_queue = deque([Node(self.board.initial_state)])
        explored_set = set()

        while frontiers_queue:
            current_node = frontiers_queue.popleft()
            nodes_expanded += 1
            max_depth = max(max_depth, current_node.depth)

            current_state_tuple = tuple(tuple(row) for row in current_node.state)
            if self.goal_test(current_node.state):
                path = self.get_path_to_goal(current_node)
                end_time = time.time()
                self.print_goal_path(path)
                return {
                    "path_to_goal": path,
                    "cost_of_path": len(path) - 1,
                    "nodes_expanded": nodes_expanded,
                    "search_depth": max_depth,
                    "running_time": end_time - start_time
                }

            if current_state_tuple not in explored_set:
                explored_set.add(current_state_tuple)
                for new_neighbor_node in self.board.get_possible_moves(current_node):
                    frontiers_queue.append(new_neighbor_node)

        return None

    def dfs(self, max_depth=None):
        start_time = time.time()
        nodes_expanded = 0
        max_depth_reached = 0
        frontiers_stack = [Node(self.board.initial_state)]
        explored_set = set()

        while frontiers_stack:
            current_node = frontiers_stack.pop()
            nodes_expanded += 1
            max_depth_reached = max(max_depth_reached, current_node.depth)

            current_state_tuple = tuple(tuple(row) for row in current_node.state)
            if self.goal_test(current_node.state):
                path = self.get_path_to_goal(current_node)
                end_time = time.time()
                self.print_goal_path(path)

                return {
                    "path_to_goal": path,
                    "cost_of_path": len(path) - 1,
                    "nodes_expanded": nodes_expanded,
                    "search_depth": max_depth_reached,
                    "running_time": end_time - start_time
                }

            if current_state_tuple not in explored_set:
                explored_set.add(current_state_tuple)
                if max_depth is None or current_node.depth < max_depth:
                    for new_neighbor_node in self.board.get_possible_moves(current_node):
                        frontiers_stack.append(new_neighbor_node)

        return None

    def idfs(self, max_depth):
        for depth_limit in range(max_depth + 1):
            solution_path_idfs = self.dfs(max_depth=depth_limit)
            if solution_path_idfs:
                return solution_path_idfs
        return None
    
    def manhattan_distance(self, state):
        distance = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                value = state[i][j]
                if value != 0:
                    goal_x, goal_y = divmod(value, self.board.size)
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance

    def euclidean_distance(self, state):
        distance = 0
        for i in range(self.board.size):
            for j in range(self.board.size):
                value = state[i][j]
                if value != 0:
                    goal_x, goal_y = divmod(value, self.board.size)
                    distance += ((i - goal_x) ** 2 + (j - goal_y) ** 2) ** 0.5
        return distance



 
    def a_star(self, heuristic='manhattan'):
        start_time = time.time()
        nodes_expanded = 0
        max_depth = 0
        frontiers_queue = []
        initial_node = Node(self.board.initial_state)
        initial_distance = (self.manhattan_distance(initial_node.state) if heuristic == 'manhattan' else self.euclidean_distance(initial_node.state))
        heapq.heappush(frontiers_queue, (initial_distance, 0, 0, initial_node))
        explored_set = set()
        index = 1  # Index to keep track of insertion order

        while frontiers_queue:
            f, g, _, current_node = heapq.heappop(frontiers_queue)
            nodes_expanded += 1
            max_depth = max(max_depth, current_node.depth)

            if self.goal_test(current_node.state):
                path = self.get_path_to_goal(current_node)
                end_time = time.time()
                self.print_goal_path(path)
                return {
                    "path_to_goal": path,
                    "cost_of_path": len(path) - 1,
                    "nodes_expanded": nodes_expanded,
                    "search_depth": max_depth,
                    "running_time": end_time - start_time
                }

            state_tuple = tuple(tuple(row) for row in current_node.state)
            if state_tuple not in explored_set:
                explored_set.add(state_tuple)

                for new_node in self.board.get_possible_moves(current_node):
                    new_g = g + 1
                    h = (self.manhattan_distance(new_node.state) if heuristic == 'manhattan' else self.euclidean_distance(new_node.state))
                    new_f = new_g + h
                    heapq.heappush(frontiers_queue, (new_f, new_g, index, new_node))
                    index += 1

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

class GUI:
    def show_popup(self,text):
        popup = tk.Toplevel(self.root)
        popup.title("Report")
        popup.geometry("300x150")  # Set size for the pop-up window

        # Add a label with the desired text
        label = tk.Label(popup, text=text, font=("Helvetica", 12))
        label.pack(pady=20)

        # Add a close button to the pop-up window
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def on_selection(self, selected_value):
        print(selected_value)
        self.solving_method = self.solving_methods[selected_value]
        self.option=selected_value

    def get_max_depth(self):
        max_depth = self.max_depth_entry.get()
        return int(max_depth) if max_depth.isdigit() else None

    def __init__(self, board, game):
        self.board = board
        self.game = game
        self.solving_method = self.game.bfs
        self.option='BFS'
        self.max_depth=0
        self.root = tk.Tk()
        self.root.title("8-Puzzle AI Lab1")
        self.root.geometry("400x500")
        self.root.config(bg="#111111")

        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.options = ["BFS", "DFS", "IDFS", "Manhattan", "Eucledian"]

        self.solving_methods={
            "BFS":self.game.bfs,
            "DFS":self.game.dfs,
            "IDFS":self.game.idfs,
            "Manhattan":self.game.a_star,
            "Eucledian":self.game.a_star
        }


        default_option = tk.StringVar()
        default_option.set(self.options[0])
        dropdown = tk.OptionMenu(self.root, default_option, *self.options, command=self.on_selection)
        dropdown.config(width=20, bg="#00796b", fg="white", font=("Helvetica", 14), relief="raised",justify='center')
        dropdown.grid(row=4, column=0, columnspan=3, pady=10, sticky="ew")
        self.max_depth_entry = tk.Entry(self.root, font=("Helvetica", 12), width=10)
        self.max_depth_entry.insert(0,"Enter max depth for idfs")
        self.max_depth_entry.grid(row=6, column=0,columnspan=3, pady=10, sticky="ew")

        solve_button = tk.Button(self.root, text="Solve", command=self.solve, bg="#00796b", fg="black", font=("Helvetica", 14), width=20)
        solve_button.grid(row=5, column=0, columnspan=3, pady=10, sticky="ew")

        self.tile_colors = {
            0: "#607d8b",
            "normal": "#a7c7e7",  # Pastel blue color for other tiles
        }

        self.tiles = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                num = self.board.initial_state[i][j]
                tile_text = str(num)
                tile_color = self.tile_colors[0] if num == 0 else self.tile_colors["normal"]
                tile = tk.Label(self.root, text=tile_text, font=("Helvetica", 24), width=5, height=2,
                                bg=tile_color, fg="#333333", borderwidth=2, relief="solid")
                tile.grid(row=i, column=j, sticky="nsew")
                self.tiles[i][j] = tile

    def update_board(self, state):
        for i in range(3):
            for j in range(3):
                num = state[i][j]
                tile_text = str(num) 
                tile_color = self.tile_colors[0] if num == 0 else self.tile_colors["normal"]
                self.tiles[i][j].config(text=tile_text, bg=tile_color)

    def solve(self):
        self.update_board(self.board.initial_state)
        if (self.option=="IDFS"):
            print("solving with idfs")
            depth=self.get_max_depth()
            result = self.solving_method(depth)
            solution_path=result['path_to_goal']
        elif(self.option=="Manhatten"):
            result = self.solving_method('manhattan')
            solution_path=result['path_to_goal']
        elif(self.option=="Eucledian"):
            result = self.solving_method('manhattan')
            solution_path=result['path_to_goal']
        else:
            result = self.solving_method()
            solution_path=result['path_to_goal']
        if solution_path:
            for state in solution_path:
                self.update_board(state)
                self.root.update()
                time.sleep(0.01)
            self.show_popup(f"cost of path={result['cost_of_path']}\nexpanded nodes={result['nodes_expanded']}\nsearch depth={result['search_depth']}\ntime={result['running_time']}\n")
        else:
            print("No solution found")

    def run(self):
        self.root.mainloop()

def generate_random_initial_state():
    numbers=get_random_numbers()
    state=[numbers[i:i+3]for i in range(0,9,3)]
    return state

def get_random_numbers():
    numbers = list(range(9))
    random.shuffle(numbers)
    return numbers


def main():
    # initial_state = generate_random_initial_state()
    initial_state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
    root_node = Node(initial_state)
    board = Board(root_node)
    game = GameAlgorithms(board)
    app = GUI(board, game)
    app.run()

if __name__ == "__main__":
    main()
