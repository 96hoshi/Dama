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
max_path = []
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
    global max_path
    global max_eaten_order
    global max_is_dama

    max_eat = 0
    max_path = []
    max_eaten_order = []
    max_is_dama = 0

def eval_and_register_path(path, eaten, dama):
    global max_eat
    global max_path
    global max_eaten_order
    global max_is_dama

    n_eat = len(eaten)
    print(n_eat, path, eaten, dama)

    if n_eat < max_eat:
        print("not the best")
        return

    if n_eat == max_eat:
        if max_is_dama and not dama:
            print("dama has priority")
            return
        # entrambe sono dama
        if max_is_dama and dama:
            # confronta chi ha mangiato più dame
            d_eaten = eaten.count("d")
            # print("d_eaten: ", d_eaten)
            d_max_eaten = max_eaten_order.count("d")
            if d_eaten < d_max_eaten:
                return

            # se hanno mangiato lo stesso numero di dame
            if d_eaten == d_max_eaten and d_eaten > 0:
                # trovo il path che ha incontrato prima una dama
                if eaten.index("d") > max_eaten_order.index("d"):
                    return
                if eaten.index("d") == max_eaten_order.index("d"):
                    # caso particolare: entrambe le scelte sono equivalenti
                    # devo aggiungere entrambe alle mosse obbligate
                    # da modificarein lista di liste
                    return
# update values
    max_eat = n_eat
    max_path = []
    # max_path.append(path)
    max_path = path
    max_eaten_order = eaten
    max_is_dama = dama
    print("-----------", path, max_path)

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

    print(max_path)
    return max_path


def calculate_forced_moves(i, j, color, path, eaten, dama, board):
    dir = 1
    if color == WHITE:
        dir = -1

    # destra
    if box_legal(i + dir, j - 1) and board[i + dir][j - 1] != EMPTY:
        if not color_check(i + dir, j - 1, color, board):
            # se la casella dx è occupata da una pedina avversaria
            if box_legal(i + dir*2, j - 2) and board[i + dir*2][j - 2] == EMPTY:
                # e la casella dopo è libera, posso mangiare
                if not is_dama(board[i + dir][j - 1]):
                    eaten.append("p") #ho mangiato una pedina
                    path.append((i + dir*2, j - 2))
                    #copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir*2, j - 2, True, board)
                    calculate_forced_moves(i + dir*2, j - 2, color, path, eaten, dama, new_board)
                elif dama:
                    eaten.append("d") #ho mangiato una dama
                    path.append((i + dir*2, j - 2))
                    #copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir*2, j - 2, True, board)
                    calculate_forced_moves(i + dir*2, j - 2, color, path, eaten, dama, new_board)

    # sinistra
    if box_legal(i + dir, j + 1) and board[i + dir][j + 1] != EMPTY:
        if not color_check(i + dir, j + 1, color, board):
            if box_legal(i + dir*2, j + 2) and board[i + dir*2][j + 2] == EMPTY:
                if not is_dama(board[i + dir][j + 1]):
                    eaten.append("p") #ho mangiato una pedina
                    path.append((i + dir*2, j + 2))
                    #copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir*2, j + 2, True, board)
                    calculate_forced_moves(i + dir*2, j + 2, color, path, eaten, dama, new_board)
                elif dama:
                    eaten.append("d") #ho mangiato una dama
                    path.append((i + dir*2, j + 2))
                    #copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir*2, j + 2, True, board)
                    calculate_forced_moves(i + dir*2, j + 2, color, path, eaten, dama, new_board)

    # se sono una dama valuto anche e altre due direzioni
    if dama:
        dir *= -1
        # destra
        if box_legal(i + dir, j - 1) and board[i + dir][j - 1] != EMPTY:
            if not color_check(i + dir, j - 1, color, board):
                # se la casella dx è occupata da una pedina avversaria
                if box_legal(i + dir*2, j - 2) and board[i + dir*2][j - 2] == EMPTY:
                    # e la casella dopo è libera, posso mangiare
                    if not is_dama(board[i + dir][j - 1]):
                        eaten.append("p") #ho mangiato una pedina
                        path.append((i + dir*2, j - 2))
                        #copia della nuova board con la mossa effettuata
                        new_board = copy_new_board(i, j, i + dir*2, j - 2, True, board)
                        calculate_forced_moves(i + dir*2, j - 2, color, path, eaten, dama, new_board)
                    else:
                        eaten.append("d") #ho mangiato una dama
                        path.append((i + dir*2, j - 2))
                        #copia della nuova board con la mossa effettuata
                        new_board = copy_new_board(i, j, i + dir*2, j - 2, True, board)
                        calculate_forced_moves(i + dir*2, j - 2, color, path, eaten, dama, new_board)

        # sinistra
        if box_legal(i + dir, j + 1) and board[i + dir][j + 1] != EMPTY:
            if not color_check(i + dir, j + 1, color, board):
                if box_legal(i + dir*2, j + 2) and board[i + dir*2][j + 2] == EMPTY:
                    if not is_dama(board[i + dir][j + 1]):
                        eaten.append("p") #ho mangiato una pedina
                        path.append((i + dir*2, j + 2))
                        #copia della nuova board con la mossa effettuata
                        new_board = copy_new_board(i, j, i + dir*2, j + 2, True, board)
                        calculate_forced_moves(i + dir*2, j + 2, color, path, eaten, dama, new_board)

                    else:
                        eaten.append("d") #ho mangiato una dama
                        path.append((i + dir*2, j + 2))
                        #copia della nuova board con la mossa effettuata
                        new_board = copy_new_board(i, j, i + dir*2, j + 2, True, board)
                        calculate_forced_moves(i + dir*2, j + 2, color, path, eaten, dama, new_board)


    # se arrivo fino in fondo e nel path c'è più di una mossa
    if len(path) > 1:
        eval_and_register_path(path, eaten, dama)
        # aggiungi la mossa al set di mosse (poi verrà confrontata)
