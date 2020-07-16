#!/usr/bin/env python3

import random
from moves import *
from ia_dama import ia_turn

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

def main():
    # initialize the board
    board = [[EMPTY for c in range(SIZE)] for r in range(SIZE)]

    start_board(board)
    print_board(board)

    # game loop
    while True:
        end = human_turn(WHITE, board)
        if end:
            print("Whites win!")
            break

        end = ia_turn(BLACK, board)
        if end:
            print("Blacks win!")
            break

if __name__ == "__main__":
    main()
