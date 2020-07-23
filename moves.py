#!/usr/bin/env python3

from copy import copy, deepcopy

# ----------------------consts-------------------------------

SIZE = 8

EMPTY = " "
WHITE = ' \033[91m' + "W" + '\033[0m '#"W"
BLACK = ' \033[94m' + "B" + '\033[0m '#"B"
DAMAW = '\033[91m' + "W-D" + '\033[0m'#"W-D"
DAMAB = '\033[94m' + "B-D" + '\033[0m'#"B-D"

max_eat = 0
max_paths = []
max_eaten_order = []
max_is_dama = 0

# ----------------------------------------------------

# print a dama board
def print_board(board):
    print('    ', end = "")
    for c in range(SIZE):
        print('{:^4}'.format(c), end = "")
    print()
    print("   ---------------------------------")
    for r in range(SIZE):
        print("{:^3}".format(r), end = "")
        for c in range(SIZE):
            print('|{:^3}'.format(board[r][c]), end = "")
        print("|")
        print("   ---------------------------------")

def print_position(pos, color):
    c = '\033[94m'
    if color == WHITE:
        c = '\033[91m'

    i, j = pos
    print(" {}{},{}\033[0m".format(c, i, j), end = "")

def print_move(move, color):
    first = True

    for m in move:
        print_position(m[0], color)
        print(" ->", end = "")
        print_position(m[1], color)
        print(", ", end = "")
    print()

def print_movement(m, color):
    if not m:
        return

    print_position(m[0], color)
    print(" ->", end = "")
    print_position(m[1], color)
    print()

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

def is_dama(string):
    return string == DAMAB or string == DAMAW

# check if the pedina becomes dama
def check_new_dama(i, j, board):
    if board[i][j] == WHITE  and i == 0:
        board[i][j] = DAMAW
        return True

    if board[i][j] == BLACK and i == 7:
        board[i][j] = DAMAB
        return True

    return False

# check if there's only one color in the board
def win_condition(board):
    color = 0

    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY:
                continue
            if board[i][j] == WHITE or board[i][j] == DAMAW:
                if color == 0 or color == 1:
                    color = 1
                    continue
                else:
                    return False
            if board[i][j] == BLACK or board[i][j] == DAMAB:
                if color == 0 or color == 2:
                    color = 2
                    continue
                else:
                    return False

    return True

# returns list of legal moves from a position
# if there's no pedina in there returns empty list
# ASSUMPTION: (i, j) is a board position
def legal_moves(i, j, board):
    legal_m = []

    is_dama = board[i][j] == DAMAW or board[i][j] == DAMAB

    if board[i][j] == WHITE or is_dama:
        if box_legal(i - 1, j - 1) and board[i - 1][j - 1] == EMPTY:
            legal_m.append((i - 1, j - 1))
        if box_legal(i - 1, j + 1) and board[i - 1][j + 1] == EMPTY:
            legal_m.append((i - 1, j + 1))

    if board[i][j] == BLACK or is_dama:
        if box_legal(i + 1, j - 1) and board[i + 1][j - 1] == EMPTY:
            legal_m.append((i + 1, j - 1))
        if box_legal(i + 1, j + 1) and board[i + 1][j + 1] == EMPTY:
            legal_m.append((i + 1, j + 1))

    return legal_m

def check_if_empty(list_of_lists):
    for elem in list_of_lists:
        if elem:
            return False
    return True

def update_forced_moves(i, j, all_forced_m):
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

def movement(i, j, end_i, end_j, eat, board):
    board[end_i][end_j] = board[i][j]
    board[i][j] = EMPTY
    if eat:
        eat_pedina(i, j, end_i, end_j, board)

# changes the board moving a pedina.
# if and only if (end_i, end_j) are legal_moves
# if there's a forced move to do and it's not (end_i, end_j) it is an illegal move
def try_move(i, j, end_i, end_j, all_forced_m, board):
    eat = False

    # there's a forced move but it's not the selected one
    if not check_if_empty(all_forced_m):
        if search_forced_move(end_i, end_j, all_forced_m):
            all_forced_m = update_forced_moves(end_i, end_j, all_forced_m)
            eat = True
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

    movement(i, j, end_i, end_j, eat, board)
    check_new_dama(end_i, end_j, board)

    return True

# ORDINAMENTO:
# Avendo più possibilità di presa si debbono rispettare obbligatoriamente
# nell'ordine le seguenti priorità:
#DONE # è obbligatorio mangiare dove ci sono più pezzi;
#DONE # a parità di pezzi da prendere, tra pedina e dama si è obbligati a mangiare la dama;
#       inoltre se si può optare tra il mangiare di dama o di pedina
#       è obbligatorio mangiare con la dama;
#DONE # la dama sceglie la presa dove si mangiano più dame;
#DONE # a parità  di condizioni si mangia dove s'incontra prima la dama avversaria.

# TODO:
# Si vince per abbandono dell'avversario, che si trova in palese difficoltà,
# o quando si catturano o si bloccano tutti i pezzi avversari.

# TODO:
# Si pareggia in una situazione di evidente equilibrio finale per accordo
# dei giocatori o per decisione dell'arbitro a seguito del conteggio di 40 mosse
# richiesto da uno dei due giocatori.
# Il conteggio delle mosse si azzera e riparte da capo tutte le volte che
# uno dei due giocatori muove una pedina o effettua una presa.

def human_turn(player_color, board):
    all_forced_m = board_forced_moves(player_color, board)
    print("You are player: " + player_color)

    # first position loop
    while True:
        # ask for pedina to move
        i, j = ask_box("Enter box location: ")

        # check if there is a pedina of player color
        if not (box_legal(i, j) and color_check(i, j, player_color, board)):
            print("Not a legal position")
            continue

        # check if there are moves to do first
        if not check_if_empty(all_forced_m):
            if search_forced_move(i, j, all_forced_m):
                all_forced_m = update_forced_moves(i, j, all_forced_m)
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

    # destination move loop
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

    return win_condition(board)

# ----------------------------------------------------

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
    global max_eat
    global max_paths
    global max_eaten_order
    global max_is_dama

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

def copy_new_eaten(eaten, pedina):
    new_eaten = eaten.copy()
    new_eaten.append(pedina)

    return new_eaten

def copy_new_path(path, elem):
    new_path = path.copy()
    new_path.append(elem)

    return new_path

def copy_new_board(i, j, end_i, end_j, eat, board):
    new_board = deepcopy(board)
    movement(i, j, end_i, end_j, eat, new_board)

    return new_board

def board_forced_moves(color, board):
    clear_max()

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                calculate_forced_moves(i, j, color, [(i, j)], [], is_dama(board[i][j]), board)

    return max_paths

def check_direction(i, dir_i, j, dir_j, color, path, eaten, dama, board):
    if box_legal(i + dir_i, j + dir_j) and board[i + dir_i][j + dir_j] != EMPTY:
        if not color_check(i + dir_i, j + dir_j, color, board):
            # se la casella dx è occupata da una pedina avversaria
            if box_legal(i + dir_i*2, j + dir_j*2) and board[i + dir_i*2][j + dir_j*2] == EMPTY:
                # e la casella dopo è libera, posso mangiare
                if not is_dama(board[i + dir_i][j + dir_j]):
                    new_eaten = copy_new_eaten(eaten,"p") #ho mangiato una pedina semplice
                    new_path = copy_new_path(path, (i + dir_i*2, j + dir_j*2))
                    # copia della nuova board con la mossa effettuata
                    new_board = copy_new_board(i, j, i + dir_i*2, j + dir_j*2, True, board)
                    calculate_forced_moves(i + dir_i*2, j + dir_j*2, color, new_path, new_eaten, dama, new_board)
                    return False
                elif dama:
                    new_eaten = copy_new_eaten(eaten,"d") #ho mangiato una dama
                    new_path = copy_new_path(path, (i + dir_i*2, j + dir_j*2))
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
        register_path(path, eaten, dama)
        # aggiungi la mossa al set di mosse (poi verrà confrontata)
