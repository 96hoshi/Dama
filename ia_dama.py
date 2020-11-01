#!/usr/bin/env python3

import math
import random
from moves import *


we1 = 5
we2 = 8
we3 = 4
we4 = 2.5
we5 = 0.5
we6 = -3
we7 = 3
we8 = 0.65


# perform and update the game board
def perform_move(m, board):
    move = deepcopy(m)
    eat_move = False

    while len(move) > 1:
        i, j = move[0]
        end_i, end_j = move[1]

        eat_move = movement(i, j, end_i, end_j, board)
        del move[:1]

    return eat_move


# returns 1 if there is a black pawn, -1 if white
def count_pawns(color):
    if color == BLACK:
        return 1
    elif color == WHITE:
        return -1
    return 0


# returns 1 if there is a black dama, -1 if white dama
def count_damas(color):
    if color == DAMAB:
        return 1
    elif color == DAMAW:
        return -1
    return 0


# returns 1 if there is a black piece on the black backline
# -1 if there is a white piece on the white backline
def back_row(i, color):
    if (i == 0) and (color == BLACK or color == DAMAB):
        return 1
    if (i == 7) and (color == WHITE or color == DAMAW):
        return -1
    return 0


# returns 1 if there is a black piece in the middle 4 columns and
# the middle 2 rows, -1 if it's white
def mid_box(i, j, color):
    if i in range(2, 4):
        if j in range(2, 6):
            if color == BLACK or color == DAMAB:
                return 1
            else:
                return -1
    return 0


# returns 1 if there is a black piece in the middle 2 rowsin
# but not in the middle 4 columns, -1 if it's white
def mid_row(i, j, color):
    if i in range(2, 4):
        if (j in range(0, 2)) or (j in range(6, 8)):
            if color == BLACK or color == DAMAB:
                return 1
            else:
                return -1
    return 0


# returns 1 if the black piece at position (i, j) is vulnerable,
# (will be eaten next turn), -1 if it's white
def vulnerable(i, j, board):
    dir_i = 1
    color = WHITE
    if color_check(i, j, BLACK, board):
        dir_i = -1
        color = BLACK

    if can_be_eaten(i, dir_i, j, -1, color, board):
        return 1 * (-dir_i)
    if can_be_eaten(i, dir_i, j, 1, color, board):
        return 1 * (-dir_i)

    return 0


# check if a pawn in (i, j) can be eaten
def can_be_eaten(i, dir_i, j, dir_j, color, board):
    if box_legal(i - dir_i, j - dir_j):
        if not color_check(i - dir_i, j - dir_j, color, board):

            if box_legal(i + dir_i, j + dir_j):
                if board[i + dir_i][j + dir_j] == EMPTY:

                    if not is_dama(board[i][j]):
                        # I can be eaten
                        return True
                    elif is_dama(board[i - dir_i][j - dir_j]):
                        # If I'm a dama I still can be eaten by a dama
                        return True

        # check in opposite direction if I can be eaten by a dama
        if box_legal(i + dir_i, j + dir_j):
            if not color_check(i + dir_i, j + dir_j, color, board):

                if is_dama(board[i + dir_i][j + dir_j]):

                    if box_legal(i - dir_i, j - dir_j):
                        if board[i - dir_i][j - dir_j] == EMPTY:
                            return True

    return False


# returns 1 if the black piece at position (i, j) is protected,
# (cannot be eaten next turn), -1 if it's white
def protected(i, j, board):
    dir_i = 1
    color = WHITE
    if color_check(i, j, BLACK, board):
        dir_i = -1
        color = BLACK

    # pedina protected by same color pedinas
    if box_legal(i + dir_i, j + 1):
        if not color_check(i + dir_i, j + 1, color, board):
            return 0
    if box_legal(i + dir_i, j - 1):
        if not color_check(i + dir_i, j - 1, color, board):
            return 0
    return 1 * (-dir_i)


# returns the inverted sign of the number of box
# from the piece and the line to become a dama
def promotion_distance(i, color):
    if color == BLACK:
        return i
    if color == WHITE:
        return i - (SIZE - 1)
    return 0


# returns the heuristic value of the board according to
# the maximizer color
def eval(board, max_color):
    score = 0

    for i in range(SIZE):
        for j in range(SIZE):
            color = board[i][j]
            if color is not EMPTY:
                score += we1 * count_pawns(color)
                score += we2 * count_damas(color)
                score += we3 * back_row(i, color)
                score += we4 * mid_box(i, j, color)
                score += we5 * mid_row(i, j, color)
                score += we6 * vulnerable(i, j, board)
                score += we7 * protected(i, j, board)
                score += we8 * promotion_distance(i, color)

    if max_color == WHITE:
        return -score
    return score


# real engine of the ia.
# returns the best move to perform and the calculated value
# according to the evaluation function
def minmax(node, depth, maximizing_player, max_color, min_color):
    global min_val, max_val

    if maximizing_player:
        enemy_color = min_color
    else:
        enemy_color = max_color

    # case base: if is a terminal node then evaluate the state of the game
    # check if max_depth is reached or the player who has moved has won
    if depth == 0 or is_player_winner(enemy_color, node):
        return eval(node, max_color), []

    if maximizing_player:
        max_values = []
        max_values.append((-math.inf, []))
        # check first forced moves
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
        # check first forced moves
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


# alternative version for the ia with max_depth=0
def zero_minmax(color, board):
    forced_m = board_forced_moves(color, board)
    if forced_m:
        return 0, random.choice(forced_m)
    else:
        legal_m = board_legal_moves(color, board)
        if legal_m:
            return 0, random.choice(legal_m)

    return 0, []


# simulate a ia turn.
# call the minmax function to find the move to perform
# and update the game board
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
