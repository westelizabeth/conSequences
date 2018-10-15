#!/bin/bash


#Go through all directories and unzip files
shopt -s dotglob
find * -prune -type d | while IFS= read -r d; do
    echo "$d"
    cd $d
    for f in *.tar.gz; do tar -xf $f; done
    cd ..
done


for f in *.tar.gz; do tar -xf $f; done

failure=0;

blastp="./blastp"
if [ -f "$blastp" ]
then
	echo "$blastp found."
else
	echo "$blastp not found."
  let "failure+=1"
fi

algorithmmd="./algorithm.md"
if [ -f "$algorithmmd" ]
then
	echo "$algorithmmd found."
else
	echo "$algorithmmd not found."
  let "failure+=1"
fi

constrainalign="./constrain_align.py"
if [ -f "$constrainalign" ]
then
	echo "$constrainalign found."
else
	echo "$constrainalign not found."
  let "failure+=1"
fi

pdbseqres="./libsrc/pdb_seqres.txt"
if [ -f "$pdbseqres" ]
then
	echo "$pdbseqres found."
else
	echo "$pdbseqres not found."
  let "failure+=1"
fi

paramsweep="./paramsweep.sh"
if [ -f "$paramsweep" ]
then
	echo "$paramsweep found."
else
	echo "$paramsweep not found."
  let "failure+=1"
fi

pdbdbphr="./pdbdb.phr"
if [ -f "$pdbdbphr" ]
then
	echo "$pdbdbphr found."
else
	echo "$pdbdbphr not found."
  let "failure+=1"
fi

pdbdbpin="./pdbdb.pin"
if [ -f "$pdbdbpin" ]
then
	echo "$pdbdbpin found."
else
	echo "$pdbdbpin not found."
  let "failure+=1"
fi

pdbdbpsq="./pdbdb.psq"
if [ -f "$pdbdbpsq" ]
then
	echo "$pdbdbpsq found."
else
	echo "$pdbdbpsq not found."
  let "failure+=1"
fi


psweep3="./psweep3.sh"
if [ -f "$psweep3" ]
then
	echo "$psweep3 found."
else
	echo "$psweep3 not found."
  let "failure+=1"
fi

psweep4="./psweep4.sh"
if [ -f "$psweep4" ]
then
	echo "$psweep4 found."
else
	echo "$psweep4 not found."
  let "failure+=1"
fi

runParamSweep="./runParamSweep.py"
if [ -f "$runParamSweep" ]
then
	echo "$runParamSweep found."
else
	echo "$runParamSweep not found."
  let "failure+=1"
fi

testscript="./test_script.py"
if [ -f "$testscript" ]
then
	echo "$testscript found."
else
	echo "$testscript not found."
  let "failure+=1"
fi

update="./update.py"
if [ -f "$update" ]
then
	echo "$update found."
else
	echo "$update not found."
  let "failure+=1"
fi

#textfiles
analyze="./textfiles/analyze.py"
if [ -f "$analyze" ]
then
	echo "$analyze found."
else
	echo "$analyze not found."
  let "failure+=1"
fi

parse="./textfiles/parse.py"
if [ -f "$parse" ]
then
	echo "$parse found."
else
	echo "$parse not found."
  let "failure+=1"
fi

if [[ "$failure" -eq 0 ]];
 then echo "ALL FILES PRESENT"
 else echo "REQUIRED FILE MISSING"
fi

#The runtime arguments are as follows: $1 is the path to the file containing
#the list of files $2 is the path to the directory containing the files What I
#want to do is check that each file listed in $1 exists in the $2 directory

#while IFS= read -r f; do
#    if [[ -e $2/$f ]]; then
#        printf '%s exists in %s\n' "$f" "$2"
#    else
#        printf '%s is missing in %s\n' "$f" "$2"
#        exit 1
#    fi
#done < "$1"
