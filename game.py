#!/usr/bin/env python3

import random
import time
from moves import *
from ia_dama import ia_turn
import functools


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer()

# starting board
def start_board(board):
    for c in range(SIZE):
        for r in range(3):
            if c % 2 == 0 and r % 2 == 0:
                board[r][c] = BLACK
            elif c % 2 != 0 and r % 2 != 0:
                    board[r][c] = BLACK

        for r in range(5, SIZE):
            if c % 2 == 0 and r % 2 == 0:
                board[r][c] = WHITE
            elif c % 2 != 0 and r % 2 != 0:
                    board[r][c] = WHITE

def end_game(end, draw, color):
    winner = "Whites"
    if color == BLACK:
        winner = "Blacks"

    if end:
        print(winner + " win!")
        return True
    if draw == 40:
        print("Draw!")
        return True

    return False

@timer
def main():
    # initialize the board
    board = [[EMPTY for c in range(SIZE)] for r in range(SIZE)]

    start_board(board)
    print_board(board)

    # game loop
    while True:
        # end = human_turn(WHITE, board)
        # if end:
        #     print("Whites win!")
        #     break

        end = ia_turn(WHITE, board)
        # if end_game(end, draw, WHITE):
        #     break
        if end:
            print("Whites win!")
            break
        # time.sleep(2)
        end = ia_turn(BLACK, board)
        # if end_game(end, draw, BLACK):
        #     break
        if end:
            print("Blacks win!")
            break
        # time.sleep(2)

if __name__ == "__main__":
    main()
