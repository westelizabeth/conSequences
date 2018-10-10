# Constrained Sequence Alignment

## Old Version

### Who
Sasa and Dane

### What
* Sort sequences in some way
  * Length
  * Weight
  * Command line order
* Score first sequence using BLAST
  * Set scores for each matched sequence to `bitscore*weight`
* If **not** `blast_anchor`
  * Add every protein in the PDB to the search space
  * Give it initial score of 0
* Score results using levenshtein distance or the else branch
  * If `levenshtein`: `score += (seq len - minLevDistance) * weight`
  * Else `score += (seqLength * weight)`
* Sort based on score
* Print out results

### Why
These are assumptions based on my understanding of their algorithm.

#### Pros
* Blast quickly produces good alignments so it is a good place to start searching for alignments.
  * In fact, blast is probably the best alignment tool and we should offload as much work as possible to it.
* Lots of command line options for sorting sequences
* Attempt to use bitap algorithm for more speed
  * Uses same scoring method as Levenshtein distance so it's only useful to improve performance


#### Cons
* BlastAnchor adds the entire PDB to the search space making computation take a “long time”
* Even they admit that bitscore * weight is a strange way to start the scores since the bitscore is arbitrary
* Written in Java
* Only running Blast on the “first” sequence
  * What if something from a later sequence has a better match overall but wasn’t included because it wasn’t “first”
* No utilization of blastp-short for short sequences
* Dubious viability when only allowed to search for subsequences of other proteins
* Actually just calculated indexes wrong

### When
Before Kyle and Logan took over.

### How 
I would assume with a commercially available text editor.
* Java
* Blast
* PDB offline FASTA sequences file

## (Mostly Kyle) and Logan's Version
### Who
Kyle and Logan made an algorithm that is better than the one Sasa and Dane made (potential bias this was written by Kyle).
### What
* temp_results = set()
* max_score = length(x) * weight(x) for all user supplied sequences
* For each user supplied sequence
  * temp_results += proteins returned from blast search for sequence
* For all proteins in the temp_results set
  * Score = max_score
  * For each user supplied sequence
    * Score += levenshtein distance(seq, result) * weight
* Sort by (only) score
* Return results (by printing)

### Why
#### Pros
* Runs blast on each sequence
* Uses blastp-short and padding for small sequences
* Runs on any arbitrary user entered sequence
* Allows for custom weights
* Gives some indication of where the matches are
* Indicates distances between gaps
* I hope the output is machine readable
* Python

#### Cons
* In the matches indicator all letters after the first of a type are only there to show the length of the sequence trying to be matched.
  * For example --aaaabbbb-- the character at index 2 matched the first character of sequence a and the character at index 6 matched the first character of sequence b, the rest of the letters show the length of the sequence
* Final result sorting is only done by score. There is little attempt to give deterministic results.
  * Should definately put some work in here to allow users to sort results by something a little more useful
* Score “classes” may be too broad
  * For example, is there a way to distinguish between proteins that share a “perfect” score?
  * Create additional metrics to allow for this to happen
    * Hopefully they are biologically inspired
* Levenshtein distance only accounts for exact matches
  * Using Smith-Waterman may be a better matching algorithm (allows for gaps)
* Thinks chains of the same protein are different proteins
* Short sequences (length less than 8ish) may return no results from BLAST
* I am better at finding cons than pros

### When
This quarter *wink*.
### How
Mostly with:
* Visual Studio Code
* Python 3
* Blast 2.6.0
* PDB offline FASTA sequences file

### Output Format
```
<pdbid>_<chain> | Score: <actual score>, Gaps: <array of gaps from first match until last>
<FASTA sequence for pdbid>
<matches indicator>
<this line intentionally left blank>
<repeat>
```

### Future Advancements
* Smith-Waterman instead of (or alongside of Levenshtein distance)
* New language for defining weights for subsequences of subsequences
* Something about gaps
