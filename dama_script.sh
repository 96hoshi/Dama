#!/bin/bash

# permutation of all games simulations
for i in `seq 0 4`; do
	for j in `seq 0 4`; do
		# doing 40 games
		for k in `seq 0 7`; do

			# launch 5 games at time
			for p in `seq 0 4`; do
				python3 game.py --white_depth ${i} --black_depth ${j} > /dev/null &
				pids[${p}]=$!
			done

			# wait for all pids
			for pid in ${pids[*]}; do
				wait $pid
			done
		done
	done
done

python3 time_test.py
