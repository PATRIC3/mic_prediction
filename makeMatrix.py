'''
python makeMatrix.py [kmcOut] [arrInd] [antibioList] [micMethods] [out1] [out2] [contigs]
'''

from sys import argv,stderr

# open up the contigs file
f = open(argv[7])

# create array to hold contigs
contigs = []

# for each line in file
# append contig
for i in f:
	i = i.split('\t')[0]
	contigs.append(i)

f.close()

# open up arr index file
f = open(argv[2])

# init feature hash
featureHash = {}

# for each line in file, get the feature and index
# and set it in the hash
for i in f:
	i = i.strip().split('\t')
	if len(i) < 2:
		continue
	featureHash[i[0]] = i[1]

f.close()

# open kmc file
f = open(argv[1])

# init kmc contigs hash
kmcContigs = {}
# for each kmr in file, map kmr to count in hash
for i in f:
	i = i.strip().split('\t')
	kmcContigs[i[0]] = i[1]

# turn these into a line that is formatted:
#   [kmer]:[count] [kmer]:[count] ... [kmer]:[count]
kmcLine = ''
for i in contigs:
	if i in kmcContigs:
		kmcLine += featureHash[i] + ':' + kmcContigs[i] + ' '

f.close()

# open list of antibiotics
f = open(argv[3])

# for each antibiotic in file, append to list
antibioList = []
for i in f:
	# skip comment char
	if i[0] == '#':
		continue
	i = i.strip()
	if i in featureHash:
		antibioList.append(i)

f.close()

# open list of MIC testing methods
f = open(argv[4])

# for each method in file, append to list 
micMethods = []
for i in f:
	i = i.strip()
	if i in featureHash:
		micMethods.append(i)

f.close()

# open two output files
# 1: libsvm out
# 2: antibiotic, MIC testing method order of lbsvm out
f = [open(argv[5], 'w'), open(argv[6], 'w')]

# loop through antibiotic list and MIC methods and print out
# to files
for i in antibioList:
	for j in micMethods:
		line = kmcLine + featureHash[i] + ':1 ' + featureHash[i] + ':1\n'
		f[0].write(line)
		f[1].write(i + '\t' + j + '\n')
