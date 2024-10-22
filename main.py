from collections import deque
# deque provides an O(1) time complexity for append and pop operations
# as compared to a list that provides O(n) time complexity.
class board:
    def __init__(self,initial_state):
        self.initial_state=initial_state
        self.current_state=initial_state
        self.goal_state=[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.size=3

    def print_board(self):
        for row in self.current_state:
            print(row)
        print("----------")

    def make_move(self):
        pass

    def is_goal_achieved(self):
        return self.current_state==self.goal_state

class game_algorithms:
    def __init__(self,board):
        self.board=board

    def bfs(self):
        frontiers_queue=deque([self.board.initial_state])
        explored_set=set()
        path={}
        while frontiers_queue:
            current_state=frontiers_queue.popleft()
            if current_state not in explored_set:
                explored_set.add(current_state)
            if current_state==self.board.goal_state:
                return path

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

    def trace_game_board(self):
        pass
    #trace the board and print it with every update


initial_state = [[1, 2, 5], [3, 4, 0], [6, 7, 8]]
board = board(initial_state)
board.print_board()
