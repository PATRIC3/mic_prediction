# !/bin/bash

# testGenomeXGBoost.sh [fasta] [temp] [model] [threads] 
#   [output file] [ArrInd map] [antibiotic list] [method list]
#   [kmer list] [model accuracy]
# 
#

# set temp directory
temp=$2

# if temp doesn't have '/' at end, add it
if [[ "${2:${#2}-1}" != "/" ]]; then
	temp="$2"/
fi

# init varaibles
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
base=$(basename $1)
mod=$3
inds=$6
anti=$7
meth=$8
cont=$9
macc=${10}

# echo file name to file
echo $1 > $5

# build libsvm matrix
python $DIR/makeMatrix.py $1 $inds $anti $meth $temp/$base.libsvm $temp/$base.matOrd $cont
# make predictions and send to file
python $DIR/testXGBoost.py $3 $temp$base.libsvm $temp$base.matOrd $4 $macc | tail -n +2 >> $5

# remove temp files
rm $temp/*