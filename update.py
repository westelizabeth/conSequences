#!/usr/bin/env python3
from urllib.request import urlopen
from os import system

# Get the most recent data from the pdb and write to libsrc/pdb_seqres.txt
data = urlopen("ftp://ftp.wwpdb.org/pub/pdb/derived_data/pdb_seqres.txt").read()
with open("libsrc/pdb_seqres.txt", "w") as f:
    f.write(data.decode('utf-8'))

# Create new blast db based off updated file
cmd = "makeblastdb -dbtype prot -in libsrc/pdb_seqres.txt -out pdbdb"
system(cmd)
