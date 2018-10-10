#!/usr/bin/env python3
"""Program for testing constrained sequence alignm"""
import subprocess
from pprint import pprint
import json
import argparse
import sys
import string
import random
import datetime
from constrain_align import run_blast

AMINO_ACIDS = "GAVLIPFYWSTCMNQKRHDE"

NUM_PRINT = 50

def main():
    """Main function"""
    args = parse_arguments()
    if (args.random is None):
        seqs = args.specific
    elif (args.specific is None):
        seqs = args.random
    elif (args.random is None and args.specific is None):
        raise ValueError("Please use either -r or -s")
    else:
        raise ValueError("Pleae only use one of -r or -s")
    weights = args.w or [random.randrange(1,20) for _ in seqs]
    if weights and len(weights) != len(seqs):
        raise ValueError('Number of weights and number of sequences must be of same length')
    aminos = args.aminos
    if aminos:
        if not all(x in AMINO_ACIDS for x in aminos):
            raise ValueError('One of your amino acids is funny. Please choose amino acids from "{}"'.format(AMINO_ACIDS))
    outfile = open(args.out, 'w') if args.out else sys.stdout
    if (args.random):
        test_seqs = [make_seqs(s, amino_acids=aminos)for s in seqs]
    else:
        test_seqs = seqs
    print('Sequences are:', file=outfile)
    print(test_seqs, file=outfile)
    combined_seq = ""
    for x in test_seqs:
        combined_seq += x
    print("Combined sequence for BLAST:", file=outfile)
    print(combined_seq + '\n',file=outfile)

    #Only print top NUM_PRINT results
    blast_items = run_blast(combined_seq)
    print('The blast says:', file=outfile)
    bresults = len(blast_items)
    #if NUM_PRINT < bresults:
    #   bresults = NUM_PRINT
    if len(blast_items) > 0:
        [print(blast_items[x], file=outfile) for x in range(0, bresults)]
    #prints all blast results
    #[print(x, file=outfile) for x in blast_items]

    # Only print top NUM_PRINT results
    #want top 10 distinct scored 
    our_program = subprocess.run(['python3', 'constrain_align.py', '-s'] + [x + ':{}'.format(w) for x, w in zip(test_seqs, weights)], stdout=subprocess.PIPE)
    print('\nOur program says:', file=outfile)
    our_items = our_program.stdout.decode('utf-8').split('\n')
    oresults = int(len(our_items)/4)
    #if NUM_PRINT < oresults:
    #    oresults = NUM_PRINT
    if len(our_items) > 0:
        idx = 0
        limit = oresults*4
        while idx < limit:
            print(our_items[idx], file=outfile)
            idx += 4
    #prints all our programs results
    #[print(x, file=outfile) for x in our_program.stdout.decode('utf-8').split('\n')]
    print('-'*80, file=outfile)

def make_seqs (seq_len, amino_acids=None):
    amino_acids = amino_acids or AMINO_ACIDS
    return ''.join(random.choice(amino_acids) for x in range(seq_len))

def parse_arguments():
    """Parse command line arguments to the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', "--specific", help="Specify a specific amino acid sequence to test", nargs="*", default=None)
    parser.add_argument('-r',
        "--random", help="Specify the length of random sequnece you want to test", nargs='*', type=int, default=None)
    parser.add_argument('-w', "-weight",
                        help="Specify the weight you want to use for the constrained alignment", nargs='*', type=int, default=None)
    parser.add_argument('-o', '--out', default=None,
                        help='Specify output filename.')
    parser.add_argument('-a', '--aminos', default=None, type=str,
                        help='Specify amino acids.')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
