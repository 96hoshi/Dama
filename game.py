#!/usr/bin/env python3

import time
import functools
import argparse
from moves import *
from ia_dama import ia_turn
import numpy as np


draw_white = 0
draw_black = 0

white_times = []
black_times = []


def test_timer(func):

    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter_ns()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter_ns()  # 2
        run_time = end_time - start_time  # 3

        if args[1][0] == WHITE:
            white_times.append(run_time)
        else:
            black_times.append(run_time)
        return value
    return wrapper_timer


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
    if end:
        winner = "Whites"
        if color == BLACK:
            winner = "Blacks"
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

@test_timer
def execute_turn(fun, args):
    return fun(*args)


# @timer
def main():
    parser = argparse.ArgumentParser()

    parser = argparse.ArgumentParser(
        description='Play a dama game against another player, an ai or\
         let two ai play',
        epilog="Choose your game!")
    parser.add_argument("--white_depth", type=int, help="sets white ai depth")
    parser.add_argument("--black_depth", type=int, help="sets black ai depth")

    args = parser.parse_args()

    # initialize the board
    board = [[EMPTY for c in range(SIZE)] for r in range(SIZE)]

    start_board(board)
    print_board(board)

    if args.white_depth == 0 or args.white_depth:
        first_turn = ia_turn
        first_args = WHITE, args.white_depth, board
    else:
        first_turn = human_turn
        first_args = WHITE, board

    if args.black_depth == 0 or args.black_depth:
        second_turn = ia_turn
        second_args = BLACK, args.black_depth, board
    else:
        second_turn = human_turn
        second_args = BLACK, board

    # min game loop
    while True:
        eat_m, c, end = execute_turn(first_turn, first_args)
        if game_over(eat_m, c, end):
            break

        eat_m, c, end = execute_turn(second_turn, second_args)
        if game_over(eat_m, c, end):
            break

    # stats
    w_avg = np.average(white_times)
    b_avg = np.average(black_times)
    w_max = np.max(white_times)
    b_max = np.max(black_times)
    w_min = np.min(white_times)
    b_min = np.min(black_times)
    time = sum(white_times) + sum(black_times)

    if draw_white == 40 or draw_black == 40:
        w_res = "Draw"
        b_res = "Draw"
        res = "DRAW"
    elif c == WHITE:
        w_res = "Win"
        b_res = "Lose"
        res = "WHITE"
    else:
        w_res = "Lose"
        b_res = "Win"
        res = "BLACK"

    # print("COLOR AVG_TIME MAX_TIME MIN_TIME DEPTH RESULT")
    # print("DEPTH_W DEPTH_B TIME RESULT")
    with open('tests01.txt', 'a') as f:
        f.write("WHITE {:.3f} {} {} {} {}\n".format(w_avg, w_max, w_min,
            args.white_depth, w_res))
        f.write("BLACK {:.3f} {} {} {} {}\n".format(b_avg, b_max, b_min,
            args.black_depth, b_res))
        f.write("GAME {} {} {} {}\n".format(args.white_depth,
            args.black_depth, time, res))

if __name__ == "__main__":
    main()
