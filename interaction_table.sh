#!/bin/bash

yourfilenames=`ls *.pdb`
echo $yourfilenames
var='.pdb'
replace='.csv'
echo "Interaction table" > "table.csv"
for i in ${yourfilenames[@]}
do
    echo "$i" >> "table.csv"
    echo "Ligand,Residue_No,Atom_Name,Chain,Atom_No,,Residue_Name,Residue_No,Atom_Name,Chain,Atom_No,,Distance" >> "table.csv"
    ./pdb_std -i $i -E
    arr=${i/".pdb"/$replace}
    mv Active_site3 $arr   
done
echo "DONE!"
