# !/bin/bash

# testGenomeXGBoost.sh [fasta] [temp] [model] [threads] 
#   [output file] [ArrInd map] [antibiotic list] [method list]
#   [kmer list] [model accuracy]
# 
#

temp=$2

if [[ "${2:${#2}-1}" != "/" ]]; then
	temp="$2"/
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
base=$(basename $1)
mod=$3
inds=$6
anti=$7
meth=$8
cont=$9
macc=${10}

echo $macc

echo $1 > $5

$DIR/kmc.sh 10 $1 $temp/$base $temp > $temp/$base.kmc.stdout
python $DIR/makeMatrix.py $temp/$base.10.kmrs $inds $anti $meth $temp/$base.libsvm $temp/$base.matOrd $cont
python $DIR/testXGBoost.py $3 $temp$base.libsvm $temp$base.matOrd $4 $macc | tail -n +2 >> $5

rm $temp/*