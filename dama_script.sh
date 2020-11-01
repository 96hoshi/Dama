#!/bin/bash

FILE=final.txt
MAX_DEPTH=6

pedine=5
dame=8
back=4.0
box=2.5
row=0.5
vuln=-3.0
protec=3.0
promot=0.65

# permutation of all games simulations
for i in `seq 0 $MAX_DEPTH`; do
	for j in `seq 0 $MAX_DEPTH`; do
		# doing 50 games
		for k in `seq 0 9`; do

			# launch 5 games at time
			for p in `seq 0 4`; do
				python3 game.py --f $FILE --w $pedine $dame $back $box $row $vuln $protec $promot --white_depth ${i} --black_depth ${j} > /dev/null &
				pids[${p}]=$!
			done

			# wait for all pids
			for pid in ${pids[*]}; do
				wait $pid
			done

			sleep 30
		done
	done
done

echo  $FILE $pedine $dame $back $box $row $vuln $protec $promot >> results.txt
python3 time_test.py $FILE $MAX_DEPTH >> results.txt
