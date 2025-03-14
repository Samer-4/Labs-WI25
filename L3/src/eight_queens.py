import pygame
from pygame.surface import Surface
import sys
from typing import List, Tuple

# define constants
BOARD_SIZE = 8
SQUARE_SIZE = 75  # This sets the size of the chessboard squares
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)


def draw_board(screen: Surface, board_size: int = BOARD_SIZE, square_size: int = SQUARE_SIZE):
    """
    Draw the chessboard.

    Args:
        screen: Surface: pygame screen
        board_size (int, optional): board_size in number of box. Defaults to BOARD_SIZE.
        square_size (int, optional): square_size in number of box. Defaults to SQUARE_SIZE.
    """
    for row in range(board_size):
        for col in range(board_size):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))


def place_queens(screen: Surface, queen_positions: List[Tuple[int, int]]):
    """
    Place queens on the board based on the given positions.

    Args:
        queen_positions: List of tuples, each tuple is (row, col) for a queen's position
    """
    for pos in queen_positions:
        pygame.draw.circle(screen, GREEN, (pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2, pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 3)


def is_safe_row_diag(board, row, col) -> bool:
    """
    Check if it's safe to place a queen at board[row][col].
    This checks the row, upper diagonal, and lower diagonal.

    Args:
        board: 2D list of int
        row: int
        col: int

    Returns:
        bool: True if it's safe, False otherwise
    """
    # Check the row on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check the upper diagonal on the left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == 1:
            return False

    # Check the lower diagonal on the left side
    for i, j in zip(range(row, BOARD_SIZE), range(col, -1, -1)):
        if 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE and board[i][j] == 1:
            return False

    return True


def solve_8_queens(board: List[List[int]], col: int) -> bool:
    """
    Solve the 8 queens problem using backtracking.

    Args:
        board (List[List[int]]): 2D list of int, representing the chessboard
        col (int): int, the column to place the queen

    Returns:
        bool: whether the solution exists
    """
    # Base case: All queens are placed
    if col >= BOARD_SIZE:
        return True

    # Try placing a queen in each row of the current column
    for row in range(BOARD_SIZE):
        if is_safe_row_diag(board, row, col):
            # Place the queen
            board[row][col] = 1

            # Recur to place the rest of the queens
            if solve_8_queens(board, col + 1):
                return True

            # Backtrack if placing the queen doesn't lead to a solution
            board[row][col] = 0

    # If no position is safe, return False
    return False


def update_board():
    """
    Creates the board and returns the list of valid queen positions.

    Returns:
        List[Tuple[int, int]]: List of queen positions
    """
    # Initialize the board
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]

    # Attempt to solve the problem and check for solvability
    if not solve_8_queens(board, 0):
        return []  # Return empty list if no solution exists

    # Convert the board to a list of queen positions
    queen_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == 1]

    return queen_positions


def main():
    """
    Main function to initialize the pygame window and visualize the solution.
    """
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("8 Queens Puzzle")

    # Get the queen positions
    queen_positions = update_board()

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw the board and queens
        draw_board(screen)
        if queen_positions:
            place_queens(screen, queen_positions)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

