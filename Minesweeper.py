import random

# Global variables
board = []
mines = []
size = 0
revealed_cells = []
flags_count = 0
processed_cells = []

def create_board(board_size, num_mines):
    """Initialize the game board and place mines."""
    global board, mines, size
    
    # Initialize the board with '#' representing unrevealed cells
    board = [['#' for _ in range(board_size)] for _ in range(board_size)]
    
    # Place mines randomly on the board
    mines = set()
    while len(mines) < num_mines:
        a = random.randint(0, board_size - 1)
        b = random.randint(0, board_size - 1)
        mines.add((a, b))
    
    size = board_size

def put_flag(row, col):
    """Place a flag on the cell at (row, col)."""
    global flags_count
    if (row, col) not in revealed_cells and board[row][col] != 'p':
        board[row][col] = 'p'
        flags_count += 1

def remove_flag(row, col):
    """Remove a flag from the cell at (row, col)."""
    if board[row][col] == 'p':
        board[row][col] = '#'
        global flags_count
        flags_count -= 1

def print_board(show_mines=False):
    """Print the current state of the board."""
    for i in range(size):
        for j in range(size):
            if (i, j) in revealed_cells:
                print(count_mines(i, j), end=" ")
            elif show_mines and (i, j) in mines:
                print("@", end=" ")
            else:
                print(board[i][j], end=" ")
        print()
    print()

def count_mines(row, col):
    """Count the number of mines around the cell at (row, col)."""
    if (row, col) in mines:
        return -1
    
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= row + i < size and 0 <= col + j < size:
                if (row + i, col + j) in mines:
                    count += 1
    return count

def reveal_cell(row, col):
    """Reveal the cell at (row, col)."""
    if (row, col) not in revealed_cells:
        revealed_cells.append((row, col))
        if count_mines(row, col) == 0:
            auto_reveal(row, col)

def auto_reveal(row, col):
    """Automatically reveal surrounding cells if the current cell has no adjacent mines."""
    if (row, col) in processed_cells:
        return
    processed_cells.append((row, col))
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_row, new_col = row + i, col + j
            if 0 <= new_row < size and 0 <= new_col < size and (new_row, new_col) not in revealed_cells:
                reveal_cell(new_row, new_col)

def won():
    """Check if the player has won the game."""
    return flags_count + len(revealed_cells) == size * size and flags_count == len(mines)

def main():
    """Main function to run the game loop."""
    board_size = int(input("Input the number of rows: "))
    num_mines = int(input("Input the number of mines: "))
    create_board(board_size, num_mines)
    
    while True:
        command = input("What do you want to do? (r i j: reveal, f i j: flag, u i j: unflag, x: exit): ").split()
        if command[0] == "x":
            print("Game Over!")
            break
        
        action, row, col = command[0], int(command[1]), int(command[2])
        if 0 <= row < size and 0 <= col < size:
            if action == "r":
                reveal_cell(row, col)
                if count_mines(row, col) == -1:
                    print("You hit a mine! Game Over!")
                    print_board(show_mines=True)
                    break
            elif action == "f":
                put_flag(row, col)
            elif action == "u":
                remove_flag(row, col)
            else:
                print("Invalid Command!")
            
            print_board()
            if won():
                print("Congratulations! You won!")
                print_board(show_mines=True)
                break
        else:
            print("Invalid cell coordinates!")

main()
