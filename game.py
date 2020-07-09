#!/usr/bin/env python3

from moves import *

# -----------------utility functions-------------------------

# starting board
def start_board(board):
    for c in range(SIZE):
        for r in range(3):
            if c % 2 == 0 and r % 2 == 0:
                board[r][c] = BLACK
            elif c % 2 != 0 and r % 2 != 0:
                    board[r][c] = BLACK

        for r in range(5, SIZE):
            if c % 2 == 0 and r % 2 == 0:
                board[r][c] = WHITE
            elif c % 2 != 0 and r % 2 != 0:
                    board[r][c] = WHITE

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

# --------------------dama rules----------------------------

# check if the pedina becomes dama
def check_dama(i, j, board):
    if board[i][j] == WHITE  and i == 0:
        board[i][j] = DAMAW

    if board[i][j] == BLACK and i == 7:
        board[i][j] = DAMAB

# check if there's only one color in the board
def win_condition(color, board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] == EMPTY or board[i][j] == color:
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


# changes the board moving a pedina.
# if and only if (end_i, end_j) are legal_moves
# if there's a forced move to do and it's not (end_i, end_j) it is an illegal move
def try_move(i, j, end_i, end_j, all_forced_m, board):
    # check if is legal board position
    if not box_legal(end_i, end_j):
        print("Position out of the board")
        return False

    l_moves = legal_moves(i, j, board)

    # there's a forced move but it's not the selected one
    if not check_if_empty(all_forced_m):
        if search_forced_move(end_i, end_j, all_forced_m):
            all_forced_m = update_forced_moves(end_i, end_j, all_forced_m)
            eat_pedina(i, j, end_i, end_j, board)
        else:
            print("There are forced moves to do: ", all_forced_m)
            return False


    # there's a legal move but it's not the selected one
    elif l_moves:
        if (end_i, end_j) not in l_moves:
            print("Not a legal move")
            return False

    board[end_i][end_j] = board[i][j]
    board[i][j] = EMPTY
    return True

# TODO: ORDINAMENTO
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

# -----------------main operations-------------------------

def main():
    # initialize the board
    board = [[EMPTY for c in range(SIZE)] for r in range(SIZE)]

    start_board(board)

    # board[4][4] = BLACK
    # board[5][5] = DAMAW
    board[5][7] = EMPTY
    board[4][6] = WHITE
    board[2][6] = EMPTY
    board[4][4] = WHITE
    board[3][5] = BLACK
    board[2][4] = EMPTY

    print_board(board)

    player_color = WHITE
    print("You are: " + player_color)
    # game loop
    while True:
        all_forced_m = board_forced_moves(player_color, board)
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

            # try to perform the move
            if not try_move(i, j, end_i, end_j, all_forced_m, board):
                continue

            check_dama(end_i, end_j, board)

            print_board(board)

            # if there are still move to do
            if not check_if_empty(all_forced_m):
                print("There are still forced moves to do:", all_forced_m)
                i = end_i
                j = end_j
                continue
            # end destination move loop
            break

        if win_condition(player_color, board):
            print("Player " + player_color + " wins!")
            break

        if player_color == WHITE:
            player_color = BLACK
        else:
            player_color = WHITE

        print("You are: " + player_color)

if __name__ == "__main__":
    main()
