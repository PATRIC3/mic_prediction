# Antimicrobial Resistance Minimum Inhibitory Concentration Prediction

This package predicts the minimum inhibitory concentration of a genome using a trained XGBoost model.  A set of data files are stored in the data_files directory for use with the Klebsiella genus.  A pkl model is also provided for testing purposes as well as a fasta file.  

# 1 Prerequisites

The model requires the installation of Python\*, XGBoost (and python API), and the kmc tool.  The kmc tool must be in your paths otherwise the script will fail to run.  Section 1.1 goes into how to clone this repo, Section 1.2 goes into how KMC is installed, section 1.3 goes into the installation of XGBoost, section 1.3.1 goes into the python API installation using traditional Python, and section 1.3.2 goes into the python API installation if you used Anaconda to install Python.  

\*Note that Python 2.7 is required, Python 3 will not work.  

## 1.1 Cloning this Repo to Use Locally
Although you can download this repo through the github website, it is also possible to clone the repo.  The main advantages to cloning a repo is that it will make updates to the repo a breeze.  Cloning a repo requires that you have the *git* tool installed.  If you do not have *git* installed, you can install it using the following line (requires administrator privileges).

```bash
sudo apt-get install git
```

After installing *git*, you can use git to install this package.  In the terminal, change your current directory to the directory you wish to have the repo extracted to.  Then use the *git* command.  The bash code below shows how you extract the repo into your home directory

```bash
cd ~/
git clone https://github.com/PATRIC3/mic_prediction.git
```

To enter the package root, you can then do the following

```bash
cd mic_prediction
```

### 1.1.1 Updating the Package Using Git

If an update were pushed to the repo (or you feel your repo is out of date), you can quickly update it using the following command:

```bash
cd /path/to/mic_prediction/
git pull
```

This will pull any updates from the github server over to your computer.  

### 1.1.2 Updating the Package Without Git

If you elected to install the package by downloading through the github page, you can simply redownload the package again, delete the existing package, and replace it with the new one.  It is *highly recommended that you use git to update* as it is more seamless and will leave any non-mic_prediction files alone.

## 1.2 Installing KMC
KMC is a 3rd party kmer counting tool that can be used to count kmers.  It offers efficiency through multithreading.  This section will focus on downloading KMC and adding it to our path.  

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

Press [ctrl] + [x] to exit, and press [y] then [enter] to save.  This will install *kmc* onto your machine.  

## 1.3 Installing XGBoost
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
### 1.3.1 Standard Installation
From here, we install the python package.  The directions to do this are here: http://xgboost.readthedocs.io/en/latest/build.html#python-package-installation.  If you have administrator permissions, you can run the following:

```bash
sudo apt-get install python-setuptools
cd python-package; sudo python setup.py install
```

If you do not have administrator permissions, you can run the following:

```bash
cd python-package; python setup.py develop --user
```

You can then test the the installation by doing the following.  First, in the bash terminal, run the following command.

```bash
python
```

This will open up a python terminal for you to use.  In this terminal, we can try to import the XGBoost library by using:

```python
import xgboost as xgb
```

If an error occurs that says that the *xgboost module doesn't exist*, that the *xgboost module can't be found* or something along those lines, that means that XGBoost was not installed properly.  

It should be noted that the Anaconda installation of XGBoost is slightly out of date.  That said, it is currently normal for a warning to pop up saying that:

```
/HOMES/USER_NAME/anaconda2/lib/python2.7/site-packages/sklearn/cross_validation.py:44: DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note that the interface of the new CV iterators are different from that of this module. This module will be removed in 0.20.
  "This module will be removed in 0.20.", DeprecationWarning)
```

### 1.3.2 Anaconda installation
Many people use Anaconda to install their python as it also installs many well known packages.  If you have elected to go this route, you're in good shape.  You simply only have to run the following:

```bash
conda install -c conda-forge xgboost
```

Additionally, the following anaconda package works as well for installation:

```bash
conda install -c anaconda py-xgboost
```

# 2 Running
Once you have installed the tool, cd to the directory of this README file and run the following to ensure that the tool works properly and all required prerequisites and files were obtained during cloning/downloading.

```bash
bash testrun.sh
```

You may get a warning (specified in section 1.3.1) with specific versions of XGBoost and SciKit-Learn.  That is not an issue.  If you get output, then everything is installed properly.  

This package offers two different ways for users to make predictions, either direct from the FASTA file or direct through KMC_dump output.  

## 2.1 Running from FASTA

The *mic_prediction_fasta.sh* script is used to make predictions and takes the name of the following arguments:
- fasta : assembled fasta of genome to be predicted (*test_fasta/1001.fasta*)
- temp : a directory to store temporary data in (*temp/*)
- model : the pkl model produced by XGBoost (*data_files/KPN.mic.FIN.4.pkl*)
- threads : the number of threads to use while running
- output file : the file to output (*test_out/xgbGenomeTest* is provided as an example)
- ArrInd map : a file that maps a feature to an array index (*data_files/Kleb.ArrInds*)
- antibiotic list : a file that contains a list of antibiotics to test on (*data_files/antibioticsList.uniq*)
- method list : a file that contains a list of methdos to test on (*data_files/MICMethods*)
- kmer list : a file that contains a list of kmers that can exist (*data_files/all_kmrs* can be used for **any** model that uses 10-mers)

The test run can be done using the following from the root directory of the AMR predictor tool.

```bash
cd /directory/of/this/file/
bash mic_prediction_fasta.sh test_fasta/1001.fasta temp/ data_files/Kleb.model.pkl 1 test_out/xgbGenomeTest data_files/Kleb.ArrInds data_files/antibioticsList_Kleb.uniq data_files/MICMethods data_files/all_kmrs data_files/Kleb.model.mod_acc
```

This call will make predictions on the 1001.fasta file which is a fasta containing contigs for a Klebsiella genome.  Note that the model provided is only designed to make predictions for Klebsiella genomes.  To run on your own fasta, just replace the location of the fasta (*test_fasta/1001.fasta*) file with the location of your own fasta file.  

The script will call the *kmc.sh* script which in turn calls kmc to find 10 mers for the given fasta file.  Afterwards the *makeMatrix.py* script is used to create a libsvm formatted file for XGBoost to use to make predictions with.  The *testXGBoost.py* script is then used to make predictions using the already trained XGBoost model.  The output is then sent to the specified file.  

The file contains the following:
1. The first line gives the name of the fasta file used
2. A tab delimited file containing the following columns
	- Antibiotic : The antibiotic the MIC prediction is for.
	- MIC Test Method	: This is the testing method that is being predicted for.  As of right now, the only data that is trained is that from the *BD Pheonix* method.  The predictions will state this.
	- Prediction : The predicted MIC value.

For certain antibiotics, the statistics for the given score will say "*prediction out of range*" when there exists no actual sample with a MIC value that is predicted for a given antibiotic.  For example, in the sample output below, there exists no Ertapenem samples with a MIC of 8.  

In short, two sets of accuracy measures are provided for each prediction.  The first set reports model accuracies on a particular antibiotic (overall) while the second set reports model accuracies on a particular antibiotic at a particular MIC value.  

The sample output will be formatted like the following:

```
test_fasta/1001.fasta
Antibiotic	MIC Test Method	Prediction
Amikacin	BD_Pheonix	8.0
Ampicillin	BD_Pheonix	32.0
Ampicillin/Sulbactam	BD_Pheonix	32.0
Aztreonam	BD_Pheonix	16.0
Cefazolin	BD_Pheonix	32.0
Cefepime	BD_Pheonix	16.0
Cefoxitin	BD_Pheonix	16.0
Ceftazidime	BD_Pheonix	32.0
Ceftriaxone	BD_Pheonix	4.0
Cefuroxime sodium	BD_Pheonix	0.125
Ciprofloxacin	BD_Pheonix	16.0
Gentamicin	BD_Pheonix	0.125
Imipenem	BD_Pheonix	128.0
Levofloxacin	BD_Pheonix	32.0
Meropenem	BD_Pheonix	16.0
Nitrofurantoin	BD_Pheonix	128.0
Piperacillin/Tazobactam	BD_Pheonix	16.0
Tetracycline	BD_Pheonix	4.0
Tobramycin	BD_Pheonix	16.0
Trimethoprim/Sulfamethoxazole	BD_Pheonix	16.0
```

## 2.2 Running from KMC Output

Additionally, you can run this tool using known KMC output, this also allows you to quickly script with a directory full of genomes that have been run through the KMC tool.  This is done using the *mic_prediction_kmc.sh* script.  It takes the following arguments:
- KMC output : output from *kmc_dump* tool (*test_fasta/1001.fasta.10.kmrs*)
- temp : a directory to store temporary data in (*temp/*)
- model : the pkl model produced by XGBoost (*data_files/KPN.mic.FIN.4.pkl*)
- threads : the number of threads to use while running
- output file : the file to output (*test_out/xgbGenomeTest* is provided as an example)
- ArrInd map : a file that maps a feature to an array index (*data_files/Kleb.ArrInds*)
- antibiotic list : a file that contains a list of antibiotics to test on (*data_files/antibioticsList.uniq*)
- method list : a file that contains a list of methdos to test on (*data_files/MICMethods*)
- kmer list : a file that contains a list of kmers that can exist (*data_files/all_kmrs* can be used for **any** model that uses 10-mers)

An example run of this script is below.  

```bash
bash mic_prediction_kmc.sh test_fasta/1001.fasta.10.kmrs temp/ data_files/Kleb.model.pkl 1 test_out/xgbGenomeTest.KMC data_files/Kleb.ArrInds data_files/antibioticsList_Kleb.uniq data_files/MICMethods data_files/all_kmrs data_files/Kleb.model.mod_acc
```

The KMC output file in this case is the output from the *kmc_dump* tool included with KMC.  This requires you to run both *kmc* and *kmc_dump*.  

## 2.3 Getting Model Accuracies
All data for the accuracy of models and confidence intervals are stored in the \*.mod_acc file.  For the provided Klebsiella model, the file *data_files/Kleb.model.mod_acc* provides the appropriate accuracies accross different antibiotic and MIC combinations.  Simply find the right line and read accross.  The file contains the following columns per line:
- Antibiotic : the antibiotic for the accuracy measurements
- MIC : the MIC value for the accuracy measurements
- Average W1 antibiotic : the overall average score for the antibiotic MIC predictions
- 95-conf low antibiotic : the lower end of the 95% C.I. for the antibiotic predictions
- 95-conf high antibiotic : the upper end of the 95% C.I. for the antibiotic predictions
- Number of Antibiotic Samples : the number of antibiotic samples trained on
- Avg : the average W1 score for the given antibiotic-MIC combination
- 95-Conf Low : the lower end of the 95% C.I. for the antibiotic-MIC combination predictions
- 95-Conf High : the upper end of the 95% C.I. for the antibiotic-MIC combination predictions
- 95-Conf Size : the size of the C.I. for the antibiotic-MIC combination predictions
- Number of Samples : the number of antibiotic samples at the given MIC value trained on



