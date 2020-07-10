#!/usr/bin/env python3

from copy import copy, deepcopy

# ----------------------consts-------------------------------

SIZE = 8

EMPTY = " "
WHITE = "W"
BLACK = "B"
DAMAW = "W-D"
DAMAB = "B-D"

# PEDINE:
# White
# Black
# White-Dama
# Black-Dama
# TODO:
# assicurarsi che color sia binario

max_eat = 0
max_paths = []
max_eaten_order = []
max_is_dama = 0

# color:
# white = WHITE or DAMAW
# black = BLACK or DAMAB

# ----------------------------------------------------

# check if the pedina is inside the board
def box_legal(i, j):
    return i in range(SIZE) and j in range(SIZE)

# check if there is a pedina of that color
def color_check(i, j, color, board):
    if color == WHITE:
        return board[i][j] == WHITE or board[i][j] == DAMAW
    else:
        return board[i][j] == BLACK or board[i][j] == DAMAB

# removes the eaten pedina between two positions
def eat_pedina(i, j, end_i, end_j, board):
    delete_i = (i + end_i) // 2
    delete_j = (j + end_j) // 2

    board[delete_i][delete_j] = EMPTY

# ----------------------------------------------------

def is_dama(string):
    return string == DAMAB or string == DAMAW

def clear_max():
    global max_eat
    global max_paths
    global max_eaten_order
    global max_is_dama

    max_eat = 0
    max_paths = []
    max_eaten_order = []
    max_is_dama = 0

def eval_and_register_path(path, eaten, dama):
    global max_eat
    global max_paths
    global max_eaten_order
    global max_is_dama

    n_eat = len(eaten)
    print(n_eat, path, eaten, dama)

    if n_eat > max_eat:
        max_eat = n_eat
        max_paths.clear()
        max_paths.append(path)
        max_eaten_order = eaten
        max_is_dama = dama

    elif n_eat == max_eat:
        if (not max_is_dama) and (not dama):
            max_paths.append(path)

        elif (not max_is_dama) and dama:
            max_eat = n_eat
            max_paths.clear()
            max_paths.append(path)
            max_eaten_order = eaten
            max_is_dama = dama

            # entrambe sono dama
        elif max_is_dama and dama:
            # confronta chi ha mangiato più dame
            d_eaten = eaten.count("d")
            d_max_eaten = max_eaten_order.count("d")

            if d_eaten > d_max_eaten:
                max_eat = n_eat
                max_paths.clear()
                max_paths.append(path)
                max_eaten_order = eaten
                max_is_dama = dama

            # se hanno mangiato lo stesso numero di dame
            elif d_eaten == d_max_eaten:
                if d_eaten > 0:
                    # trovo il path che ha incontrato prima una dama
                    if eaten.index("d") < max_eaten_order.index("d"):
                        max_eat = n_eat
                        max_paths.clear()
                        max_paths.append(path)
                        max_eaten_order = eaten
                        max_is_dama = dama

                    elif eaten.index("d") == max_eaten_order.index("d"):
                        max_paths.append(path)
                else:
                    max_paths.append(path)

def copy_new_board(i, j, end_i, end_j, eat, board):
    new_board = deepcopy(board)

    new_board[end_i][end_j] = new_board[i][j]
    new_board[i][j] = EMPTY
    if eat:
        eat_pedina(i, j, end_i, end_j, new_board)

    return new_board

def board_forced_moves(color, board):
    clear_max()

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                calculate_forced_moves(i, j, color, [(i, j)], [], is_dama(board[i][j]), board)

    print("Forced paths:", max_paths)
    return max_paths

def check_direction(i, dir_i, j, dir_j, color, path, eaten, dama, board):
    if box_legal(i + dir_i, j + dir_j) and board[i + dir_i][j + dir_j] != EMPTY:
        if not color_check(i + dir_i, j + dir_j, color, board):
            # se la casella dx è occupata da una pedina avversaria
            if box_legal(i + dir_i*2, j + dir_j*2) and board[i + dir_i*2][j + dir_j*2] == EMPTY:
                # e la casella dopo è libera, posso mangiare
                if not is_dama(board[i + dir_i][j + dir_j]):
                    new_eaten = eaten.copy()
                    new_eaten.append("p") #ho mangiato una pedina
                    new_path = path.copy()
                    new_path.append((i + dir_i*2, j + dir_j*2))
                    #copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir_i*2, j + dir_j*2, True, board)
                    calculate_forced_moves(i + dir_i*2, j + dir_j*2, color, new_path, new_eaten, dama, new_board)
                    return False
                elif dama:
                    new_eaten = eaten.copy()
                    new_eaten.append("d") #ho mangiato una dama
                    new_path = path.copy()
                    new_path.append((i + dir_i*2, j + dir_j*2))
                    new_board = copy_new_board(i, j, i + dir_i*2, j + dir_j*2, True, board)
                    calculate_forced_moves(i + dir_i*2, j + dir_j*2, color, new_path, new_eaten, dama, new_board)
                    return False

    return True

def calculate_forced_moves(i, j, color, path, eaten, dama, board):
    stop = True
    dir_i = 1
    if color == WHITE:
        dir_i = -1
    # dir_j = -1 se dx
    dx = -1
    # dir_j = 1 se sx
    sx = 1

    # destra
    stop = check_direction(i, dir_i, j, dx, color, path, eaten, dama, board)
    # sinistra
    stop = check_direction(i, dir_i, j, sx, color, path, eaten, dama, board)

    # se sono una dama valuto anche le altre due direzioni
    if dama:
        dir_i *= -1
        stop = check_direction(i, dir_i, j, dx, color, path, eaten, dama, board)
        stop = check_direction(i, dir_i, j, sx, color, path, eaten, dama, board)

    if stop and len(path) > 1:
        eval_and_register_path(path, eaten, dama)
        # aggiungi la mossa al set di mosse (poi verrà confrontata)
