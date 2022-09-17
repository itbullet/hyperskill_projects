import random
import time


class TicTacToeGame:
    def __init__(self, board_state=None):
        if board_state is None:
            board_state = "_________"
        self.board_state = list(board_state)
        self.game_state = 0
        self.mode = ["user", "easy", "medium", "hard"]
        self.menu = ["start", "exit"]
        self.parameter = ""
        self.users = []
        self.range = [1, 2, 3]
        self.depth = 0
        # player and opponent variable were introduced for minimax function where user1's opponent is user2 and vice versa
        self.player = ""
        self.opponent = ""
        self.board_rows = {"row1": {0: None, 1: None, 2: None},
                           "row2": {3: None, 4: None, 5: None},
                           "row3": {6: None, 7: None, 8: None},
                           "column1": {0: None, 3: None, 6: None},
                           "column2": {1: None, 4: None, 7: None},
                           "column3": {2: None, 5: None, 8: None},
                           "diagonal1": {0: None, 4: None, 8: None},
                           "diagonal2": {2: None, 4: None, 6: None}}

    def game_state_analysis(self):
        tictactoe_matrix = [list(self.board_state[i:i + 3]) for i in range(0, len(self.board_state), 3)]
        tictactoe_matrix_columns = [[self.board_state[j] for j in range(i, len(self.board_state), 3)] for i in range(3)]
        x_win, o_win, empty_cell = 0, 0, 0
        diagonal1, diagonal2 = [], []
        # checking rows
        for row in tictactoe_matrix:
            if row.count("X") == 3:
                x_win = 1
            elif row.count("O") == 3:
                o_win = 1
            elif row.count("_"):
                empty_cell = 1
        # checking columns
        for row in tictactoe_matrix_columns:
            if row.count("X") == 3:
                x_win = 1
            elif row.count("O") == 3:
                o_win = 1
            elif row.count("_"):
                empty_cell = 1
        # checking diagonals
        for i, elem in enumerate(tictactoe_matrix):
            diagonal1.append(elem[i])
            diagonal2.append(elem[-(i + 1)])

        if diagonal1.count("X") == 3 or diagonal2.count("X") == 3:
            x_win = 1
        elif diagonal1.count("O") == 3 or diagonal2.count("O") == 3:
            o_win = 1

        if x_win and not o_win:
            return f"X wins"
        elif o_win and not x_win:
            return f"O wins"
        elif not x_win and not o_win and not empty_cell:
            return f"Draw"

    def game_state_analysis_minimax(self, order):
        tictactoe_matrix = [list(self.board_state[i:i + 3]) for i in range(0, len(self.board_state), 3)]
        tictactoe_matrix_columns = [[self.board_state[j] for j in range(i, len(self.board_state), 3)] for i in range(3)]
        x_win, o_win, empty_cell = 0, 0, 0
        diagonal1, diagonal2 = [], []
        # checking rows
        for row in tictactoe_matrix:
            if row.count(order) == 3:
                return True
        for row in tictactoe_matrix_columns:
            if row.count(order) == 3:
                return True
        for i, elem in enumerate(tictactoe_matrix):
            diagonal1.append(elem[i])
            diagonal2.append(elem[-(i + 1)])

        if diagonal1.count(order) == 3 or diagonal2.count(order) == 3:
            return True

        return False

    def draw_field(self, print_answer=1):
        print("---------")
        for i, elem in enumerate(self.board_state):
            if not i % 3:
                print(f"| {elem}", end="")
            elif (i + 1) % 3:
                print(f" {elem}", end="")
            else:
                print(f" {elem} |")
        print("---------")

        if self.game_state_analysis() and print_answer:
            print(self.game_state_analysis())
            # reset board
            self.board_state = list("_________")
            return 0
        else:
            return 1

    def order(self):
        if self.board_state.count('X') == self.board_state.count("O"):
            return "X"
        return "O"

    def next_order(self):
        if self.board_state.count('X') == self.board_state.count("O"):
            return "O"
        return "X"

    def ai_move_easy(self, level="easy"):
        # time.sleep(2)
        free_indexes = [i for i, el in enumerate(self.board_state) if el == "_"]
        ai_coordinates_cell = random.choice(free_indexes)
        print(f"Making move level \"{level}\"")
        return ai_coordinates_cell

    def ai_move_medium(self, level="medium"):
        # time.sleep(2)
        for key, value in self.board_rows.items():
            for k, v in value.items():
                value[k] = self.board_state[k]
        # attack
        order = self.order()
        for key, value in self.board_rows.items():
            count = 0
            for k, v in value.items():
                if v == order:
                    count += 1
            if count == 2:
                for k, v in value.items():
                    if v == "_":
                        print(f"Making move level \"{level}\"")
                        return k
        # defend
        next_order = self.next_order()
        for key, value in self.board_rows.items():
            count = 0
            for k, v in value.items():
                if v == next_order:
                    count += 1
            if count == 2:
                for k, v in value.items():
                    if v == "_":
                        print(f"Making move level \"{level}\"")
                        return k
        return self.ai_move_easy(level="medium")

    # This is the minimax function. It considers all the possible ways the game can go and returns the value of the board
    def minimax(self, depth, is_max):
        # If Maximizer has won the game return his/her evaluated score
        if self.game_state_analysis_minimax(self.player):
            # self.depth = depth
            return 10 - depth
        # If Minimizer has won the game return his evaluated score
        elif self.game_state_analysis_minimax(self.opponent):
            # self.depth = depth
            return -10 + depth
        # If there are no more moves and no winner then it is a tie
        elif self.game_state_analysis() == "Draw":
            # self.depth = depth
            return 0
        # If this maximizer's move
        if is_max:
            best_value = -1000
            # Traverse all cells
            for i, el in enumerate(self.board_state):
                # Check if cell is empty
                if el == "_":
                    # Make the move
                    self.board_state[i] = self.player
                    # Call minimax recursively and choose the maximum value
                    best_value = max(best_value, self.minimax(depth + 1, not is_max))
                    # Undo the move
                    self.board_state[i] = "_"
            return best_value
        # If this minimizer's move
        else:
            best_value = 1000
            # Traverse all cells
            for i, el in enumerate(self.board_state):
                # Check if cell is empty
                if el == "_":
                    # Make the move
                    self.board_state[i] = self.opponent
                    # Call minimax recursively and choose the maximum value
                    best_value = min(best_value, self.minimax(depth + 1, not is_max))
                    # Undo the move
                    self.board_state[i] = "_"
            return best_value

    # This will return the best possible move for the player
    def ai_move_hard(self, level="hard"):
        best_value = -1000
        best_move = 0
        best_depth = 0
        self.player = self.order()
        self.opponent = self.next_order()
        # Traverse all cells, evaluate minimax function for all empty cells. And return the cell with optimal value.
        for i, el in enumerate(self.board_state):
            # Check if cell is empty
            if el == "_":
                # Make the move
                self.board_state[i] = self.order()
                # compute evaluation function for this move.
                current_value = self.minimax(0, False)
                # Undo the move
                self.board_state[i] = "_"
                # If the value of the current move is more than the best value, then update best
                if current_value > best_value:
                    best_value = current_value
                    best_depth = self.depth
                    best_move = i
        # print(f"depth is {best_depth}")
        print(f"Making move level \"{level}\"")
        return best_move

    def player_move(self):
        while True:
            try:
                user_coordinates_row, user_coordinates_column = input("Enter the coordinates: ").split()
                user_coordinates_row = int(user_coordinates_row)
                user_coordinates_column = int(user_coordinates_column)
            except ValueError:
                print("You should enter numbers!")
                continue

            if user_coordinates_row not in self.range or user_coordinates_column not in self.range:
                print("Coordinates should be from 1 to 3!")
                continue

            if user_coordinates_row == 1:
                cell_state = self.cell_analysis(self.board_state[user_coordinates_column - 1])
                if not cell_state:
                    index = user_coordinates_row * (user_coordinates_column - 1)
                    return index
                else:
                    continue
            else:
                cell_state = self.cell_analysis(self.board_state[(user_coordinates_row - 1) * 3 + user_coordinates_column - 1])
                if not cell_state:
                    index = (user_coordinates_row - 1) * 3 + user_coordinates_column - 1
                    return index
                else:
                    continue

    @staticmethod
    def cell_analysis(cell, print_answer=1):
        if cell == "_":
            _state = 0
        else:
            if print_answer:
                print("This cell is occupied! Choose another one!")
            _state = 1
        return _state

    def game_menu(self):
        while True:
            self.parameter, *self.users = input("Input command: ").split()
            if self.parameter.lower() == "exit":
                return False
            elif (self.parameter.lower() not in self.menu) or (self.parameter.lower() == "exit" and len(self.users) != 0):
                print("Bad parameters!")
                continue
            elif (len(self.users) != 2) or not all(user in self.mode for user in self.users):
                print("Bad parameters!")
                continue
            elif self.parameter.lower() == "start":
                return True

    def game(self):
        self.game_state = self.draw_field(print_answer=0)
        user1, user2 = None, None
        if self.users[0] == "user":
            user1 = self.player_move
        elif self.users[0] == "easy":
            user1 = self.ai_move_easy
        elif self.users[0] == "medium":
            user1 = self.ai_move_medium
        elif self.users[0] == "hard":
            user1 = self.ai_move_hard

        if self.users[1] == "user":
            user2 = self.player_move
        elif self.users[1] == "easy":
            user2 = self.ai_move_easy
        elif self.users[1] == "medium":
            user2 = self.ai_move_medium
        elif self.users[1] == "hard":
            user2 = self.ai_move_hard

        while self.game_state:
            if self.order() == "X":
                self.board_state[user1()] = self.order()
            else:
                self.board_state[user2()] = self.order()

            self.game_state = self.draw_field()


def main():
    game = TicTacToeGame()
    while game.game_menu():
        game.game()


if __name__ == "__main__":
    main()
