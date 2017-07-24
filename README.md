# Antimicrobial Resistance Minimum Inhibitory Concentration Prediction

This package predicts the minimum inhibitory concentration of a genome using a trained XGBoost model.  A set of data files are stored in the data_files directory for use with the Klebsiella genus.  A pkl model is also provided for testing purposes as well as a fasta file.  

# 1 Prerequisites

The model requires the installation of XGBoost and the kmc tool.  The kmc tool must be in your paths otherwise the script will fail to run.  

## 1.1 Installing KMC
Linux and Mac OS X executables for KMC are available through this URL: http://sun.aei.polsl.pl/REFRESH/index.php?page=projects&project=kmc&subpage=download.  Download the executable and untar the file using

```bash
tar -xvf KMC3.*.tar
```

This will produce three files:
- kmc
- kmc_dump
- kmc_tools

Copy these into a directory of its own.  If you have administrator access to your computer, you can run the following (1):

```
sudo mv kmc* /usr/bin/
```

If not, make a *bin* directory in your home directory, copy the three files to that directory, and add it to your path by doing (2):

```bash
if [ ! -d ~/bin/ ]; then
	mkdir ~/bin/
fi
cp kmc* ~/bin/
PATH=~/bin/:$PATH
```

If you followed the directions from (2), then you can also add the following line to the end of your *~/bashrc* (Linux) or *~/bash_profile* (OS X) file by using the following.

```
nano ~/.bashrc #use nano ~/.bash_profile if error
```

Scroll to the bottom of the file and add to the end of the file:

```
PATH=~/bin/:$PATH
```

Press [ctrl] + [x] to exit, and press [y] to save.  This will install *kmc* onto your machine.  

## 1.2 Installing XGBoost
### 1.2.1 Standard Installation
The directions for installing XGBoost can be found here: http://xgboost.readthedocs.io/en/latest/build.html.  You will want to install both the C++ library and the Python API.  In order to do this, you'll have to have git installed.  This installation requires administrator privileges.

```bash
sudo apt-get update
sudo apt-get install git
# follow directions on screen
```

Once this is done, you can go ahead and install XGBoost.  If you are on Linux, you do this by running the following:

```bash
git clone --recursive https://github.com/dmlc/xgboost
cd xgboost; make -j4
```

If you're on OS X, you'll instead run the following:

```bash
git clone --recursive https://github.com/dmlc/xgboost
cd xgboost; cp make/minimum.mk ./config.mk; make -j4
```

From here, we install the python package.  The directions to do this are here: http://xgboost.readthedocs.io/en/latest/build.html#python-package-installation.  If you have administrator permissions, you can run the following:

```bash
sudo apt-get install python-setuptools
cd python-package; sudo python setup.py install
```

If you do not have administrator permissions, you can run the following:

```bash
cd python-package; python setup.py develop --user
```

You can then test the the installation by running the following quick python script:

```python
import xgboost as xgb
```

### 1.2.2 Anaconda installation
Many people use Anaconda to install their python as it also installs many well known packages.  If you have elected to go this route, you're in good shape.  You simply only have to run the following:

```bash
conda install -c conda-forge xgboost
```

# 2 Running

The *testGenomeXGBoost.sh* script is used to make predictions and takes the name of the following arguments:
- fasta : assembled fasta of genome to be predicted (*test_fasta/1001.fasta*)
- temp : a directory to store temporary data in (*temp/*)
- model : the pkl model produced by XGBoost (*data_files/KPN.mic.FIN.4.pkl*)
- threads : the number of threads to use while running
- output file : the file to output (*test_out/xgbGenomeTest* is provided as an example)
- ArrInd map : a file that maps a feature to an array index (*data_files/ArrInds*)
- antibiotic list : a file that contains a list of antibiotics to test on (*data_files/antibioticsList.uniq*)
- method list : a file that contains a list of methdos to test on (*data_files/MICMethods*)
- kmer list : a file that contains a list of kmers that can exist (*data_files/all_kmrs* can be used for **any** model that uses 10-mers)

The test run can be done using the following from the root directory of the AMR predictor tool.

```bash
cd /directory/of/this/file/
bash testGenomeXGBoost.sh test_fasta/1001.fasta temp/ data_files/Kleb.table.10cv.0.0.pkl 12 test_out/xgbGenomeTest data_files/ArrInds data_files/antibioticsList_Kleb.uniq data_files/MICMethods data_files/all_kmrs
```

This call will make predictions on the 1001.fasta file which is a fasta containing contigs for a Klebsiella genome.  Note that the model provided is only designed to make predictions for Klebsiella genomes.  

The script will call the *kmc.sh* script which in turn calls kmc to find 10 mers for the given fasta file.  Afterwards the *makeMatrix.py* script is used to create a libsvm formatted file for XGBoost to use to make predictions with.  The *testXGBoost.py* script is then used to make predictions using the already trained XGBoost model.  The output is then sent to the specified file.  

The file contains the following:
1. The first line gives the name of the fasta file used
2. A tab delimited file containing the following columns
	- Antibiotic (antibiotic for prediction)
	- MIC Test Method (MIC testing method predicted)
	- Low Bound (the within 1 2-fold dilution lower bound)
	- Prediction (the prediction given by the model)
	- High Bound (the within 1 2-fold dilution upper bound)

The sample output will be formatted like the following:

```
test_fasta/1001.fasta
Antibiotic	MIC Test Method	Low Bound (within 1)	Prediction	High Bound (within 1)
Amikacin	MIC	4.0	8.0	16.0
Ampicillin	MIC	16.0	32.0	64.0
Aztreonam	MIC	8.0	16.0	32.0
Cefazolin	MIC	16.0	32.0	64.0
Cefepime	MIC	2.0	4.0	8.0
Cefoxitin	MIC	4.0	8.0	16.0
Ceftazidime	MIC	8.0	16.0	32.0
Ceftriaxone	MIC	32.0	64.0	128.0
Cefuroxime sodium	MIC	16.0	32.0	64.0
Ciprofloxacin	MIC	2.0	4.0	8.0
Ertapenem	MIC	4.0	8.0	16.0
Fosfomycin	MIC	4.0	8.0	16.0
Gentamicin	MIC	4.0	8.0	16.0
Imipenem	MIC	0.5	1.0	2.0
Levofloxacin	MIC	2.0	4.0	8.0
Meropenem	MIC	0.5	1.0	2.0
Nitrofurantoin	MIC	32.0	64.0	128.0
Tetracycline	MIC	8.0	16.0	32.0
Tobramycin	MIC	4.0	8.0	16.0
```
