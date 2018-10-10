#!/usr/bin/python3
import sys
import re
import fnmatch
import argparse
import subprocess
import os
sys.path.insert(0, 'textfiles')
import analyze
import parse

OUTFILE = "textfiles/Structures.txt"

#list comprehension
#automate your stuff

parameter_sweep_two_subsequences = "./paramsweep.sh"
parameter_sweep_three_subsequences = "./psweep3.sh"
parameter_sweep_four_subsequences = "./psweep4.sh"
#max jump filename.txt seq seq seq....
# sys.argv[0]=runParamSweep.py
# sys.argv[1]=max
# sys.argv[2]=jump
# sys.argv[3]=filename
# sys.argv[4] and more are sequences
#
sys_len = len(sys.argv)
if (sys.argv[1].isdigit() and sys.argv[2].isdigit() and (sys_len >= 6)):
	for x in range(4, sys_len):
		print(sys.argv[x])
		if (not sys.argv[x].isupper() and not sys.argv[x].isalpha()and fnmatch.fnmatch(sys.argv[3], '*.txt')):
			print("Sequences need to be all uppercase letters")
			sys.exit(0)
	num_seq = sys_len-4
	arg = sys.argv
	if(num_seq == 2):
		arg[0]= parameter_sweep_two_subsequences
	elif(num_seq == 3):
		arg[0]=	parameter_sweep_three_subsequences
	elif(num_seq == 4):
		arg[0] = parameter_sweep_four_subsequences
	else:
		print("currently cant handle more than four subsequences")
		sys.exit(0)
	#print(*arg, sep='\n')
	subprocess.call(arg)


	parsed_extension = "_parsed.txt"

	input1 = "textfiles/"+sys.argv[3]
	filename = input1[:-4]
	input2 = filename + parsed_extension

	inputarr1 = [input1, input2]
	inputarr2 = [input2, OUTFILE]


	parse.main(inputarr1)
	analyze.main(inputarr2)
	print("Analyzed")
