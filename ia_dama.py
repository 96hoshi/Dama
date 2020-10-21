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

    return eat_move


def count_pawns(i, j, color):
    if color == BLACK:
        return 1
    elif color == WHITE:
        return -1
    return 0


def count_damas(i, j, color):
    if color == DAMAB:
        return 1
    elif color == DAMAW:
        return -1
    return 0


def is_pawn_safe(i, j, color):
    if color == DAMAB or color == DAMAW:
        return 0

    if (j == 0 or j == 7) or (i == 0 or i == 7):
        if color == BLACK:
            return 1
        if color == WHITE:
            return -1
    return 0


def is_dama_safe(i, j, color):
    if (j == 0 or j == 7) or (i == 0 or i == 7):
        if color == DAMAB:
            return 1
        if color == DAMAW:
            return -1
    return 0


def promotion_distance(i, color):
    if color == BLACK:
        return i
    if color == WHITE:
        return i - (SIZE - 1)
    return 0


# 60.7543 secs con altezza 5
def eval(board, max_color):
    score = 0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] is not EMPTY:
                score += w1 * count_pawns(i, j, board[i][j])
                score += w2 * count_damas(i, j, board[i][j])
                score += w3 * is_pawn_safe(i, j, board[i][j])
                score += w4 * is_dama_safe(i, j, board[i][j])
                score += w5 * promotion_distance(i, board[i][j])

    if max_color == WHITE:
        return -score
    return score


def minmax(node, depth, maximizing_player, max_color, min_color):
    global min_val, max_val

    if maximizing_player:
        enemy_color = min_color
    else:
        enemy_color = max_color

    if depth == 0 or is_player_winner(enemy_color, node):
        return eval(node, max_color), []

    if maximizing_player:
        max_values = []
        max_values.append((-math.inf, []))

        forced_m = board_forced_moves(max_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, False, max_color, min_color)
                if v > max_values[0][0]:
                # update values
                    max_values.clear()
                    max_values.append((v, move))
                elif v == max_values[0][0]:
                    max_values.append((v, move))

        else:
            all_legal_m = board_legal_moves(max_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, False, max_color, min_color)
                if v > max_values[0][0]:
                # update values
                    max_values.clear()
                    max_values.append((v, move))
                elif v == max_values[0][0]:
                    max_values.append((v, move))

        return random.choice(max_values)

    else:  # minimizing player
        min_values = []
        min_values.append((math.inf, []))

        forced_m = board_forced_moves(min_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, True, max_color, min_color)
                if v < min_values[0][0]:
                # update values
                    min_values.clear()
                    min_values.append((v, move))
                elif v == min_values[0][0]:
                    min_values.append((v, move))

        else:
            all_legal_m = board_legal_moves(min_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, child)
                v, _ = minmax(child, depth - 1, True, max_color, min_color)
                if v < min_values[0][0]:
                # update values
                    min_values.clear()
                    min_values.append((v, move))
                elif v == min_values[0][0]:
                    min_values.append((v, move))

        return random.choice(min_values)


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
    print("{} turn:".format(player_color))

    enemy_color = opposite_color(player_color)

    if max_depth == 0:
        val, move = zero_minmax(player_color, board)
    else:
        val, move = minmax(board, max_depth, True, player_color, enemy_color)

    if not move:
        return False, enemy_color, True

    eat_move = perform_move(move, board)

    print("    VAL: {} ".format(val), end="")
    print("    {} IA move:".format(player_color), end="")
    print_movement(move, player_color)
    print_board(board)

    return eat_move, player_color, is_player_winner(player_color, board)

