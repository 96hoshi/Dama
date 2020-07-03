#!/usr/bin/env python3

# ----------------------consts-------------------------------

SIZE = 8

EMPTY = " "
WHITE = "W"
BLACK = "B"
DAMAW = "W_D"
DAMAB = "B_D"

# PEDINE:
# White
# Black
# White-Dama
# Black-Dama

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

# def index_legal(i):
#     return i in range(SIZE)

# check if the pedina is inside the board
def box_legal(i, j):
    return i in range(SIZE) and j in range(SIZE)

# check if there is a pedina of that color
def box_occupied(i, j, color, board):

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

# --------------------dama rules----------------------------

# check if the pedina becomes dama
def dama(i, j, board):
    if board[i][j] == WHITE  and j == 7:
        board[i][j] = DAMAW

    if board[i][j] == BLACK and j == 0:
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
#  if there's no pedina in there returns empty list
# ASSUMPTION: (i, j) is a board position
def legal_moves(i, j, board):
    legal_moves = []

    # # just to clarify, not necessary
    # if board[i][j] == EMPTY:
    #     return legal_moves

    is_dama = (board[i][j] == DAMAW) or (board[i][j] == DAMAB)

    if board[i][j] == WHITE or is_dama:
        if box_legal(i - 1, j - 1) and board[i - 1][j - 1] == EMPTY:
            legal_moves.append((i - 1, j - 1))
        if box_legal(i - 1, j + 1) and board[i - 1][j + 1] == EMPTY:
            legal_moves.append((i - 1, j + 1))

    if board[i][j] == BLACK or is_dama:
        if box_legal(i + 1, j - 1) and board[i + 1][j - 1] == EMPTY:
            legal_moves.append((i + 1, j - 1))
        if box_legal(i + 1, j + 1) and board[i + 1][j + 1] == EMPTY:
            legal_moves.append((i + 1, j + 1))

    return legal_moves


# tells if a pedina must do a certain move (eat)
# returns list of forced moves
# ASSUMPTION: (i, j) is a board position
def forced_moves(i, j, board):
    forced_moves = []

    if board[i][j] == WHITE:
        if box_legal(i - 1, j - 1) and board[i - 1][j - 1] == BLACK:
            if board[i - 2][j - 2] == EMPTY:
                forced_moves.append((i - 2, j - 2))
        if box_legal(i - 1, j + 1) and board[i - 1][j + 1] == BLACK:
            if board[i - 2][j + 2] == EMPTY:
                forced_moves.append((i - 2, j + 2))

    if board[i][j] == BLACK:
        if box_legal(i + 1, j - 1) and board[i + 1][j - 1] == WHITE:
            if board[i + 2][j - 2] == EMPTY:
                forced_moves.append((i + 2, j - 2))
        if box_legal(i + 1, j + 1) and board[i + 1][j + 1] == WHITE:
            if board[i + 2][j + 2] == EMPTY:
                forced_moves.append((i + 2, j + 2))

    return forced_moves

# removes the eaten pedina between two positions
def eat_pedina(i, j, end_i, end_j, board):
    delete_i = (i + end_i) // 2
    delete_j = (j + end_j) // 2

    board[delete_i][delete_j] = EMPTY

# changes the board moving a pedina
# if and only if (end_i, end_j) are legal_moves
# if there's a forced move to do and it's not end_i, end_j)
# then it is an illegal move
# CONTROLLI RIDONDANTI?
def move(i, j, end_i, end_j, board):
    # check if is legal board position
    if not box_legal(i, j):
        print("Position out of the board")
        return False

    # check if there's a pedina
    if board[i][j] == EMPTY:
        print("This bitch is empty yeet")
        return False

    # check if is legal board position
    if not box_legal(end_i, end_j):
        print("Position out of the board")
        return False

    f_moves = forced_moves(i, j, board)
    l_moves = legal_moves(i, j, board)

    # no moves allowed
    if (not f_moves) and (not l_moves):
        print("no2.0")
        return False

    # there's a forced move but it's not the selected one
    if f_moves:
        if not ((end_i, end_j) in f_moves):
            print("no3")
            return False
        else:
            eat_pedina(i, j, end_i, end_j, board)
    # there's a legal move but it's not the selected one
    elif l_moves:
        if not ((end_i, end_j) in l_moves):
            print("no4")
            return False

    board[end_i][end_j] = board[i][j]
    board[i][j] = EMPTY
    return True

# TODO: add rules for draw 


# -----------------main operations-------------------------

def main():
    # initialize the board
    board = [[EMPTY for c in range(SIZE)] for r in range(SIZE)]

    start_board(board)
    print_board(board)

    color = WHITE
    print("You are the whites")
    while True:
        # ask for pedina to move
        str_i, str_j = ask_input("Enter box location: ")
        if (not is_int(str_i)) and (not is_int(str_j)):
            print("Wrong input, correct usage: <int, int>")
            continue
        # cast input
        i = int(str_i)
        j = int(str_j)

        if not (box_legal(i, j, board) and box_occupied(i, j, color, board)):
            print("Not a legal position")
            continue


    # ask for input from user. It returns string
    # str_i, str_j = ask_input("Enter box location: ")
    # str_end_i, str_end_j = ask_input("Enter destination box: ")

    # # casting input data
    # # TODO: fare un try per il controllo dell'input
    # i = int(str_i)
    # j = int(str_j)

    # end_i = int(str_end_i)
    # end_j = int(str_end_j)

    # print(win_condition(WHITE, board))

    # board[4][2] = BLACK
    # print(forced_moves(5, 3, board))
    # eat_pedina(5,3,3,1,board)

    # print(move(5,1,4,2,board))
    # move(i, j, end_i, end_j, board)

    print_board(board)

if __name__ == "__main__":
    main()
