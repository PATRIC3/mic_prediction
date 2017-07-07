# Antimicrobial Resistance Minimum Inhibitory Concentration Prediction

This package predicts the minimum inhibitory concentration of a genome using a trained XGBoost model.  A set of data files are stored in the data_files directory for use with the Klebsiella genus.  A pkl model is also provided for testing purposes as well as a fasta file.  

# Prerequisites

The model requires the installation of XGBoost and the kmc tool.  The kmc tool must be in your paths otherwise the script will fail to run.  

# Running

The testGenomeXGBoost.sh script is used to make predictions and takes the name of the following arguments:
- fasta : fasta to be predicted (*test_fasta/1001.fasta*)
- temp : a directory to store temp data in (*temp/*)
- model : the pkl model produced by XGBoost (*data_files/KPN.mic.FIN.4.pkl*)
- threads : the number of threads to use while running
- output file : the file to output (*test_out/xgbGenomeTest* is provided as an example)
- ArrInd map : a file that maps a feature to an array index (*data_files/ArrInds*)
- antibiotic list : a file that contains a list of antibiotics to test on (*data_files/antibioticsList.uniq*)
- method list : a file that contains a list of methdos to test on (*data_files/MICMethods*)
- kmer list : a file that contains a list of kmers that can exist (*data_files/all_kmrs* can be used for **any** model that uses 10-mers)

The script will call the *kmc.sh* script which in turn calls kmc to find 10 mers for the given fasta file.  Afterwards the *makeMatrix.py* script is used to create a libsvm formatted file for XGBoost to use to make predictions with.  The *testXGBoost.py* script is then used to make predictions.  The output is then sent to the specified file.  

The file contains the following:
1. The first line gives the name of the fasta file used
2. A tab delimited file containing the following columns
	- Antibiotic (antibiotic for prediction)
	- MIC Test Method (MIC testing method predicted)
	- Low Bound (the within 1 2-fold dilution lower bound)
	- Prediction (the prediction given by the model)
	- High Bound (the within 1 2-fold dilution upper bound)


