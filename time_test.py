#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt

MIN_SIZE = 0

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('size')
args = parser.parse_args()

MAX_SIZE = int(args.size) + 1


def translate_res(string):
    if string == "Win":
        return 0
    if string == "Lose":
        return 1
    else:
        return 2


def get_res_percent(color, res):
    res_percent = []

    for i in range(MIN_SIZE, MAX_SIZE):
        result = []
        for j in range(MIN_SIZE, MAX_SIZE):
            total = np.sum(results[color][i][j])
            if total == 0:
                w = 0
            else:
                w = (results[color][i][j][res] / total) * 100
            result.append(int(w))
        res_percent.append(result)
    return res_percent


blacks = []
whites = []
games = []

with open(args.filename, 'r') as f:
    for line in f:
        strings = line.split()
        e0 = strings[0]
        if e0 == "GAME":
            e1 = int(strings[1])
            e2 = int(strings[2])
            e3 = int(strings[3])
            e4 = strings[4]
            record = (e0, e1, e2, e3, e4)
            games.append(record)
        else:
            e1 = float(strings[1])
            e2 = int(strings[2])
            e3 = int(strings[3])
            e4 = int(strings[4])
            e5 = strings[5]
            record = (e0, e1, e2, e3, e4, e5)
            if e0 == "WHITE":
                whites.append(record)
            else:
                blacks.append(record)

# # 0.WHITE 1.AVG_TIME 2.MAX_TIME 3.MIN_TIME 4.DEPTH 5.RESULT
# # BLACK AVG_TIME MAX_TIME MIN_TIME DEPTH RESULT
# # 0.GAME 1.DEPTH_W 2.DEPTH_B 3.TIME 4.RESULT

depths = []
for i in range(MIN_SIZE, MAX_SIZE):
    a_list = []
    depths.append(a_list)

n_games = len(games)
for i in range(0, n_games):
    for k in range(MIN_SIZE, MAX_SIZE):
        if whites[i][4] == k:
            depths[k].append(whites[i][1])
            break

for i in range(0, n_games):
    depths[blacks[i][4]].append(blacks[i][1])

# --------------------TESTS----------------------------

# TIME PER DEPTH
time_depths = []
# remove outliaers
for i in range(MIN_SIZE, MAX_SIZE):
    depths[i].remove(np.max(depths[i]))
    depths[i].remove(np.min(depths[i]))
    time_depths.append(np.median(depths[i]) / 1e6)

print(time_depths)

plt.plot(time_depths, marker="o")
plt.xlabel('depth')
plt.ylabel('time (msec)')
plt.yscale('log')
plt.ylim(1e-1, 1e4)
plt.savefig('plots/time-per-depth.png')

# RESULTS PERCENTAGE PER DEPTH
results = []

# result[0] is WHITE
# result[1] is BLACK

# results[color][depth][depth_enemy][result]
for i in range(0, 2):
    a_depth = []
    results.append(a_depth)
    for j in range(MIN_SIZE, MAX_SIZE):
        enemy_depth = []
        a_depth.append(enemy_depth)
        for k in range(MIN_SIZE, MAX_SIZE):
            a_res = [0] * 3
            enemy_depth.append(a_res)

# 0.GAME 1.DEPTH_W 2.DEPTH_B 3.TIME 4.RESULT
for i in range(0, len(games)):
    elem = games[i]
    res_w = translate_res(whites[i][5])
    res_b = translate_res(blacks[i][5])

    results[0][elem[1]][elem[2]][res_w] += 1
    results[1][elem[2]][elem[1]][res_b] += 1

white_wins = get_res_percent(0, 0)
black_wins = get_res_percent(1, 0)

white_loses = get_res_percent(0, 1)
black_loses = get_res_percent(1, 1)

white_draws = get_res_percent(0, 2)
black_draws = get_res_percent(1, 2)


n_test = len(games) / (MAX_SIZE * MAX_SIZE)

# print all results
print("TEST: {} games played, {} per type, Max depth: {}".format(len(games), int(n_test), MAX_SIZE-1))
print("     ", end="")
for i in range(MIN_SIZE, MAX_SIZE):
    print("{:^15}|".format(str(i)), end="")
print()
print("     ", end="")
for i in range(MIN_SIZE, MAX_SIZE):
    print(" {:3}  {:3} |".format("  W", "  D"), end="")
print()
for i in range(MIN_SIZE, MAX_SIZE):
    print("{:3}: ".format(i), end= "")
    for j in range(MIN_SIZE, MAX_SIZE):
        print(" {:3}, {:3} |".format(white_wins[i][j], white_draws[i][j]), end="")
    print()
print("-"*85)
for i in range(MIN_SIZE, MAX_SIZE):
    print("{:3}: ".format(i), end= "")
    for j in range(MIN_SIZE, MAX_SIZE):
        print(" {:3}, {:3} |".format( black_wins[i][j], black_draws[i][j]), end="")
    print("")

# print draw and win results
# print("TEST: {} games played, {} per type, Max depth: {}".format(len(games), int(n_test), MAX_SIZE-1))
# print("     ", end="")
# for i in range(MIN_SIZE, MAX_SIZE):
#     print("{:^15}|".format(str(i)), end="")
# print()
# print("     ", end="")
# for i in range(MIN_SIZE, MAX_SIZE):
#     print(" {:3}  {:3}  {:3} |".format("  W", "  L", "  D"), end="")
# print()
# for i in range(MIN_SIZE, MAX_SIZE):
#     print("{:3}: ".format(i), end= "")
#     for j in range(MIN_SIZE, MAX_SIZE):
#         print(" {:3}, {:3}, {:3} |".format(white_wins[i][j], white_loses[i][j], white_draws[i][j]), end="")
#     print()
# print("-"*85)
# for i in range(MIN_SIZE, MAX_SIZE):
#     print("{:3}: ".format(i), end= "")
#     for j in range(MIN_SIZE, MAX_SIZE):
#         print(" {:3}, {:3}, {:3} |".format( black_wins[i][j], black_loses[i][j], black_draws[i][j]), end="")
#     print("")
# print()
