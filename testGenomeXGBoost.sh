# !/bin/bash

# testGenomeXGBoost.sh [fasta] [temp] [model] [threads] 
#   [output file] [ArrInd map] [antibiotic list] [method list]
#   [kmer list]
# 
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
base=$(basename $1)
mod=$3
inds=$6
anti=$7
meth=$8
cont=$9

echo $1 > $5

$DIR/kmc.sh 10 $1 $2/$base $2 > $2/$base.kmc.stdout
python $DIR/makeMatrix.py $2/$base.10.kmrs $inds $anti $meth $2/$base.libsvm $2/$base.matOrd $cont
python $DIR/testXGBoost.py $3 $2$base.libsvm $2$base.matOrd $4 | tail -n +2 >> $5

rm $2/*