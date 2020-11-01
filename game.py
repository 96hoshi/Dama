#!/usr/bin/env python3

import argparse
from moves import *
from ia_dama import ia_turn


draw_white = 0
draw_black = 0

white_times = []
black_times = []


# set the board with the initial configuration
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


# check if the game loop needs to stop
# it occur when a player wins or 40 moves without a eat move is performed.
# if an eat move is performed then reset the counter, else increment it
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


def execute_turn(fun, args):
    return fun(*args)


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

    # sets the turns
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
        # every turn returns if an eat move is performed, the actual color
        # and a flag that warn if there is a winner
        eat_m, c, end = execute_turn(first_turn, first_args)
        if game_over(eat_m, c, end):
            break

        eat_m, c, end = execute_turn(second_turn, second_args)
        if game_over(eat_m, c, end):
            break


if __name__ == "__main__":
    main()
