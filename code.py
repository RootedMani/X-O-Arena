import random

class Game:
    def __init__(self):
        self.board = [[1,2,3],[4,5,6],[7,8,9]]
        self.player = None
        self.robot = None

    # ---------------- Display Board --------------------
    def show_board(self):
        col_width = max(len(str(x)) for row in self.board for x in row)
        top = "┌" + "┬".join("─"*(col_width+2) for _ in self.board[0]) + "┐"
        middle = "├" + "┼".join("─"*(col_width+2) for _ in self.board[0]) + "┤"
        bottom = "└" + "┴".join("─"*(col_width+2) for _ in self.board[0]) + "┘"
        
        print(top)
        for i, row in enumerate(self.board):
            print("│ " + " │ ".join(str(x).ljust(col_width) for x in row) + " │")
            if i < len(self.board) - 1:
                print(middle)
        print(bottom)

    # ---------------- Player Move --------------------
    def choice_maker(self):
        while True:
            try:
                choice = int(input("Enter the block you want to place your move in (1-9): "))
            except ValueError:
                print("Please enter a valid integer.")
                continue

            if not 1 <= choice <= 9:
                print("Choose a number between 1 and 9.")
                continue

            row = (choice - 1) // 3
            col = (choice - 1) % 3

            if isinstance(self.board[row][col], str):
                print("That block is already taken. Try another.")
                continue

            self.board[row][col] = self.player
            return

    # ---------------- Robot Move --------------------
    def next_move(self):
        """Very basic AI"""
        for i in range(3):
            for j in range(3):
                if not isinstance(self.board[i][j], str):
                    self.board[i][j] = self.robot
                    return

    # ---------------- Winner Check --------------------
    def check_winner(self):
        lines = (
            self.board +
            [list(col) for col in zip(*self.board)] +   # columns
            [[self.board[i][i] for i in range(3)]] +    # main diagonal
            [[self.board[i][2 - i] for i in range(3)]]  # other diagonal
        )

        for line in lines:
            if line.count(line[0]) == 3 and isinstance(line[0], str):
                return line[0]

        if all(isinstance(cell, str) for row in self.board for cell in row):
            return "Tie"

        return None

    # ---------------- Main Game Loop --------------------
    def play(self):
        self.player = random.choice(["O", "X"])
        self.robot = "X" if self.player == "O" else "O"

        print(f"You are playing as '{self.player}'")
        if self.player == "O":
            print("Your opponent starts the game...")

        self.show_board()
        status = None

        while status is None:
            # Player move
            self.choice_maker()
            self.show_board()
            status = self.check_winner()
            if status:
                break

            # Robot move
            print("Robot's turn:")
            self.next_move()
            self.show_board()
            status = self.check_winner()

        if status == "Tie":
            print("It's a tie!")
        else:
            print(f"The winner is: {status}")

# In this part the game runs if the program is being run directly
if __name__ == "__main__":
    Game().play()