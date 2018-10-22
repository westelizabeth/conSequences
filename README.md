# Constrained Sequence Alignment

## tl;dr
* Running the algorithm
    * Help: `./constrain_align.py -h`
    * Searching for protein subsequences: `./constrain_align.py 1bni_a 10:30:10 40:60:10`
    * Searching for string subsequences: `./constrain_align.py -s ADYLQTYHKLPDNYITKSEA:10 NLADVAPGKSIGGDIFSNRE:10`
* Running the test script
    * Help: `./test_script.py -h`
    * Running with random amino acid sequences: `./test_script.py -r 10 15 20 -w 1 2 3`
    * Running with specific amino acid sequences: `./test_script.py -s AAAAAA QQQQQQQQ -w 1 2`
* Running the parameter sweep
    * Help: `./runParamSweep.py -h`
    * Running with specific maximum, jump, outfile and up to four amino acid sequences: `./runParamSweep.py max jump textfilename.txt AAAAAAA BBBBBBB CCCCCCC DDDDDDD`

## Overview of the Algorithm
[See the algorithm page.](https://gitlab.cs.wwu.edu/jagodzf/prioritySeqAlign/blob/master/algorithm.md)

## Overview of the Test Script
* Input: 1 or more (random or specific) amino acid sequence(s) and corresponding weight(s)
* Output:
    * Results from running BLAST once on the concatenation of the input sequences
    * Results from running the algorithm with the input sequences and corresponding weights

## Installation Guide
* Clone the git repository
* `apt-get install ncbi-blast+`
* Download and unpack BLAST 2.6.0 from [NCBI FTP site](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/)
```
tar -xvf ncbi-blast-2.6.0+-x64-linux.tar.gz
```
* Move blastp from the unpacked ncbi-blast-2.6.0+/bin/ to the root directory of the repo.
* Download most recent version of `pdb_seqres.txt` by running `./update.py`
    * Retrieves `pdb_seqres.txt` from [wwPDB ftp site](ftp://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt)
    * Saves into `libsrc/pdb_seqres.txt`
* Create the database
```
makeblastdb -dbtype prot -in libsrc/pdb_seqres.txt -out pdbdb
```

## Running the Algorithm and the Test Script
Python's argparse should provide enough information to allow you to use both the constrained alignment program and the test script.

## Updating the PDB Database
To update the `pdb_seqres.txt` file that contains all of the most recent entries from the PDB, run:
```
./update.py
```

### Positional Arguments for the Constrained ALignment Program
#### pdbid
Required for indexed subsequence queries. Gives the name of the protein to index into to find the subsequences.
#### subsequences
Required for indexed subsequence queries. Gives the indexes and weights for the subsequences specified.
#### -s \<SEQ>...
Specify a string sequence for searching. Multiple search strings can be provided. Format is \<search_str>:\<weight>
#### -o \<OUTFILE>
Specify the location for the output file.
#### --fasta-file <FASTA_FILE>
Specify the location of the database file used by BLAST.

### Positional Arguments for the Test Script
#### -r random sequences \<LENGTH1>,<LENGTH2>....
Provide an integer to generate a random amino acid sequence of that length. Provide at least 1 or more.
#### -s specific sequences \<SEQ1>,<SEQ2>...
Provide specific strings of amino acids.
#### -w weights \<WEIGHT1>,<WEIGHT2>...
Provide weights for the sequences to be tested. If no weight is supplied, give all the same weight. Must enter as many weights as sequences entered (random or specific).
#### -o outfile \<OUTFILE>
Specify the location of the outfile.

## Dependencies
This software was developed on Ubuntu 16.04. It should work on other operating systems but these instructions are written for Ubuntu 16.04. Some adjustment may be needed to get this software working on other systems.

Prior to setting up the first dependency, it is recommended to install the `ncbi-blast+` package. Do this by running
```
sudo apt-get install ncbi-blast+
```
This package is a meta package that installs BLAST and all of it's dependencies.

This project is dependent on [BLASTP][blast]. To ensure compatability please follow the [instructions to build from a source tarball][blast-from-source]. The version of `blastp` that this project was built using was BLAST 2.6.0. The sources are available to download at the [NCBI FTP site](ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/).

The project also requires a full download of all the sequences in the PDB in the [FASTA format][fasta-format]. The file can be downloaded from the [wwPDB ftp site](ftp://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt). By default the application looks for this file at `libsrc/pdb_seqres.txt`.

The `pdb_seqres.txt` file is also required for building the databases required by `blastp` to operate. Build the databases by running the following command in the root of the repository. It is recommended to use the version of `makeblastdb` that was compiled with your version of `blastp`.

```
makeblastdb -dbtype prot -in libsrc/pdb_seqres.txt -out pdbdb
```


[blast]: https://www.ncbi.nlm.nih.gov/books/NBK279690/
[blast-from-source]: https://www.ncbi.nlm.nih.gov/books/NBK279671/#introduction.Source_tarball
[fasta-format]: https://en.wikipedia.org/wiki/FASTA_format
