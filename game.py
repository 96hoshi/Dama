#!/usr/bin/env python3

import random
import time
import functools
from moves import *
from ia_dama import ia_turn

draw_white = 0
draw_black = 0

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

def increment_draw(color):
    global draw_white, draw_black

    if color == WHITE:
        draw_white += 1
        return draw_white
    else:
        draw_black += 1
        return draw_black

def reset_draw(color):
    global draw_white, draw_black

    if color == WHITE:
        draw_white = 0
    else:
        draw_black = 0

def game_over(eat_move, color, end):
    winner = "Whites"
    if color == BLACK:
        winner = "Blacks"

    if end:
        print(winner + " win!")
        return True
    if eat_move:
        reset_draw(color)
    else:
        draw_counter = increment_draw(color)
        if draw_counter == 40:
            print("Draw!")
            return True

    return False

def ask_color():
    while True:
        try:
            c = input("Choose your color:\033[91m w\033[0m / \033[94m b \033[0m\n").lower()
        except ValueError:
            print("Wrong input, correct usage: <string>")
            continue
        else:
            if c == "w" or c == "b":
                return c
            print("Wrong input, correct usage: w/b")
            continue

def is_player_first(c):
    if c == "w":
        # player choose white, first move to perform
        return True
    else:
        return False

@timer
def main():
    # initialize the board
    board = [[EMPTY for c in range(SIZE)] for r in range(SIZE)]

    start_board(board)
    print_board(board)

#     # ask color to the player
#     color = ask_color()

# # game main loop
#     if is_player_first(color):
#         while True:
#             e_m, c, end = human_turn(WHITE, board)
#             if game_over(e_m, WHITE, end):
#                 break

#             e_m, c, end = ia_turn(BLACK, board)
#             if game_over(e_m, c, end):
#                 break
#     else:
#         while True:
#             e_m, c, end = ia_turn(WHITE, board)
#             if game_over(e_m, c, end):
#                 break

#             e_m, c, end = human_turn(BLACK, board)
#             if game_over(e_m, BLACK, end):
#                 break

    # test loop
    # TO REMOVE
    while True:
        e_m, c, end = ia_turn(WHITE, board)
        if game_over(e_m, c, end):
            break

        e_m, c, end = ia_turn(BLACK, board)
        if game_over(e_m, c, end):
            break


if __name__ == "__main__":
    main()
