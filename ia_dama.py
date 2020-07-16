#!/usr/bin/env python3

import math
from moves import *

MAX_DEPTH = 3
min_val = math.inf
max_val = -math.inf

def all_legal_moves(color, board):
    all_legal_m = []

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                l_m = legal_moves(i, j, board)
                for move in l_m:
                    all_legal_m.append([(i, j), move])

    # print("alm:", all_legal_m)
    return all_legal_m

def perform_move(m, forced, board):
    move = deepcopy(m)

    while len(move) > 1:
        i, j = move[0]
        end_i, end_j = move[1]

        if forced:
            eat_pedina(i, j, end_i, end_j, board)

        board[end_i][end_j] = board[i][j]
        board[i][j] = EMPTY

        del move[:1]

    if move:
        end_i, end_j = move.pop()
        check_new_dama(end_i, end_j, board)

def eval(board):
    whites = 0
    blacks = 0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == WHITE or board[i][j] == DAMAW:
                whites += 1
            if board[i][j] == BLACK or board[i][j] == DAMAB:
                blacks += 1

    return blacks - whites

def minmax(node, depth, maximizing_player):
    global min_val, max_val

    if depth == MAX_DEPTH or win_condition(node):
        return eval(node), []
    if maximizing_player:
        value = -math.inf
        m = []
        forced_m = board_forced_moves(BLACK, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, True, child)
                v, m = minmax(child, depth + 1, False)
                value = max(value, v)
                m.append(move)
        else:
            all_legal_m = all_legal_moves(BLACK, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, False, child)
                v, m = minmax(child, depth + 1, False)
                value = max(value, v)
                m.append(move)

        max_val = max(max_val, value)
        min_val = min(min_val, value)
        print(m)
        return value, m
    else: # minimizing player
        value = math.inf
        m = []
        forced_m = board_forced_moves(BLACK, node)
        if forced_m:
            for move in forced_m:
                child = deepcopy(node)
                perform_move(move, True, child)
                v, m = minmax(child, depth + 1, True)
                value = min(value, v)
                m.append(move)
        else:
            all_legal_m = all_legal_moves(BLACK, node)
            for move in all_legal_m:
                child = deepcopy(node)
                perform_move(move, False, child)
                v, m = minmax(child, depth + 1, True)
                value = min(value, v)
                m.append(move)

        return value, m

def ia_turn(player_color, board):
    global min_val, max_val
    all_forced_m = board_forced_moves(player_color, board)

    move = []
    forced = False

    if not check_if_empty(all_forced_m):
        forced = True

    moves = minmax(board, 0, True)[1]
    move = moves.pop()
    # print("----------------- Min: {} MAX: {}".format(min_val, max_val))
    min_val = math.inf
    max_val = -math.inf
    print("IA move: ", move)

    perform_move(move, forced, board)

    print_board(board)

    return win_condition(board)