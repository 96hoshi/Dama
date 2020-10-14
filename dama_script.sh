#!/bin/bash

# #same depth games
# for i in `seq 0 5`; do
# 	for k in `seq 1 10`; do
# 		python3 game.py --white_depth ${i} --black_depth ${i}
# 	done
# done

# 
for i in `seq 0 6`; do
	for j in `seq 0 6`; do
		for k in `seq 1 10`; do
			python3 game.py --white_depth ${i} --black_depth ${j} 
		done
	done
done

#
for i in `seq 0 6`; do
	for j in `seq 0 6`; do
		for k in `seq 1 10`; do
			python3 game.py --white_depth ${j} --black_depth ${i}
		done
	done
done

