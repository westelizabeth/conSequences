#!/usr/bin/python3

import csv
import re
import sys
def main(args):
    blast = False
    infile, outfile = args[0], args[1]
    with open(infile) as inf, open(outfile,"w+") as outf:
            input_seq = inf.readline()
            combined_seq = ''.join([i for i in input_seq if not i.isdigit()]).replace(" ","")
            outf.write("Input parameters: [max w/jump size] %s"%input_seq)
            outf.write("Combined sequence for BLAST: %s" %combined_seq)
            for line in inf:
                if not line == "\n":
                    line = re.sub(":","",line)
                    line = re.sub(",","",line)
                    line = re.sub("\|","",line)
                    parse_blast, non_blast = line.split("Our program says ")
                    if not blast:
                        parse_BLAST(parse_blast, outf)
                        blast = True
                    if "Our program says: ---" not in non_blast:
                        skip_BLAST(non_blast, outf)
            outf.write("\n")
    inf.close()
    outf.close()

def parse_BLAST(line, outf):
    #strip to bare minimum
    line = line.split('The blast says ', 1)[-1]
    line = re.sub("bit_score........", "",line)
    line = re.sub("Score ", "", line)
    #stripped
    outf.write("\nBLAST Scores:")
    index_lst = list(re.finditer(" \d+ ", line))
    score = 0
    pdb_id = ""
    for i in range(len(index_lst)):
        start_idx = index_lst.__getitem__(i).span()[0] + 1
        end_idx = index_lst.__getitem__(i).span()[1]
        number = int(line[start_idx : end_idx])
        if(number != score):
            outf.write("\n%d  : " %number)
            score = number
            pdb_id = line[start_idx -7: start_idx-1]
            outf.write("%s "%pdb_id)
        else:
            pdb_id = line[start_idx -7: start_idx-1]
            outf.write("%s "%pdb_id)


def skip_BLAST(line, outf):
    #strip to bare minimum
    line = re.sub("Gaps \[[^\]]*\]", "", line)
    line = re.sub("  ", " ", line)
    line = re.sub("Score ", "", line)
    #stripped to bare minimum
    outf.write("\n\nOUR Scores:")
    index_lst = list(re.finditer(" \d+ ", line))
    score = 0
    pdb_id = ""
    for i in range(len(index_lst)):
        start_idx = index_lst.__getitem__(i).span()[0] + 1
        end_idx = index_lst.__getitem__(i).span()[1]
        number = int(line[start_idx : end_idx])
        if(number != score):
            outf.write("\n%d  : " %number)
            score = number
            pdb_id = line[start_idx -7: start_idx-1]
            outf.write("%s "%pdb_id)
        else:
            pdb_id = line[start_idx -7: start_idx-1]
            outf.write("%s "%pdb_id)
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
