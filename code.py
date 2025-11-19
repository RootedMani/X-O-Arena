# Importing the library random
import random

# defining functions
def show_board(game_board): 
    """This function is used to show the current situation of the board"""
    col_width = max(len(str(x)) for row in game_board for x in row)

    top =    "┌" + "┬".join("─"*(col_width+2) for _ in game_board[0]) + "┐"
    middle = "├" + "┼".join("─"*(col_width+2) for _ in game_board[0]) + "┤"
    bottom = "└" + "┴".join("─"*(col_width+2) for _ in game_board[0]) + "┘"
    print(top)
    for i, row in enumerate(game_board):
        print("│ " + " │ ".join(str(x).ljust(col_width) for x in row) + " │")
        if i < len(game_board) - 1:
            print(middle)
    print(bottom)

def choice_maker(game_board, role):
    while True:
        try:
            choice = int(input("Enter the block you want to place your move in (1–9) : "))
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if not 1 <= choice <= 9:
            print("Choose a number between 1 and 9.")
            continue

        row = (choice - 1) // 3
        col = (choice - 1) % 3

        if isinstance(game_board[row][col], str):
            print("That block is already taken. Try another.")
            continue

        game_board[row][col] = role
        return  # success


def next_move(board , count , robot_role):
    """This function is the algorithm for the robot to choose a block to mark"""
    if robot_role == "X": 
        if count == 0: 
            board[0][0] = "X"
        if count == 2 : 
            if board[1][1] == "O": 
                board[0][2] = "X"
            if board[0][2] == "O":
                board[2][0] = "X"
    return board
def count(game_board):
    """It count how many X's and O's are on the board"""
    counter = 0 
    for row in game_board: 
        for item in row: 
            if item != "X" or item != "O": 
                counter += 1 
    return counter

def game(): 
    """This function will run the game"""
    roles = ["O" , "X"]
    game_status = None
    game_role = random.choice(roles)
    turn_counter = 0
    game_board = [
        [1 , 2 ,3], 
        [4 , 5 , 6], 
        [7 , 8 , 9]
    ]
    print(f"You are playing as '{game_role}'")
    if game_role == "X": 
         while game_status == None: 
            show_board(game_board)
            game_board = choice_maker(game_board , game_role)
            show_board(game_board)
            game_board = next_move(game_board , turn_counter , "X" if game_role == "O" else "O")
            show_board(game_board)

    if game_role == "O": 
        print("Your opponent is the one who starts the game ...")
        while game_status == None:
            game_board = next_move(game_board , turn_counter , "X" if game_role == "O" else "O")
            show_board(game_board)
            game_board = choice_maker(game_board, game_role)
            show_board(game_board)

print(game())
