#!/usr/bin/env python3

import math
import time
from moves import *

MAX_DEPTH = 4

def perform_move(m, board):
    move = deepcopy(m)
    eat_move = False

    while len(move) > 1:
        i, j = move[0]
        end_i, end_j = move[1]

        eat_move = movement(i, j, end_i, end_j, board)
        del move[:1]

    if move:
        end_i, end_j = move.pop()
        check_new_dama(end_i, end_j, board)

    return eat_move

def end_game(board):
    return not (move_aviable(WHITE, board) and move_aviable(BLACK, board))

# # check if there's only one color in the board
# # and if the enemy cannot do any movement
def move_aviable(color, board):
    dama_col = DAMAB
    if color == WHITE:
        dama_col = DAMAW

    enemy_color = opposite_color(color)

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY:
                continue
            if color_check(i, j, color, board):
                continue
            else:
                # if the enemy can do a movement then it's not a win condition
                enemy_legal = legal_moves(i, j, board)
                if enemy_legal:
                    return True

                # if the enemy can eat then it's not a win condition
                dir_i = 1
                if enemy_color == WHITE:
                    dir_i = -1
                if can_eat(i, dir_i, j, -1, enemy_color, board):
                    return True
                if can_eat(i, dir_i, j, 1, enemy_color, board):
                    return True

                if is_dama(board[i][j]):
                    dir_i *= -1
                    if can_eat(i, dir_i, j, -1, enemy_color, board):
                        return True
                    if can_eat(i, dir_i, j, 1, enemy_color, board):
                        return True

    return False

# check if is possible to eat AT LEAST a pedina from a position (i, j)
def can_eat(i, dir_i, j, dir_j, color, board):
    if box_legal(i + dir_i, j + dir_j) and board[i + dir_i][j + dir_j] != EMPTY:
        if not color_check(i + dir_i, j + dir_j, color, board):
            if box_legal(i + dir_i*2, j + dir_j*2) and board[i + dir_i*2][j + dir_j*2] == EMPTY:

                if not is_dama(board[i + dir_i][j + dir_j]):
                    # I can eat
                    return True
                elif is_dama(board[i][j]):
                    # I can eat a dama if I'm a dama
                    return True
    return False

def eval(board, max_color):
    w1 = 1
    w2 = 3

    whites = 0
    blacks = 0
    white_damas = 0
    black_damas = 0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == WHITE:
                whites += 1
            if board[i][j] == DAMAW:
                white_damas += 1
            if board[i][j] == BLACK:
                blacks += 1
            if board[i][j] == DAMAB:
                black_damas += 1

    score = w1*(blacks - whites) + w2*(black_damas - white_damas)

    if max_color == WHITE:
        return -score
    return score

def minmax(node, depth, maximizing_player, max_color, min_color):
    global min_val, max_val

    if depth == MAX_DEPTH or end_game(node):
        return eval(node, max_color), []

    if maximizing_player:
        value = -math.inf
        max_current = []
        forced_m = board_forced_moves(max_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth + 1, False, max_color, min_color)
                if value < v:
                    value = v
                    max_current = move
        else:
            all_legal_m = board_legal_moves(max_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth + 1, False, max_color, min_color)
                if value < v:
                    value = v
                    max_current = move

        return value, max_current

    else: # minimizing player
        value = math.inf
        min_current = []
        forced_m = board_forced_moves(min_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth + 1, True, max_color, min_color)
                if value > v:
                    value = v
                    min_current = move
        else:
            all_legal_m = board_legal_moves(min_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth + 1, True, max_color, min_color)
                if value > v:
                    value = v
                    min_current = move

        return value, min_current

def ia_turn(player_color, board):
    print("{} turn:".format(player_color))

    enemy_color = opposite_color(player_color)
    val, move = minmax(board, 0, True, player_color, enemy_color)
    # time.sleep(1)

    if not move:
        return False, enemy_color, True

    print("    VAL: {} ".format(val), end = "")
    print("    {} IA move:".format(player_color), end = "")
    print_movement(move, player_color)

    eat_move = perform_move(move, board)
    print_board(board)

    return eat_move, player_color, win_condition(player_color, board)
