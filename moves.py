#!/usr/bin/env python3

from copy import deepcopy

# ----------------------consts-------------------------------

SIZE = 8

EMPTY = " "
WHITE = ' \033[91m' + "W" + '\033[0m '
BLACK = ' \033[94m' + "B" + '\033[0m '
DAMAW = '\033[91m' + "W-D" + '\033[0m'
DAMAB = '\033[94m' + "B-D" + '\033[0m'

max_eat = 0
max_paths = []
max_eaten_order = []
max_is_dama = 0

# ------------------------prints----------------------------


# print a dama board
def print_board(board):
    print('    ', end="")
    for c in range(SIZE):
        print('{:^4}'.format(c), end="")
    print()
    print("   ---------------------------------")
    for r in range(SIZE):
        print("{:^3}".format(r), end="")
        for c in range(SIZE):
            print('|{:^3}'.format(board[r][c]), end="")
        print("|")
        print("   ---------------------------------")


def print_position(position, color):
    c = '\033[94m'
    if color == WHITE:
        c = '\033[91m'

    i, j = position
    print(" {}{},{}\033[0m".format(c, i, j), end="")


def print_movement(m, color):
    if not m:
        return

    print_position(m[0], color)
    print(" ->", end="")
    print_position(m[1], color)
    print()

# DEBUG print
# def print_move(move, color):
#     for pos in move:
#         print_position(pos[0], color)
#         print(" ->", end = "")
#         print_position(pos[1], color)
#         print(", ", end = "")
#     print()

# --------------------utilities------------------------------


# check if the pawn is inside the board
def box_legal(i, j):
    return i in range(SIZE) and j in range(SIZE)


# check if there is a pawn of that color
def color_check(i, j, color, board):
    if color == WHITE:
        return board[i][j] == WHITE or board[i][j] == DAMAW
    else:
        return board[i][j] == BLACK or board[i][j] == DAMAB


def opposite_color(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def is_dama(string):
    return string == DAMAB or string == DAMAW


# check if the pawn becomes dama
def check_new_dama(i, j, board):
    if board[i][j] == WHITE and i == 0:
        board[i][j] = DAMAW
        return True

    if board[i][j] == BLACK and i == 7:
        board[i][j] = DAMAB
        return True

    return False


def ask_input(string):
    while True:
        try:
            str_i, str_j = input(string).split()
        except ValueError:
            print("Wrong input, correct usage: <int, int>")
            continue
        else:
            return str_i, str_j


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def ask_box(string):
    str_i, str_j = ask_input(string)
    while (not is_int(str_i)) and (not is_int(str_j)):
        print("Wrong input, correct usage: <int, int>")
        continue

    i = int(str_i)
    j = int(str_j)
    return i, j


# check if there's only one color in the board
# and if the enemy cannot do any movement
def win_condition(color, board):
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
                    return False

                # if the enemy can eat then it's not a win condition
                dir_i = 1
                if enemy_color == WHITE:
                    dir_i = -1
                if can_eat(i, dir_i, j, -1, enemy_color, board):
                    return False
                if can_eat(i, dir_i, j, 1, enemy_color, board):
                    return False

                if is_dama(board[i][j]):
                    dir_i *= -1
                    if can_eat(i, dir_i, j, -1, enemy_color, board):
                        return False
                    if can_eat(i, dir_i, j, 1, enemy_color, board):
                        return False
    return True


# check if is possible to eat AT LEAST a pawn from a position (i, j)
def can_eat(i, dir_i, j, dir_j, color, board):
    if box_legal(i + dir_i, j + dir_j) and board[i + dir_i][j + dir_j] != EMPTY:
        if not color_check(i + dir_i, j + dir_j, color, board):
            if box_legal(i + dir_i * 2, j + dir_j * 2) and board[i + dir_i * 2][j + dir_j * 2] == EMPTY:

                if not is_dama(board[i + dir_i][j + dir_j]):
                    # I can eat
                    return True
                elif is_dama(board[i][j]):
                    # I can eat a dama if I'm a dama
                    return True
    return False


# returns list of legal moves from a position
# if there's no pawn in there returns empty list
# ASSUMPTION: (i, j) is a board position
def legal_moves(i, j, board):
    legal_m = []

    dama = is_dama(board[i][j])

    if color_check(i, j, WHITE, board) or dama:
        if box_legal(i - 1, j - 1) and board[i - 1][j - 1] == EMPTY:
            legal_m.append((i - 1, j - 1))
        if box_legal(i - 1, j + 1) and board[i - 1][j + 1] == EMPTY:
            legal_m.append((i - 1, j + 1))

    if color_check(i, j, BLACK, board) or dama:
        if box_legal(i + 1, j - 1) and board[i + 1][j - 1] == EMPTY:
            legal_m.append((i + 1, j - 1))
        if box_legal(i + 1, j + 1) and board[i + 1][j + 1] == EMPTY:
            legal_m.append((i + 1, j + 1))

    return legal_m


# returna a list of possible legal moves on the board
# for the player of that color
# returns a list of lists
def board_legal_moves(color, board):
    all_legal_m = []

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                l_m = legal_moves(i, j, board)
                for move in l_m:
                    all_legal_m.append([(i, j), move])

    return all_legal_m


# check if a list of lists is empty
def check_if_empty(list_of_lists):
    for elem in list_of_lists:
        if elem:
            return False
    return True


def update_forced_move(i, j, all_forced_m):
    updated_forced_m = []
    for path in all_forced_m:
        if path[0] == (i, j):
            path.pop(0)
            updated_forced_m.append(path)

    return updated_forced_m


def search_forced_move(i, j, all_forced_m):
    for path in all_forced_m:
        if path[0] == (i, j):
            return True

    return False


# perform a single movement froma (i,j) to (end_i,end_j)
# removing enemy pawn if needed
def movement(i, j, end_i, end_j, board):
    board[end_i][end_j] = board[i][j]
    board[i][j] = EMPTY

    diff_i = abs(i - end_i)
    diff_j = abs(j - end_j)

    if diff_i == 2 or diff_j == 2:
        # if eat move is performed
        delete_i = (i + end_i) // 2
        delete_j = (j + end_j) // 2

        # removes the eaten pawn between two positions
        board[delete_i][delete_j] = EMPTY
        return True
    return False


# check if is possible to updates the board moving a pawn.
# if and only if (end_i, end_j) are legal_moves
# if there's a forced move to do and it's not (end_i, end_j)
# it is an illegal move
def try_move(i, j, end_i, end_j, all_forced_m, board):
    # there's a forced move but it's not the selected one
    if not check_if_empty(all_forced_m):
        if search_forced_move(end_i, end_j, all_forced_m):
            all_forced_m = update_forced_move(end_i, end_j, all_forced_m)
        else:
            print("There are forced moves to do: ", all_forced_m)
            return False
    else:
        l_moves = legal_moves(i, j, board)
        if l_moves:
            # there's a legal move but it's not the selected one
            if (end_i, end_j) not in l_moves:
                print("Not a legal move")
                return False
            else:
                l_moves.clear()

    movement(i, j, end_i, end_j, board)
    check_new_dama(end_i, end_j, board)

    return True


def clear_max():
    global max_eat
    global max_paths
    global max_eaten_order
    global max_is_dama

    max_eat = 0
    max_paths = []
    max_eaten_order = []
    max_is_dama = 0


def update_max(n_eat, path, eaten, dama):
    global max_eat
    global max_paths
    global max_eaten_order
    global max_is_dama

    max_eat = n_eat
    max_paths.clear()
    max_paths.append(path)
    max_eaten_order = eaten
    max_is_dama = dama


def register_path(path, eaten, dama):
    global max_paths

    n_eat = len(eaten)

    if n_eat > max_eat:
        update_max(n_eat, path, eaten, dama)
    elif n_eat == max_eat:

        if (not max_is_dama) and (not dama):
            max_paths.append(path)
        elif (not max_is_dama) and dama:
            update_max(n_eat, path, eaten, dama)
            # entrambe sono dama
        elif max_is_dama and dama:

            # confronta chi ha mangiato più dame
            d_eaten = eaten.count("d")
            d_max_eaten = max_eaten_order.count("d")
            if d_eaten > d_max_eaten:
                update_max(n_eat, path, eaten, dama)
            # se hanno mangiato lo stesso numero di dame
            elif d_eaten == d_max_eaten:
                if d_eaten > 0:

                    # trovo il path che ha incontrato prima una dama
                    index_eaten = eaten.index("d")
                    index_max_eaten = max_eaten_order.index("d")
                    if index_eaten < index_max_eaten:
                        update_max(n_eat, path, eaten, dama)
                    elif index_eaten == index_max_eaten:
                        max_paths.append(path)
                else:
                    max_paths.append(path)


def copy_new_eaten(eaten, p):
    new_eaten = eaten.copy()
    new_eaten.append(p)

    return new_eaten


def copy_new_path(path, elem):
    new_path = path.copy()
    new_path.append(elem)

    return new_path


def copy_new_board(i, j, end_i, end_j, board):
    new_board = deepcopy(board)
    movement(i, j, end_i, end_j, new_board)

    return new_board


# returns a list of lists
def board_forced_moves(color, board):
    clear_max()

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                calculate_forced_moves(i, j, color, [(i, j)], [], is_dama(board[i][j]), board)

    return max_paths


def check_direction(i, dir_i, j, dir_j, color, path, eaten, dama, board):
    if box_legal(i + dir_i, j + dir_j) and board[i + dir_i][j + dir_j] != EMPTY:
        # se la casella è occupata da una pedina avversaria
        if not color_check(i + dir_i, j + dir_j, color, board):
            # e la casella dopo è libera
            if box_legal(i + dir_i * 2, j + dir_j * 2) and board[i + dir_i*2][j + dir_j * 2] == EMPTY:
                # non è una dama
                if not is_dama(board[i + dir_i][j + dir_j]):
                    # ho mangiato una pedina semplice
                    new_eaten = copy_new_eaten(eaten, "p")
                    new_path = copy_new_path(path, (i + dir_i * 2, j + dir_j * 2))
                    # copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir_i * 2, j + dir_j * 2, board)
                    calculate_forced_moves(i + dir_i * 2, j + dir_j * 2, color, new_path, new_eaten, dama, new_board)
                    return False
                # è una dama e anche io sono una dama
                elif dama:
                    # ho mangiato una dama
                    new_eaten = copy_new_eaten(eaten, "d")
                    new_path = copy_new_path(path, (i + dir_i * 2, j + dir_j * 2))
                    new_board = copy_new_board(i, j, i + dir_i * 2, j + dir_j * 2, board)
                    calculate_forced_moves(i + dir_i * 2, j + dir_j * 2, color, new_path, new_eaten, dama, new_board)
                    return False

    return True


def calculate_forced_moves(i, j, color, path, eaten, dama, board):
    stop = True
    dir_i = 1
    if color == WHITE:
        dir_i = -1

    # se dx allora dir_j = -1
    dx = -1
    # se sx allora dir_j = 1
    sx = 1

    stop = check_direction(i, dir_i, j, dx, color, path, eaten, dama, board)
    stop = check_direction(i, dir_i, j, sx, color, path, eaten, dama, board)

    # se sono una dama valuto anche le altre due direzioni
    if dama:
        dir_i *= -1
        stop = check_direction(i, dir_i, j, dx, color, path, eaten, dama, board)
        stop = check_direction(i, dir_i, j, sx, color, path, eaten, dama, board)

    # aggiungi la mossa al set di mosse (poi verrà confrontata)
    if stop and len(path) > 1:
        register_path(path, eaten, dama)

# ORDINAMENTO:
# Avendo più possibilità di presa si debbono rispettare obbligatoriamente
# nell'ordine le seguenti priorità:
# DONE # è obbligatorio mangiare dove ci sono più pezzi;
# DONE # a parità di pezzi da prendere, tra pedina e dama si è obbligati
#        a mangiare la dama;
#       inoltre se si può optare tra il mangiare di dama o di pedina
#       è obbligatorio mangiare con la dama;
# DONE # la dama sceglie la presa dove si mangiano più dame;
# DONE # a parità  di condizioni si mangia dove s'incontra prima
#        la dama avversaria.

# TODO:
# Si vince per abbandono dell'avversario, che si trova in palese difficoltà,
# o quando si catturano o si bloccano tutti i pezzi avversari.
# DONE

# TODO:
# Si pareggia in una situazione di evidente equilibrio finale per accordo
# dei giocatori o per decisione dell'arbitro a seguito del conto di 40 mosse
# richiesto da uno dei due giocatori.
# Il conteggio delle mosse si azzera e riparte da capo tutte le volte che
# uno dei due giocatori muove una pedina o effettua una presa.
# DONE


def human_turn(player_color, board):
    print("{} turn:".format(player_color))
    eat_move = False

    all_forced_m = board_forced_moves(player_color, board)
    all_legal_m = board_legal_moves(player_color, board)

    if (not all_forced_m) and (not all_legal_m):
        print("No possible moves to do")
        return False, opposite_color(player_color), True

    # first box position loop
    while True:
        # ask for pawn to move
        i, j = ask_box("Enter box location: ")

        # check if there is a pawn of player color
        if not (box_legal(i, j) and color_check(i, j, player_color, board)):
            print("Not a legal position")
            continue

        # check if there are moves to do first
        if not check_if_empty(all_forced_m):
            eat_move = True
            if search_forced_move(i, j, all_forced_m):
                all_forced_m = update_forced_move(i, j, all_forced_m)
            else:
                print("There are forced moves to do first: ", all_forced_m)
                continue
        else:
            # if there are no possible actions from that position
            legal_m = legal_moves(i, j, board)
            if not legal_m:
                print("No possible actions from", i, j)
                continue
        break

    # destination box for movement loop
    while True:
        # ask for destination box
        end_i, end_j = ask_box("Enter destination box: ")

        # check if is legal board position
        if not box_legal(end_i, end_j):
            print("Position out of the board")
            continue

        # try to perform the move
        if not try_move(i, j, end_i, end_j, all_forced_m, board):
            continue

        print_board(board)

        # if there are still move to do
        if not check_if_empty(all_forced_m):
            print("There are still forced moves to do:", all_forced_m)
            i = end_i
            j = end_j
            continue
        # end destination move loop
        break

    return eat_move, player_color, win_condition(player_color, board)
