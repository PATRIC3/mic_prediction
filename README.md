# Antimicrobial Resistance Minimum Inhibitory Concentration Prediction

This package predicts the minimum inhibitory concentration of a genome using a trained XGBoost model.  A set of data files are stored in the data_files directory for use with the Klebsiella genus.  A pkl model is also provided for testing purposes as well as a fasta file.  

# 1 Prerequisites

The model requires the installation of Python\*, XGBoost (and python API), and the kmc tool.  The kmc tool must be in your paths otherwise the script will fail to run.  Section 1.1 goes into how KMC is installed, section 1.2 goes into the installation of XGBoost, section 1.2.1 goes into the python API installation using traditional Python, and section 1.2.2 goes into the python API installation if you used Anaconda to install Python.  

\*Note that Python 2.7 is required, Python 3 will not work.  

## 1.1 Installing KMC
Linux and Mac OS X executables for KMC are available through this URL: http://sun.aei.polsl.pl/REFRESH/index.php?page=projects&project=kmc&subpage=download.  Download the executable and untar the file using:

```bash
cd ~/Downloads/  #This is the default directory for downloads, make sure the KMC3 download is in this directory, otherwise, replace "~/Downloads/" with the appropriate directory
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
### 1.2.1 Standard Installation
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

This call will make predictions on the 1001.fasta file which is a fasta containing contigs for a Klebsiella genome.  Note that the model provided is only designed to make predictions for Klebsiella genomes.  To run on your own fasta, just replace the location of the fasta (*test_fasta/1001.fasta*) file with the location of your own fasta file.  

The script will call the *kmc.sh* script which in turn calls kmc to find 10 mers for the given fasta file.  Afterwards the *makeMatrix.py* script is used to create a libsvm formatted file for XGBoost to use to make predictions with.  The *testXGBoost.py* script is then used to make predictions using the already trained XGBoost model.  The output is then sent to the specified file.  

The file contains the following:
1. The first line gives the name of the fasta file used
2. A tab delimited file containing the following columns
	- Antibiotic : The antibiotic the MIC prediction is for.
	- MIC Test Method	Prediction : The predicted MIC value.
	- Average W1 antibiotic : Average within 1 two-fold dilution factor accuracy for the given antibiotic.
	- 95-conf low antibiotic : The lower bound for the 95% confidence interval for the within 1 two-fold dilution factor accuracy for the given antibiotic.
	- 95-conf high antibiotic : The upper bound for the 95% confidence interval for the within 1 two-fold dilution factor accuracy for the given antibiotic.
	- Number of Antibiotic Samples : The number of samples trained for the given antibiotic.
	- Avg	95-Conf Low : The average within 1 two-fold dilution factor accuracy for the antibiotic at the predicted MIC value.
	- 95-Conf High : The lower bound for the 95% confidence interval for the within 1 two-fold dilution factor accuracy for the antibiotic at the predicted MIC value.
	- 95-Conf Size : The upper bound for the 95% confidence interval for the within 1 two-fold dilution factor accuracy for the antibiotic at the predicted MIC value.
	- Number of Samples : The number of samples trained on for the antibiotic at the given MIC value.  
	<!-- - Antibiotic (antibiotic for prediction)
	- MIC Test Method (MIC testing method predicted)
	- Low Bound (the within 1 2-fold dilution lower bound)
	- Prediction (the prediction given by the model)
	- High Bound (the within 1 2-fold dilution upper bound) -->

The sample output will be formatted like the following:

```
test_fasta/1001.fasta
Antibiotic	MIC Test Method	Prediction	Average W1 antibiotic	95-conf low antibiotic	95-conf high antibiotic	Number of Antibiotic Samples	Avg	95-Conf Low	95-Conf High	95-Conf Size	Number of Samples
Amikacin	BD_Pheonix	4.0	0.969298406925	0.959960495127	0.978636318723	1773	0.957376614613	0.935428753509	0.979324475718	0.0438957222084	169.0
Ampicillin	BD_Pheonix	32.0	0.996166191049	0.994264916636	0.998067465461	1772	0.997241705104	0.99515407074	0.999329339469	0.00417526872846	1738.0
Aztreonam	BD_Pheonix	16.0	0.891708547704	0.872592902401	0.910824193008	1749	1.0	1.0	1.0	0.0	93.0
Cefazolin	BD_Pheonix	4.0	0.960888634578	0.952537770768	0.969239498387	1773	0.416666666667	0.00198701967945	0.831346313654	0.829359293974	13.0
Cefepime	BD_Pheonix	8.0	0.601583293055	0.569013976278	0.634152609831	1672	0.956547619048	0.906003691158	1.00709154694	0.101087855778	76.0
Cefoxitin	BD_Pheonix	4.0	0.910395994857	0.893073691026	0.927718298689	1747	0.823524769113	0.774696153527	0.8723533847	0.0976572311727	449.0
Ceftazidime	BD_Pheonix	4.0	0.90588441329	0.895740694246	0.916028132334	1773	0.5	0.112997513558	0.887002486442	0.774004972884	17.0
Ceftriaxone	BD_Pheonix	4.0	0.888020735415	0.871767521672	0.904273949158	1773	0.375	-0.386740090415	1.13674009041	1.52348018083	9.0
Cefuroxime sodium	BD_Pheonix	4.0	0.991192186746	0.98757212432	0.994812249172	1681	0.911388888889	0.861272130662	0.961505647116	0.100233516454	85.0
Ciprofloxacin	BD_Pheonix	2.0	0.970461862497	0.961936295145	0.97898742985	1770	0.966666666667	0.891261427909	1.04207190542	0.150810477516	42.0
Ertapenem	BD_Pheonix	8.0	prediction out of range
Fosfomycin	BD_Pheonix	8.0	prediction out of range
Gentamicin	BD_Pheonix	4.0	0.936032721813	0.92002951831	0.952035925316	1773	0.985413943355	0.96821159824	1.00261628847	0.0344046902312	191.0
Imipenem	BD_Pheonix	1.0	0.936667080546	0.925895298013	0.947438863079	1772	0.963996335714	0.947750509881	0.980242161547	0.0324916516659	1061.0
Levofloxacin	BD_Pheonix	0.5	prediction out of range
Meropenem	BD_Pheonix	4.0	0.91878325845	0.906443008617	0.931123508284	1762	0.788571428571	0.650217083345	0.926925773798	0.276708690452	66.0
Nitrofurantoin	BD_Pheonix	4.0	prediction out of range
Tetracycline	BD_Pheonix	0.5	prediction out of range
Tobramycin	BD_Pheonix	1.0	0.935438298873	0.92152099106	0.949355606686	1772	0.922297979798	0.864693558084	0.979902401512	0.115208843427	104.0

```
