import random
from math import inf

class Game:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player = None
        self.robot = None
        self.turn = None
        self.difficulty = None

    # Display board
    def show_board(self):
        col_width = 1
        top = "┌" + "┬".join("─"*(col_width+2) for _ in range(3)) + "┐"
        middle = "├" + "┼".join("─"*(col_width+2) for _ in range(3)) + "┤"
        bottom = "└" + "┴".join("─"*(col_width+2) for _ in range(3)) + "┘"

        ref = [["1","2","3"],["4","5","6"],["7","8","9"]]

        print("Current Board:".ljust(30) + "Reference Board:")
        print(top.ljust(30) + top)

        for i in range(3):
            left = "│ " + " │ ".join(self.board[i]) + " │"
            right = "│ " + " │ ".join(ref[i]) + " │"
            print(left.ljust(30) + right)
            if i < 2:
                print(middle.ljust(30) + middle)

        print(bottom.ljust(30) + bottom)

    # Lines helper
    def get_lines(self):
        return (
            self.board +
            [list(col) for col in zip(*self.board)] +
            [[self.board[i][i] for i in range(3)]] +
            [[self.board[i][2-i] for i in range(3)]]
        )

    # Player move
    def choice_maker(self):
        while True:
            try:
                choice = int(input("Enter a block (1-9): "))
            except ValueError:
                print("Invalid input.")
                continue

            if not 1 <= choice <= 9:
                print("Choose 1-9.")
                continue

            row = (choice - 1) // 3
            col = (choice - 1) % 3

            if self.board[row][col] != " ":
                print("That block is taken.")
                continue

            self.board[row][col] = self.player
            return

    # Evaluate winner
    def check_winner(self):
        for line in self.get_lines():
            if line[0] in ("X","O") and line.count(line[0]) == 3:
                return line[0]
        if all(cell != " " for row in self.board for cell in row):
            return "Tie"
        return None

    # Minimax evaluation scoring
    def evaluate_board(self):
        winner = self.check_winner()
        if winner == self.robot:
            return +10
        if winner == self.player:
            return -10
        return 0

    # Get empty spots
    def get_moves(self):
        return [(r,c) for r in range(3) for c in range(3) if self.board[r][c] == " "]

    # Minimax
    def minimax(self, depth, is_maximizing):
        score = self.evaluate_board()
        if score != 0:
            return score - depth if score > 0 else score + depth

        if not self.get_moves():
            return 0

        if is_maximizing:
            best = -inf
            for r,c in self.get_moves():
                self.board[r][c] = self.robot
                best = max(best, self.minimax(depth+1, False))
                self.board[r][c] = " "
            return best

        else:
            best = 999
            for r,c in self.get_moves():
                self.board[r][c] = self.player
                best = min(best, self.minimax(depth+1, True))
                self.board[r][c] = " "
            return best

    # Easy mode
    def easy_mode(self):
        moves = self.get_moves()
        if moves:
            r,c = moves[0]
            self.board[r][c] = self.robot

    # One move win
    def one_move_win(self):
        for r,c in self.get_moves():
            self.board[r][c] = self.turn
            if self.check_winner() == self.turn:
                self.board[r][c] = " "
                return (r,c)
            self.board[r][c] = " "
        return None

    # Intermediate mode
    def inter_mode(self):
        move = self.one_move_win()
        if move:
            r,c = move
            self.board[r][c] = self.turn
            return

        opponent = "X" if self.turn == "O" else "O"
        lines = self.get_lines()
        line_coords = (
            [[(0,0),(0,1),(0,2)],[(1,0),(1,1),(1,2)],[(2,0),(2,1),(2,2)]] +
            [[(0,0),(1,0),(2,0)],[(0,1),(1,1),(2,1)],[(0,2),(1,2),(2,2)]] +
            [[(0,0),(1,1),(2,2)]] +
            [[(0,2),(1,1),(2,0)]]
        )

        for line,coords in zip(lines,line_coords):
            if line.count(opponent) == 2 and line.count(" ") == 1:
                idx = line.index(" ")
                r,c = coords[idx]
                self.board[r][c] = self.turn
                return

        self.easy_mode()

    # Hard = minimax with depth limit
    def hard_mode(self):
        best_score = -999
        best_move = None
        for r,c in self.get_moves():
            self.board[r][c] = self.robot
            score = self.minimax(0, False)
            self.board[r][c] = " "
            if score > best_score:
                best_score = score
                best_move = (r,c)
        if best_move:
            r,c = best_move
            self.board[r][c] = self.robot

    # Impossible full minimax
    def impossible_mode(self):
        best_score = -999
        best_move = None
        for r,c in self.get_moves():
            self.board[r][c] = self.robot
            score = self.minimax(0, False)
            self.board[r][c] = " "
            if score > best_score:
                best_score = score
                best_move = (r,c)
        if best_move:
            r,c = best_move
            self.board[r][c] = self.robot

    def next_move(self):
        if self.difficulty == 1:
            self.easy_mode()
        elif self.difficulty == 2:
            self.inter_mode()
        elif self.difficulty == 3:
            self.hard_mode()
        elif self.difficulty == 4:
            self.impossible_mode()

    # Main loop
    def play(self):
        self.player = random.choice(["X","O"])
        self.robot = "X" if self.player == "O" else "O"
        print(f"You are '{self.player}'")

        while True:
            try:
                diff = int(input("Choose difficulty (1-4): "))
                if diff in (1,2,3,4):
                    self.difficulty = diff
                    break
            except:
                pass

        self.show_board()
        status = None

        if self.player == "X":
            while status is None:
                self.turn = "X"
                self.choice_maker()
                self.show_board()
                status = self.check_winner()
                if status:
                    break
                print("Robot's turn:")
                self.turn = "O"
                self.next_move()
                self.show_board()
                status = self.check_winner()
        else:
            print("Robot starts:")
            while status is None:
                print("Robot's turn:")
                self.turn = "X"
                self.next_move()
                self.show_board()
                status = self.check_winner()
                if status:
                    break
                self.turn = "O"
                self.choice_maker()
                self.show_board()
                status = self.check_winner()

        if status == "Tie": print("It's a tie!")
        else: print(f"Winner: {status}")


if __name__ == "__main__":
    Game().play()