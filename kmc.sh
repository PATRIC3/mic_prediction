#!/bin/bash

if (( $# != 4 )); then
	echo usage: "$0 [k] [file in] [file out] [temp dir]"
	echo "Uses kmc to get kmers and kmc_dump to print"
	echo "Outputs readable file to [file out].[k].kmrs"
	echo $# args supplied
	exit
fi

k=$1
fin=$2
fout=$3
dir=$4

kmc -k$k -fm -ci1 -cs1677215 $fin $fout $dir
kmc_dump $fout $fout.$k.kmrs