#!/usr/bin/env python3

import math
import random
import new_method
from consts import *
from moves import *


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
    return win_condition(WHITE, board) or win_condition(BLACK, board)


# 55.0345 secs con altezza 5
def eval(board, max_color):
    whites = 0
    blacks = 0
    white_damas = 0
    black_damas = 0
    safe_whites = 0
    safe_blacks = 0
    safe_white_damas = 0
    safe_black_damas = 0
    white_promotion_dis = 0
    black_promotion_dis = 0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] is not EMPTY:
                if board[i][j] == WHITE:
                    whites += 1
                    safe_whites += is_safe(i, j)
                    white_promotion_dis += (SIZE - 1) - i

                elif board[i][j] == DAMAW:
                    white_damas += 1
                    safe_white_damas += is_safe(i, j)

                elif board[i][j] == BLACK:
                    blacks += 1
                    safe_blacks += is_safe(i, j)
                    black_promotion_dis += i

                elif board[i][j] == DAMAB:
                    black_damas += 1
                    safe_black_damas += is_safe(i, j)

    pawns = blacks - whites
    damas = black_damas - white_damas
    safe_paws = safe_blacks - safe_whites
    safe_damas = safe_black_damas - safe_white_damas
    promotion_distance = black_promotion_dis - white_promotion_dis

    score = w1 * pawns + w2 * damas + w3 * safe_paws + w4 * safe_damas + w5 * promotion_distance

    if max_color == WHITE:
        return -score
    return score


def is_safe(i, j):
    if (j == 0 or j == 7) or (i == 0 or i == 7):
        return 1

    return 0


def minmax(node, depth, maximizing_player, max_color, min_color):
    global min_val, max_val

    if depth == 0 or end_game(node):
        return eval(node, max_color), []

    if maximizing_player:
        value = -math.inf
        max_current = []
        forced_m = board_forced_moves(max_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, False, max_color, min_color)
                if value < v:
                    value = v
                    max_current = move
        else:
            all_legal_m = board_legal_moves(max_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, False, max_color, min_color)
                if value < v:
                    value = v
                    max_current = move

        return value, max_current

    else:  # minimizing player
        value = math.inf
        min_current = []
        forced_m = board_forced_moves(min_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, True, max_color, min_color)
                if value > v:
                    value = v
                    min_current = move
        else:
            all_legal_m = board_legal_moves(min_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, True, max_color, min_color)
                if value > v:
                    value = v
                    min_current = move

        return value, min_current


def zero_minmax(color, board):
    forced_m = board_forced_moves(color, board)
    if forced_m:
        return 0, random.choice(forced_m)
    else:
        legal_m = board_legal_moves(color, board)
        if legal_m:
            return 0, random.choice(legal_m)

    return 0, []


def ia_turn(player_color, max_depth, board):
    # print("{} turn:".format(player_color))

    enemy_color = opposite_color(player_color)

    if max_depth == 0:
        val, move = zero_minmax(player_color, board)
    else:
        val, move = new_method.minmax(board, max_depth, True, player_color, enemy_color)

    if not move:
        return False, enemy_color, True

    # print("    VAL: {} ".format(val), end="")
    # print("    {} IA move:".format(player_color), end="")

    # print_movement(move, player_color)

    eat_move = perform_move(move, board)
    # print_board(board)

    return eat_move, player_color, win_condition(player_color, board)

# def ia_turn(player_color, max_depth, board):
#     print("{} turn:".format(player_color))

#     enemy_color = opposite_color(player_color)

#     if max_depth == 0:
#         val, move = zero_minmax(player_color, board)
#     else:
#         val, move = minmax(board, max_depth, True, player_color, enemy_color)

#     print("    VAL: {} ".format(val), end="")
#     print("    {} IA move:".format(player_color), end="")

#     if not move:
#         return False, enemy_color, True

#     print_movement(move, player_color)

#     eat_move = perform_move(move, board)
#     print_board(board)

#     return eat_move, player_color, win_condition(player_color, board)
