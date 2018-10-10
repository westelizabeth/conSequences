#!/usr/bin/env python3
"""Program for constrained multiple sequence alignment."""
import subprocess
from pprint import pprint
import json
import argparse
import sys
import string


def main():
    """Main function"""
    args = parse_arguments()
    protein = args.pdbid
    idx_seq = args.subsequences
    str_seq = args.seq
    outfile = open(args.out, 'w') if args.out else sys.stdout

    fasta_sequences = load_fasta(open(args.fasta_file))
    # Set static variables
    ScoredResult.fasta_sequences = fasta_sequences
    SubsequenceQuery.fasta_sequences = fasta_sequences

    # Parse input (x:x:x or AAAAA:x) to create subsequences
    subseq_query = [SubsequenceQuery(protein, y) for y in idx_seq + str_seq]

    # List of amino acid subsequences
    subsequences = [x.sequence for x in subseq_query]

    # Set static vars
    ScoredResult.subseq_query = subseq_query
    ScoredResult.subsequences = subsequences

    # Set max possible score for all subsequences
    ScoredResult.max_score = sum(
        [(x.end_idx - x.start_idx) * x.weight for x in subseq_query])

    blast_results = set()
    for seq in subsequences:
        temp = run_blast(seq) # List of blast results
        blast_results.update(temp) # adds blast results to set

    scored_results = []

    # Creates a list of scored unique pdbids
    for pdbid in set([x.pdb_id for x in blast_results]):
        scored_results.append(ScoredResult(pdbid))
    scored_results.sort(reverse=True)

    for result in scored_results:
        print('{} | Score: {}, Gaps: {}'.format(result.pdb_id, result.score, result.gaps), file=outfile)
        print('{}'.format(fasta_sequences[result.pdb_id]), file=outfile)
        print('{}'.format(result.match_str()), file=outfile)
        print(file=outfile)


class SubsequenceQuery(object):
    """Store subsequences for searching"""
    fasta_sequences = None

    def __init__(self, protein, seq_query):
        seq_split = seq_query.split(':')
        if len(seq_split) == 3:
            self.start_idx, self.end_idx, self.weight = [
                int(x) for x in seq_split]
            self.sequence = self.fasta_sequences[protein][self.start_idx:self.end_idx]
        elif len(seq_split) == 2:
            self.sequence, weight_str = seq_split
            self.weight = int(weight_str)
            self.start_idx = 0
            self.end_idx = len(self.sequence)
        else:
            raise ValueError(
                'Invalid format for subsequences (use str:int or int:int:int).')

    def __str__(self):
        return '{}:{}:{}'.format(self.start_idx, self.end_idx, self.weight)


class ScoredResult(object):
    """Object for scoring and storing scored results"""
    fasta_sequences = None
    subsequences = None
    subseq_query = None
    max_score = None

    def __init__(self, pdb_id):
        self.pdb_id = pdb_id
        # Score the pdbid against every subsequence. Scores is a list of tuples
        self.scores = [optimal_levenshtein(
            self.fasta_sequences[self.pdb_id], x) + (len(x),) for x in self.subsequences]
        # Calculate total score for this pdbid
        self.score = self.max_score - \
            sum([x[0] * seq.weight for x, seq in zip(self.scores, self.subseq_query)])
            #   score   weight      scores,seq       merge scores with subsequence_queries

        # Sorts all scores based on their index in the pdb sequence
        sorted_indexed_scores = sorted(self.scores, key=lambda x: x[1])
        self.gaps = []
        # Calculate gaps between subsequences
        for i in range(len(self.scores) - 1):
            left_seq = sorted_indexed_scores[i]
            right_seq = sorted_indexed_scores[i + 1]
            self.gaps.append(right_seq[1] - (left_seq[1] + left_seq[2]))
        self.gaps_abs = sum([abs(x) for x in self.gaps])

    def __lt__(self, other):
        if self.score < other.score:
            return True
        elif self.score == other.score and self.gaps_abs < other.gaps_abs:
            return True
        else:
            return False

    def __eq__(self, other):
        return self.score == other.score and self.pdb_id == other.pdb_id and self.gaps_abs == other.gaps_abs

    def __str__(self):
        return '{}'.format(self.pdb_id)

    def match_str(self):
        """Print out the matches in the string"""
        # Make a list of dashes == len(pdb_seq)
        out = ['-' for x in self.fasta_sequences[self.pdb_id]]
        chars = string.ascii_letters
        for i, score in enumerate(self.scores):
            _, match_start, seq_len = score
            start_chr = chars[i]
            # Replace out[match_start:min(length of subsequence or end of out)] with sequence characters
            for idx in range(match_start, min(match_start + seq_len, len(out))):
                out[idx] = '*' if out[idx] != '-' else start_chr
        return ''.join(out)

def load_fasta(fasta_file):
    """Load all sequences from FASTA file"""
    pdb_sequences = {}
    pdb_id = None
    for line in fasta_file:
        if line.startswith('>'):
            pdb_id = line[1:7]
        else:
            if not pdb_id:
                raise ValueError("Must have pdb_id")
            pdb_sequences[pdb_id.lower()] = line.strip()
            pdb_id = None
    return pdb_sequences


def parse_arguments():
    """Parse command line arguments to the program"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "pdbid", help="pdbid_chain Protein and chain for constrained alignment", nargs='?', default=None)
    parser.add_argument("subsequences", nargs='*',
                        help="X:X:X Specify the subsequence and weight for the contrained alignment", default=[])
    parser.add_argument('-s', '--seq', nargs='+',
                        help='Specify a sequence string and weight (sequence:weight) to search for.', default=[])
    parser.add_argument('--fasta-file', default='libsrc/pdb_seqres.txt',
                        help='Specify file that specifies all the sequences in the PDB in FASTA format')
    parser.add_argument('-o', '--out', default=None,
                        help='Specify output filename.')
    args = parser.parse_args()
    return args


def run_blast(sequence):
    """Run blast and return scored results"""
    blast_cmd = ['./blastp', '-db', 'pdbdb', '-outfmt', '15']
    if len(sequence) < 10:
        # Pads sequence w/ blast wildcard (*)
        sequence = '{s:{c}^{n}}'.format(s=sequence, c='*', n=10)
    if len(sequence) < 30:
        blast_cmd += ['-task', 'blastp-short']
    blast = subprocess.run(blast_cmd, input=sequence.encode('utf-8'), stdout=subprocess.PIPE)
    # Load results from blast
    blast_result_hits = json.loads(blast.stdout.decode(
        'utf-8'))['BlastOutput2'][0]['report']['results']['search']['hits']
    pdb_id = []
    for item in blast_result_hits:
        # Make a list of blast result objects
        pdb_id.append(BlastResult(item))
    return pdb_id


def optimal_levenshtein(haystack, needle):
    """Compute the optimal Levenshtein distance between two strings"""
    # TODO: Consider using more optimal algorithm than this O(n^3)
    # Smith-Waterman can be implemented in O(mn) time and O(n) space
    min_score = len(haystack)
    idx = 0
    for i in range(len(haystack) - len(needle)):
        score = levenshtein(haystack[i:i + len(needle)], needle)
        if score < min_score:
            min_score, idx = score, i
    return (min_score, idx)


def levenshtein(haystack, needle):
    """"Compute levenshtein distance between two strings"""
    old = [x for x in range(len(needle) + 1)]
    new = [0 for x in range(len(needle) + 1)]
    for i, char_h in enumerate(haystack):
        new[0] = i + 1
        for j, char_n in enumerate(needle):
            cost = 0 if char_h == char_n else 1
            new[j + 1] = min([new[j] + 1, old[j + 1] + 1, old[j] + cost])
        old, new = new, old
    return old[len(needle)]


class BlastResult(object):
    """Nice class for storing the results of a Blast query"""

    def __init__(self, blast):
        self.pdb_id = blast['description'][0]['title'][0:6].lower()
        self.score = blast['hsps'][0]['score']
        self.bit_score = blast['hsps'][0]['bit_score']

    def __str__(self):
        return "{}: Score: {}, bit_score: {}".format(self.pdb_id, self.score, self.bit_score)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash((self.pdb_id,))


if __name__ == '__main__':
    main()
