#!/bin/bash

# check argument count, 4 arguments are required to run script
# if less than 4 provided, output usage information
if (( $# != 4 )); then
	echo usage: "$0 [k] [file in] [file out] [temp dir]"
	echo "Uses kmc to get kmers and kmc_dump to print"
	echo "Outputs readable file to [file out].[k].kmrs"
	echo $# args supplied
	exit
fi

# set the argument numbers to appropriate variables
k=$1
fin=$2
fout=$3
dir=$4

if [ ! -f $fin ]; then
	>&2 echo $fin does not exist
	exit 1
fi

# run KMC
kmc -k$k -fm -ci1 -cs1677215 $fin $fout $dir
# run KMC dump
kmc_dump $fout $fout.$k.kmrs