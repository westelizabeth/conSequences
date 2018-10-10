
#!/usr/bin/python3
import sys
import re
import fnmatch
import argparse
import subprocess
import os.path
from os import path
import math

PERCENT = .40

def count_alg(filename, linecount):
    count = -1
    line_count = 0
    with open(filename) as file:
        for line in file:
            #print line
            line_count +=1
            if "OUR Scores:" in line or not line:
                if count == -1 and linecount == line_count: # found the start of the block
                    count = 0
                elif count > 1: # found the start of the end
                    break
            elif count >= 0: # inside the block
                count += 1
    count -= 1
    return(count)

def count(filename):
    count = -1
    with open(filename) as file:
        for line in file:
            if "BLAST Scores:" in line or "OUR Scores:" in line or not line:
                if count == -1: # found the start of the block
                    count = 0
                elif count > 1: # found the start of the end
                    break
            elif count >= 0: # inside the block
                count += 1
    count -= 1
    return(count)

def add_blast_set(bset, outf):
    outf.write("\nWHOLE Blast set:\n")
    for x in bset:
        outf.write("%s, " %x)
    outf.write("\n " )
def compare_PDBID(blist, algorithm_list, outf):
    hit = set(algorithm_list).intersection(blist)
    miss = set(algorithm_list).difference(blist)
    outf.write("In Blast set\n")
    for x in hit:
        outf.write("%s, " %x)
    outf.write("\n")
    outf.write("Not in Blast set\n")
    for y in miss:
        outf.write("%s, " %y)
    outf.write("\n " )
    #append this
def make_set(potential_list):
    potential_list = potential_list.lstrip("0123456789 ")
    the_list = re.sub(": ", "", potential_list).split()
    return the_list

def main(args):
    infile, outfile = args[0], args[1]
    k = "w+"
    if os.path.exists("./analyzed.txt"):
        k = "a"
    with open(infile) as inf, open(outfile, k) as outf:
        outf.write("------------------------------------------------------------------------\n")
        outf.write("------------------------------------------------------------------------\n")
        outf.write("------------------------------------------------------------------------\n")
        l1 = inf.readline()
        l2 = inf.readline()
        outf.write("%s"%l1)
        outf.write("%s"%l2)
        blast_set = []
        alg_set = []
        current_line = 2

        for line in inf:
            current_line += 1
            if not line == "\n":
                if "BLAST Scores:" in line:
                    num_of_blast_lines = count(args[0])
                    blast_num = num_of_blast_lines * PERCENT
                    blast_num = int(math.ceil(blast_num))
                    #print blast_num # this is the number of lines we need to make the blast pool
                    if blast_num > 0:
                        for x in range(blast_num):
                            blast_line = inf.readline()
                            current_line +=1
                            temp_blast_set = make_set(blast_line)
                            blast_set.extend(temp_blast_set)
                        add_blast_set(blast_set, outf)
                    else:
                        outf.write("No Blast Set\n")
                        print("No blast set")
                        blast_set.append("DNE")

                elif "OUR Scores:" in line:
                    alg_set = []
                    num_of_lines = count_alg(args[0], current_line)
                    num = num_of_lines * PERCENT
                    num = int(math.ceil(num))
                    #print numnext
                    if num > 0:
                        for x in range(num):
                            alg_line = inf.readline()
                            current_line +=1
                            temp_set = make_set(alg_line)
                            alg_set.extend(temp_set)
                        compare_PDBID(blast_set, alg_set, outf)
                outf.write("\n")
    inf.close()
    outf.close()



if __name__ == "__main__":
    import sys
    print("here")
    main(sys.argv[1:])
