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


# returns teh opposite color
def opposite_color(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def is_dama(string):
    return string == DAMAB or string == DAMAW


# do a type check to the info submitted by the user
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


# ask to the user coordinates for the box
def ask_box(string):
    str_i, str_j = ask_input(string)
    while (not is_int(str_i)) and (not is_int(str_j)):
        print("Wrong input, correct usage: <int, int>")
        continue

    i = int(str_i)
    j = int(str_j)
    return i, j


def is_only_color(color, board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] is not EMPTY:
                if not color_check(i, j, color, board):
                    return False
    return True


# check if is possible to eat at least a pawn from a position (i, j)
def can_eat(i, dir_i, j, dir_j, color, board):
    if box_legal(i + dir_i, j + dir_j):
        if board[i + dir_i][j + dir_j] != EMPTY:
            # check if there is a box with a piece
            if not color_check(i + dir_i, j + dir_j, color, board):
                if box_legal(i + dir_i * 2, j + dir_j * 2):
                    if board[i + dir_i * 2][j + dir_j * 2] == EMPTY:
                        # check if is possible to perform a eat move
                        if not is_dama(board[i + dir_i][j + dir_j]):
                            # it's a simple pawn, I can eat
                            return True
                        elif is_dama(board[i][j]):
                            # I can eat a dama if I'm a dama
                            return True
    return False


# returns True if the player of the selected color has at least a move to do
# False otherwise
def has_player_moves(color, board):
    for i in range(SIZE):
        for j in range(SIZE):
            if board[i][j] is not EMPTY:
                if color_check(i, j, color, board):
                    # if the enemy can do a movement then it's not a win
                    if legal_moves(i, j, board):
                        return True

                    # if the enemy can eat then it's not a win condition
                    dir_i = 1
                    if color == WHITE:
                        dir_i = -1
                    if can_eat(i, dir_i, j, -1, color, board):
                        return True
                    if can_eat(i, dir_i, j, 1, color, board):
                        return True

                    if is_dama(board[i][j]):
                        dir_i *= -1
                        if can_eat(i, dir_i, j, -1, color, board):
                            return True
                        if can_eat(i, dir_i, j, 1, color, board):
                            return True
    return False


# return True if the player_color is the winner.
# A player wins if and only if he is the only color on the board
# or the enemy has no more moves to perform
def is_player_winner(player_color, board):
    if is_only_color(player_color, board):
        return True

    enemy_color = opposite_color(player_color)
    return not has_player_moves(enemy_color, board)


# returns the list of legal moves from a position.
# if there is no pawn returns empty list
# (i, j) is a board position
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


# slide a forced move performed
def update_forced_move(i, j, all_forced_m):
    updated_forced_m = []
    for path in all_forced_m:
        if path[0] == (i, j):
            path.pop(0)
            updated_forced_m.append(path)

    return updated_forced_m


# check if the selected move is contained
# in the list of forced moves already calculated
def search_forced_move(i, j, all_forced_m):
    for path in all_forced_m:
        if path[0] == (i, j):
            return True

    return False


# perform a single movement froma (i,j) to (end_i,end_j)
# removing enemy pawn if needed, and checking if there is
# a promotion for a new dama
def movement(i, j, end_i, end_j, board):
    board[end_i][end_j] = board[i][j]
    board[i][j] = EMPTY

    # check if there is a new dama
    if end_i == 0 and board[end_i][end_j] == WHITE:
        board[end_i][end_j] = DAMAW
    elif end_i == 7 and board[end_i][end_j] == BLACK:
        board[end_i][end_j] = DAMAB

    # check if an eat move is performed
    diff_i = abs(i - end_i)
    diff_j = abs(j - end_j)
    if diff_i == 2 or diff_j == 2:
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


# evaluate a move and register it if it's better
# or equal than the saved one
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
            # both are damas
        elif max_is_dama and dama:

            # compare which have eaten more damas
            d_eaten = eaten.count("d")
            d_max_eaten = max_eaten_order.count("d")
            if d_eaten > d_max_eaten:
                update_max(n_eat, path, eaten, dama)
            # if both have the same number of eaten damas
            elif d_eaten == d_max_eaten:
                if d_eaten > 0:

                    # find the path that eat a dama first
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


# returns a list of lists of forced moves
def board_forced_moves(color, board):
    clear_max()

    for i in range(SIZE):
        for j in range(SIZE):
            if color_check(i, j, color, board):
                calculate_forced_moves(
                    i, j, color, [(i, j)], [], is_dama(board[i][j]), board)

    return max_paths


# check recursively if an eat move can be performed in a direction
# editing and saving the path
def check_direction(i, dir_i, j, dir_j, c, path, eaten, dama, board):
    if box_legal(i + dir_i, j + dir_j):
        if board[i + dir_i][j + dir_j] != EMPTY:
            # if the box is occupied by the enemy
            if not color_check(i + dir_i, j + dir_j, c, board):
                # if the box after is empty
                if box_legal(i + dir_i * 2, j + dir_j * 2):
                    if board[i + dir_i * 2][j + dir_j * 2] == EMPTY:
                        # it's not a dama
                        if not is_dama(board[i + dir_i][j + dir_j]):
                            # a pawn is eaten
                            n_e = copy_new_eaten(eaten, "p")
                            n_p = copy_new_path(
                                path, (i + dir_i * 2, j + dir_j * 2))
                            # copy of the new board with move performed
                            n_b = copy_new_board(
                                i, j, i + dir_i * 2, j + dir_j * 2, board)
                            calculate_forced_moves(
                                i + dir_i * 2, j + dir_j * 2, c, n_p, n_e, dama, n_b)
                            return False
                        # if it's a dama and I'm a dama too
                        elif dama:
                            # a dama was eaten
                            n_e = copy_new_eaten(eaten, "d")
                            n_p = copy_new_path(
                                path, (i + dir_i * 2, j + dir_j * 2))
                            n_b = copy_new_board(
                                i, j, i + dir_i * 2, j + dir_j * 2, board)
                            calculate_forced_moves(
                                i + dir_i * 2, j + dir_j * 2, c, n_p, n_e, dama, n_b)
                            return False

    return True


# check in all direction if a forced moved is possible form a position.
# in the end register it
def calculate_forced_moves(i, j, color, path, eaten, dama, board):
    stop = True
    dir_i = 1
    if color == WHITE:
        dir_i = -1

    # if dx then dir_j = -1
    dx = -1
    # if sx then dir_j = 1
    sx = 1

    stop = check_direction(i, dir_i, j, dx, color, path, eaten, dama, board)
    stop = check_direction(i, dir_i, j, sx, color, path, eaten, dama, board)

    # if I'm a dama check the other two directions
    if dama:
        dir_i *= -1
        stop = check_direction(i, dir_i, j, dx, color,
                               path, eaten, dama, board)
        stop = check_direction(i, dir_i, j, sx, color,
                               path, eaten, dama, board)

    # add the move to the set
    if stop and len(path) > 1:
        register_path(path, eaten, dama)


# handle a human turn.
# ask for pawn to move, moves to be performed and check if them
# follow the dama rules
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

    return eat_move, player_color, is_player_winner(player_color, board)
