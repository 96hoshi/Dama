#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

MIN_SIZE = 0
MAX_SIZE = 7

def translate_res(string):
    if string == "Win":
        return 0
    if string == "Lose":
        return 1
    else:
        return 2

def get_wins_per(c):
    wins_percent = []

    for i in range(MIN_SIZE, MAX_SIZE):
        wins = []
        for j in range(MIN_SIZE, MAX_SIZE):
            total = np.sum(results[c][i][j])
            if total == 0:  w = 0
            else: w = (results[c][i][j][0] / total) * 100
            wins.append(int(w))
        wins_percent.append(wins)
    return wins_percent

blacks = []
whites = []
games = []

with open('tests00.txt', 'r') as f:
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

# 0.WHITE 1.AVG_TIME 2.MAX_TIME 3.MIN_TIME 4.DEPTH 5.RESULT
for elem in whites:
    print(elem)
# BLACK AVG_TIME MAX_TIME MIN_TIME DEPTH RESULT
for elem in blacks:
    print(elem)
# 0.GAME 1.DEPTH_W 2.DEPTH_B 3.TIME 4.RESULT
for elem in games:
    print(elem)

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
# remove outliners
for i in range(MIN_SIZE, MAX_SIZE):
    depths[i].remove(np.max(depths[i]))
    depths[i].remove(np.min(depths[i]))
    time_depths.append(np.median(depths[i]))

plt.plot(time_depths)
plt.xlabel('depth')
# plt.xlim(0, 6)
plt.ylabel('time (nsec)')
plt.yscale('log')
plt.savefig('plots/time-per-depth.png')

# RESULTS PERCENTAGE PER DEPTH
results = []

# result[0] è WHITE
# result[1] è BLACK

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

white_wins = get_wins_per(0)
black_wins = get_wins_per(1)

for i in range(MIN_SIZE, MAX_SIZE):
    print(i, white_wins[i])
print("-"*40)
trans_black_wins = np.transpose(black_wins)
for i in range(MIN_SIZE, MAX_SIZE):
    print(i, black_wins[i])


# column_headers = [0, 1, 2, 3, 4]
# row_headers = [" 0 ", " 1 ", " 2 ", " 3 ", " 4 "]
# rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))
# ccolors = plt.cm.BuPu(np.full(len(column_headers), 0.1))

# plt.figure(linewidth=3,
#            tight_layout={'pad':1},
#            figsize=(5,3)
#           )

# the_table = plt.table(cellText=white_wins,
#                       rowLabels=row_headers,
#                       rowColours=rcolors,
#                       rowLoc='right',
#                       colLabels=column_headers,
#                       colColours=ccolors,
#                       loc='center',
#                       cellLoc='center')

# # Scaling is the only influence we have over top and bottom cell padding.
# # Make the rows taller (i.e., make cell y scale larger).
# the_table.scale(0.8, 1.4)

# # Hide axes
# ax = plt.gca()
# ax.get_xaxis().set_visible(False)
# ax.get_yaxis().set_visible(False)

# # Hide axes border
# plt.box(on=None)

# # Add title
# plt.suptitle("White's win Percentage per depth")

# # Force the figure to update, so backends center objects correctly within the figure.
# # Without plt.draw() here, the title will center on the axes and not the figure.
# plt.draw()

# # Create image. plt.savefig ignores figure edge and face colors, so map them.
# fig = plt.gcf()
# # plt.show()
# plt.savefig('plots/win-percentage.png')
