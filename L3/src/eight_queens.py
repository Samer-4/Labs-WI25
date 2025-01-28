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


def draw_board(screen: Surface, board_size: int = BOARD_SIZE, square_size: int = SQUARE_SIZE):
    for row in range(board_size):
        for col in range(board_size):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))


def place_queens(screen: Surface, queen_positions: List[Tuple[int, int]]):
    queen_image = pygame.image.load("queen.png")
    queen_image = pygame.transform.scale(queen_image, (SQUARE_SIZE, SQUARE_SIZE))
    for pos in queen_positions:
        screen.blit(queen_image, (pos[1] * SQUARE_SIZE, pos[0] * SQUARE_SIZE))


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
        if board[i][j] == 1:
            return False

    # Check the lower diagonal on the left side
    for i, j in zip(range(row, BOARD_SIZE), range(col, -1, -1)):
        if board[i][j] == 1:
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
    board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    if not solve_8_queens(board, 0):
        return []  # Return empty if no solution exists

    # Prepare the list of queen positions
    queen_positions = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 1:
                queen_positions.append((i, j))

    return queen_positions


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("8 Queens Puzzle")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_board(screen)
        queen_positions = update_board()
        place_queens(screen, queen_positions)
        pygame.display.update()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
