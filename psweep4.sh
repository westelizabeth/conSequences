#!/bin/bash

#input
# [max-score] [score-incramentor] [seq1] [seq2] [filename]

#first command to be the ceiling
#second command is the jumps
max=${1}
jumps=${2}
fileName=${3}
#retrieve 4 sequences
seq1=${4}
seq2=${5}
seq3=${6}
seq4=${7}
#creates new file
touch textfiles/$fileName
echo $max $jumps $seq1 $seq2 $seq3 $seq4 > textfiles/$fileName
#increments the first
for (( x=1; x <= $max+1; x+=$jumps)) do
  for (( y=1; y <= $max+1; y+=$jumps)) do
    for (( z=1; z <= $max+1; z+=$jumps)) do
      for (( r=1; r <= $max+1; r+=$jumps)) do
        echo $seq1 $seq2 $seq3 $seq4 $x $y $z $r
        output=$(./test_script.py -s ${seq1} ${seq2} ${seq3} ${seq4} -w $x $y $z $r)
        echo $output >> textfiles/$fileName
      done;
    done;
  done;
done;
