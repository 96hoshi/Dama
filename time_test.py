#!/usr/bin/env python3

# import numpy as np


# a = []
# i = 0

# with open('tests.txt', 'r') as f:
#     for line in f:
#         strings = line.split()
#         e0 = strings[0]
#         e1 = float(strings[1])
#         e2 = float(strings[2])
#         e3 = float(strings[3])
#         e4 = int(strings[4])
#         e5 = strings[5]
#         record = (e0, e1, e2, e3, e4, e5)

#         a.append(record)


#     for elem in a:
#         print(elem)

# import numpy as np


# turns = []
# games = []

# with open('tests01.txt', 'r') as f:
#     for line in f:
#         strings = line.split()
#         e0 = strings[0]
#         if e0 == "GAME":
#             e1 = int(strings[1])
#             e2 = int(strings[2])
#             e3 = float(strings[3])
#             e4 = strings[4]
#             record = (e0, e1, e2, e3, e4)
#             games.append(record)
#         else:
#             e1 = float(strings[1])
#             e2 = float(strings[2])
#             e3 = float(strings[3])
#             record = (e0, e1, e2, e3)
#             turns.append(record)

#     for elem in turns:
#         print(elem)
#     for elem in games:
#         print(elem)

import numpy as np


turns = []
games = []

with open('tests02.txt', 'r') as f:
    for line in f:
        strings = line.split()
        e0 = strings[0]
        if e0 == "GAME":
            e1 = int(strings[1])
            e2 = int(strings[2])
            e3 = float(strings[3])
            e4 = strings[4]
            record = (e0, e1, e2, e3, e4)
            games.append(record)
        else:
            e1 = float(strings[1])
            e2 = float(strings[2])
            e3 = float(strings[3])
            e4 = int(strings[4])
            e5 = strings[5]
            record = (e0, e1, e2, e3, e4, e5)
            turns.append(record)

    for elem in turns:
        print(elem)
    for elem in games:
        print(elem)
