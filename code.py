import random

class Game:
    def __init__(self):
        self.board = [[" " , " " , " "] , [" " , " " , " "] , [" " , " " , " "]]
        self.player = "O"
        self.robot = "X"
        self.turn = None

    # Display board
    def show_board(self):
        col_width = max(len(str(x)) for row in self.board for x in row)
        top = "┌" + "┬".join("─"*(col_width+2) for _ in self.board[0]) + "┐"
        middle = "├" + "┼".join("─"*(col_width+2) for _ in self.board[0]) + "┤"
        bottom = "└" + "┴".join("─"*(col_width+2) for _ in self.board[0]) + "┘"

        print(top)
        for i, row in enumerate(self.board):
            print("│ " + " │ ".join(str(x).ljust(col_width) for x in row) + " │")
            if i < 2:
                print(middle)
        print(bottom)

    # Player move
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

            # Correct empty check
            if self.board[row][col] != " ":
                print("That block is already taken. Try another.")
                continue

            self.board[row][col] = self.player
            return
    def easy_mode(self): # Powered by TMC 1.0 Lite
        """AI model for the easy level of the game"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = self.robot
                    return
    
    def inter_mode(self): # Powered by TMC 1.0 I (Under development)
        """The AI model for the intermediate level of the game. turn : X or O, is necessery for it to work"""
        move = self.one_move_win(self.turn)
        if move:
            r, c = move
            self.board[r][c] = self.turn
            return
    
    def hard_mode(self): # Powered by TMC 1.0 Pro (Under development)
        """The AI model for the hard level of the game"""
        pass
    
    def impossible_mode(self): # The most powerful model powered by TMC 1.0 Max (Under development)
        """The AI model for impoossible level of the game"""
        pass

    # Robot move (Powered by "TMC 1.0")
    def next_move(self , difficulty):
        """Puts together all of the algorithms and run one of them when needed. the parameter turn is needed (X or O)"""
        if self.difficulty == 1 :
            self.easy_mode()
        elif difficulty == 2:
            self.inter_mode()
        elif difficulty == 3: 
            self.hard_mode()
        elif difficulty == 4: 
            self.impossible_mode()
        

    # Winner check
    def check_winner(self):
        """Checks if one side has won (Returns X if X is won and O if O is won) and None if
        no side won"""
        lines = (
            self.board +
            [list(col) for col in zip(*self.board)] +
            [[self.board[i][i] for i in range(3)]] +
            [[self.board[i][2 - i] for i in range(3)]]
        )

        # Winner detection
        for line in lines:
            if line[0] in ("X", "O") and line.count(line[0]) == 3:
                return line[0]

        if all(cell != " " for row in self.board for cell in row):
            return "Tie"

        return None

    # Game Evaluator
    def game_eval(self):
        """Evaluates the game and returns 1 if X has won or can win in only one move and it is his turn 
        (and O can't do anything about it) and -1, if this is happening with O and 0 if the game is ongoing and
        none of the conditions are true."""
        winner = self.check_winner()
        if winner == "X":
            return 1
        if winner == "O":
            return -1
        if winner == "Tie" or winner is None:
            return 0

        lines = (
            self.board +
            [list(col) for col in zip(*self.board)] +
            [[self.board[i][i] for i in range(3)]] +
            [[self.board[i][2-i] for i in range(3)]]
        )

        for line in lines:
            if line.count("X") == 2 and line.count(" ") == 1 and self.turn == "X":
                return 1
            if line.count("O") == 2 and line.count(" ") == 1 and self.turn == "O":
                return -1
        # if none worked :
        return 0
     
    def one_move_win(self, symbol):
        """Returns a tuple in which the first index is the row and the second index is the column where
        if you mark you will instantly win and if there is no move which win instantly it will return None"""
        # Try every empty cell
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = symbol
                    if self.check_winner() == symbol:
                        self.board[i][j] = " "
                        return (i, j)
                    self.board[i][j] = " "
        return None

        
    # Main Game Loop
    def play(self):
        """This function puts all of the other functions together and makes the game alive"""
        # Choose the player's and robot's symbol randomly
        self.player = random.choice(["X" , "O"])
        self.robot = "X" if self.player == "O" else "O"
        # Inform the player about their symbol and if they start the game
        print(f"You are playing as '{self.player}'")
        if self.player == "O":
            print("Your opponent starts the game...")

        # Take the difficulty level from the user and call the correct function
        # We will know which difficulty is the player intrested in playing after this part
        while True: 
            try:
                difficulty = int(input("Choose a difficulty (1:Easy-2:Intermediate-3:Hard-4:Impossible): "))
                if difficulty in (1 , 2 , 3 , 4): 
                    self.difficulty = difficulty
                    break
                else: 
                    print("")
            except ValueError:
                print("Something was wrong about your input's value. Note that only integer from 1 to 4 is allowed and Please try again")
        
        # showing the user the initial board
        self.show_board()
        
        """Define the initial game status to None (It can be changed to the winner's symbol later with
        the output of the function check winner or it can be "Tie")"""
        status = None

        # Game's main loop
        if self.player == "X":
            while status == None:
                # Player turn
                self.turn = "X"
                self.choice_maker()
                self.show_board()
                status = self.check_winner()
                if status:
                    break

                # Robot turn
                print("Robot's turn:")
                self.turn = "O"
                self.next_move(difficulty)
                self.show_board()
                status = self.check_winner()

        # If the player's symbol is O
        else:
            print("Robot starts the game!")
            while status is None:
                # Robot goes first
                print("Robot's turn:")
                self.turn = "X"
                self.next_move(difficulty)
                self.show_board()
                status = self.check_winner()
                if status:
                    break

                # Player turn
                self.turn = "O"
                self.choice_maker()
                self.show_board()
                status = self.check_winner()

    # End game output
        if status == "Tie":
            print("It's a tie!")
        else:
            print(f"The winner is: {status}")

# Run game
if __name__ == "__main__":
    Game().play()