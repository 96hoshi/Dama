#!/usr/bin/env python3

import math
from moves import *

MAX_DEPTH = 3
min_val = math.inf
max_val = -math.inf

def opposite_color(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE

def board_legal_moves(color, board):
    all_legal_m = []

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                l_m = legal_moves(i, j, board)
                for move in l_m:
                    all_legal_m.append([(i, j), move])

    return all_legal_m

def perform_move(m, forced, board):
    move = deepcopy(m)

    while len(move) > 1:
        i, j = move[0]
        end_i, end_j = move[1]

        movement(i, j, end_i, end_j, forced, board)
        del move[:1]

    if move:
        end_i, end_j = move.pop()
        check_new_dama(end_i, end_j, board)

def eval(board, max_color):
    w1 = 1
    w2 = 2

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

    if depth == MAX_DEPTH or win_condition(node):
        return eval(node, max_color), []

    if maximizing_player:
        value = -math.inf
        max_current = []
        forced_m = board_forced_moves(max_color, node)
        if forced_m:
            # print("DIM FORCED: {} {}".format(len(forced_m), forced_m))
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, True, child)
                v, _ = minmax(child, depth + 1, False, max_color, min_color)
                # print("val: {} moves:{}".format(v, m))
                if value <= v:
                    value = v
                    max_current = move
                # print("frc-val: {}".format(v), end = "")
                # print_movement(move, max_color)
        else:
            all_legal_m = board_legal_moves(max_color, node)
            # print("DIM LEGAL: {} {}".format(len(all_legal_m), all_legal_m))
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, False, child)
                v, _ = minmax(child, depth + 1, False, max_color, min_color)
                if value < v:
                    value = v
                    max_current = move
                # print("lgl-val: {}".format(v), end = "")
                # print_movement(move, max_color)


        max_val = max(max_val, value)
        min_val = min(min_val, value)
        # print(" Max: {} move: {}".format(value, m))
        # print("MAX_val: {}".format(value), end = "")
        # print_movement(max_current, max_color)
        return value, max_current

    else: # minimizing player
        value = math.inf
        min_current = []
        forced_m = board_forced_moves(min_color, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, True, child)
                v, m = minmax(child, depth + 1, True, max_color, min_color)
                if value > v:
                    value = v
                    min_current = move
                # print("val-F: {}".format(v), end = "")
                # print_movement(move, min_color)
        else:
            all_legal_m = board_legal_moves(min_color, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, False, child)
                v, m = minmax(child, depth + 1, True, max_color, min_color)
                if value > v:
                    value = v
                    min_current = move
        #         print("val-L: {}".format(v), end = "")
        #         print_movement(move, min_color)

        # print("MIN_val: {}".format(value), end = "")
        # print_movement(m, min_color)
        return value, min_current

def ia_turn(player_color, board):
    print("{} TURN:".format(player_color))
    global min_val, max_val

    all_forced_m = board_forced_moves(player_color, board)

    move = []
    forced = False

    if not check_if_empty(all_forced_m):
        forced = True

    enemy_color = opposite_color(player_color)
    val, move = minmax(board, 0, True, player_color, enemy_color)
    print("    VAL: {}".format(val), end = "")

    print("#### MIN: {} MAX: {}".format(min_val, max_val))
    min_val = math.inf
    max_val = -math.inf
    print("    {} IA move:".format(player_color), end = "")
    print_movement(move, player_color)

    perform_move(move, forced, board)
    print_board(board)

    return win_condition(board)
